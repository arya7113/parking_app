from app.internals.endpoints.__init__ import *
from app.internals.models.model import *
from app.internals.endpoints.auth.form import *
from app.internals.endpoints.admin.form import *
import matplotlib.pyplot as plt
import io
import base64


def Admin_Dashboard():
    lots = Parking_Lots.query.all()
    lots_data = []

    for lot in lots:
        spots = Parking_Spot.query.filter_by(lot_id=lot.id).order_by(Parking_Spot.spot_number.asc()).all()

        # Calculate occupied and available inside the loop for each lot
        occupied = sum(1 for s in spots if s.status == "occupied")
        available = sum(1 for s in spots if s.status == "available")

        spot_list = []
        for spot in spots:
            spot_list.append({
                "id": spot.id,
                "number": spot.spot_number,
                "status": spot.status
            })

        lots_data.append({
            "id": lot.id,
            "name": lot.location_name,
            "address": lot.address,
            "pin_code": lot.pin_code,
            "total_spots": lot.total_spots,
            "available_spots": available,
            "price_per_hour": lot.price_per_hour,
            "occupied_spots": occupied,
            "spots": spot_list
        })

    nav_data = {
        'page_title': 'Admin Dashboard',
        'site_title': {'name': 'My Park Place', 'url': Home_Url, 'active': False},
        'nav_items': [
            {'text': 'Home', 'url': Admin_Home_Url, 'active': True},
            {'text': 'Users', 'url': Admin_Users_Url, 'active': False},
            {'text': 'Summary', 'url': Admin_Summary_Url, 'active': False}
        ],
        'logout': True
    }

    return render_template(
        'admin/dashboard.html',
        lots=lots_data,
        **nav_data,
        access_token=request.cookies.get('access_token')
    )
def Add_Parking_Lot():
    form = AddParkingLotForm()
    nav_data = {
        'page_title': 'Add Parking Lot',
        'site_title': {'name': 'My Park Place', 'url': Home_Url, 'active': False},
        'nav_items': [
            {'text': 'Home', 'url': Admin_Home_Url, 'active': False},
            {'text': 'Users', 'url': Admin_Users_Url, 'active': False},
            {'text': 'Summary', 'url':Admin_Summary_Url, 'active': False}
        ],
        'logout': True
    }
    
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                total_spots = int(form.total_spots.data)
                new_lot = Parking_Lots(
                    location_name=form.location_name.data,
                    address=form.address.data,
                    pin_code=form.pin_code.data,
                    total_spots=total_spots,
                    available_spots=total_spots,
                    price_per_hour=float(form.price_per_hour.data)
                )

                db.session.add(new_lot)
                db.session.flush()  # so we get new_lot.id

                # Auto-generate spots
                for i in range(1, total_spots + 1):
                    spot = Parking_Spot(
                        lot_id=new_lot.id,
                        spot_number=str(i),
                        status='available'
                    )
                    db.session.add(spot)

                db.session.commit()
                flash('Parking lot and spots added successfully!', 'success')
                return redirect(url_for('admin_dashboard'))

            except Exception as e:
                db.session.rollback()
                flash(f'Error: {str(e)}', 'danger')

    return render_template('admin/add_parking_lot.html', form=form, **nav_data)


def Edit_Parking_Lot(lot_id):
    lot = Parking_Lots.query.get_or_404(lot_id)
    form = EditParkingLotForm(obj=lot)

    nav_data = {
        'page_title': 'Edit Parking Lot',
        'site_title': {'name': 'My Park Place', 'url': Home_Url, 'active': False},
        'nav_items': [
            {'text': 'Home', 'url': Admin_Home_Url, 'active': False},
            {'text': 'Users', 'url': Admin_Users_Url, 'active': False},
            {'text': 'Summary', 'url': Admin_Summary_Url, 'active': False}
        ],
        'logout': True
    }
    
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                old_total_spots = lot.total_spots
                new_total_spots = int(form.total_spots.data)

                # Update basic fields
                lot.location_name = form.location_name.data
                lot.address = form.address.data
                lot.pin_code = form.pin_code.data
                lot.total_spots = new_total_spots
                lot.price_per_hour = float(form.price_per_hour.data)

                if new_total_spots < old_total_spots:
                    # Cannot remove occupied spots
                    occupied_count = Parking_Spot.query.filter_by(lot_id=lot.id, status='occupied').count()
                    if occupied_count > new_total_spots:
                        flash("Cannot reduce total spots below occupied count.", "danger")
                        return redirect(url_for('edit_parking_lot', lot_id=lot.id))

                    # Delete excess available spots
                    excess = old_total_spots - new_total_spots
                    available_spots = (
                        Parking_Spot.query
                        .filter_by(lot_id=lot.id, status='available')
                        .order_by(Parking_Spot.spot_number.desc())
                        .limit(excess)
                        .all()
                    )
                    for spot in available_spots:
                        db.session.delete(spot)

                elif new_total_spots > old_total_spots:
                    # Add new available spots
                    existing_spots = Parking_Spot.query.filter_by(lot_id=lot.id).all()
                    current_spot_count = len(existing_spots)

                    for i in range(current_spot_count + 1, new_total_spots + 1):
                        new_spot = Parking_Spot(
                            lot_id=lot.id,
                            spot_number=str(i),
                            status='available'
                        )
                        db.session.add(new_spot)
                # Recalculate available_spots in the lot
                lot.available_spots = Parking_Spot.query.filter_by(lot_id=lot.id, status='available').count()

                db.session.commit()
                flash('Parking lot updated successfully!', 'success')
                return redirect(url_for('admin_dashboard'))

            except Exception as e:
                db.session.rollback()
                flash(f"Error while updating: {str(e)}", 'danger')

    return render_template('admin/edit_parking_lot.html', form=form, lot=lot, **nav_data)

def Delete_Parking_Lot(lot_id):
    lot = Parking_Lots.query.get_or_404(lot_id)

    try:
        occupied_count = Parking_Spot.query.filter_by(lot_id=lot.id, status='occupied').count()
        if occupied_count > 0:
            flash("Cannot delete lot with occupied spots.", "danger")
            return redirect(url_for('admin_dashboard'))

        Parking_Spot.query.filter_by(lot_id=lot.id).delete()

        db.session.delete(lot)
        db.session.commit()
        flash('Parking lot deleted successfully!', 'success')

    except Exception as e:
        db.session.rollback()
        flash(f"Error while deleting: {str(e)}", 'danger')

    return redirect(url_for('admin_dashboard'))

def Admin_User_View():
    users = User.query.filter(User.role != 'admin').all()
    user_data = []

    for user in users:
        active_reservations = Reservation.query.filter_by(user_id=user.id, status='active').all()
        spots_info = []
        for res in active_reservations:
            lot_name = Parking_Lots.query.get(res.spot.lot_id).location_name
            spot_number = res.spot.spot_number
            spots_info.append(f"Spot : {spot_number}, Lot: {lot_name}")
        

        user_data.append({
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'address': user.address,
            'pin_code': user.pin_code,
            'spots':  spots_info
        })  
    nav_data = {
        'page_title': 'Admin Users',
        'site_title': {'name': 'My Park Place', 'url': Home_Url, 'active': False},
        'nav_items': [
            {'text': 'Home', 'url': Admin_Home_Url, 'active': False},
            {'text': 'Users', 'url': Admin_Users_Url, 'active': True},
            {'text': 'Summary', 'url': Admin_Summary_Url, 'active': False}
        ],
        'logout': True
    }
    
    return render_template('admin/users.html', users=user_data, **nav_data)

def View_Spot(spot_id):
    spot = Parking_Spot.query.get_or_404(spot_id)
    if spot.status == 'occupied':
        reservation = Reservation.query.filter_by(spot_id=spot.id, status='active').first()
    else:
        reservation = None
    nav_data = {
        'page_title': f'View Spot {spot.spot_number}',
        'site_title': {'name': 'My Park Place', 'url': Home_Url, 'active': False},
        'nav_items': [
            {'text': 'Home', 'url': Admin_Home_Url, 'active': False},
            {'text': 'Users', 'url': Admin_Users_Url, 'active': False},
            {'text': 'Summary', 'url':Admin_Summary_Url, 'active': False}
        ],
        'logout': True
    }
    return render_template('admin/view_spot.html', spot=spot, reservation=reservation, **nav_data)

def Delete_Spot(spot_id):
    spot = Parking_Spot.query.get_or_404(spot_id)
    
    if spot.status == 'available':
        lot = Parking_Lots.query.get(spot.lot_id)
        db.session.delete(spot)
        
        if lot.total_spots > 0:
            lot.total_spots -= 1

        db.session.commit()
        flash('Spot deleted successfully and lot updated.', 'success')
    else:
        flash('Cannot delete an occupied spot.', 'danger')
    
    return redirect(url_for('admin_dashboard'))

def View_Parking_Lot(lot_id):
    lot = Parking_Lots.query.get_or_404(lot_id)
    
    nav_data = {
        'page_title': f'View Parking Lot {lot.location_name}',
        'site_title': {'name': 'My Park Place', 'url': Home_Url, 'active': False},
        'nav_items': [
            {'text': 'Home', 'url': Admin_Home_Url, 'active': False},
            {'text': 'Users', 'url': Admin_Users_Url, 'active': False},
            {'text': 'Summary', 'url': Admin_Summary_Url, 'active': False}
        ],
        'logout': True
    }

    return render_template(
        'admin/view_parking_lot.html',lot=lot,**nav_data)

def Admin_Summary():
    
    available = Parking_Spot.query.filter_by(status='available').count()
    occupied = Parking_Spot.query.filter_by(status='occupied').count()
    total = available + occupied

    bar_chart = None
    if total > 0:
        # Bar Chart for Spot Availability
        fig1, ax1 = plt.subplots()
        ax1.bar(['Available', 'Occupied'], [available, occupied], color=['green', 'red'])
        ax1.set_ylabel('Spots')
        io_bar = io.BytesIO()
        plt.savefig(io_bar, format='png')
        io_bar.seek(0)
        bar_chart = base64.b64encode(io_bar.read()).decode('utf8')
        plt.close(fig1)

    # pie chart
    lots = Parking_Lots.query.all()
    revenue_data = {}
    for lot in lots:
        reservations = Reservation.query.join(Parking_Spot).filter(
            Parking_Spot.lot_id == lot.id,
            Reservation.status == 'completed'
        ).all()
        total_amount = sum(r.total_amount for r in reservations)
        if total_amount > 0:
            revenue_data[lot.location_name] = total_amount

    pie_chart = None
    if revenue_data:
        fig2, ax2 = plt.subplots()
        ax2.pie(revenue_data.values(), labels=revenue_data.keys(), autopct='%1.1f%%', startangle=90)
        ax2.axis('equal')
        io_pie = io.BytesIO()
        plt.savefig(io_pie, format='png')
        io_pie.seek(0)
        pie_chart = base64.b64encode(io_pie.read()).decode('utf8')
        plt.close(fig2)

    nav_data = {
        'page_title': 'Admin Summary',
        'site_title': {'name': 'My Park Place', 'url': Home_Url, 'active': False},
        'nav_items': [    
            {'text': 'Home', 'url': Admin_Home_Url, 'active': False},
            {'text': 'Users', 'url': Admin_Users_Url, 'active': False},
            {'text': 'Summary', 'url': Admin_Summary_Url, 'active': True}
        ],
        'logout': True        
    }

    return render_template('admin/summary.html',
                           available=available,
                           occupied=occupied,
                           bar_chart=bar_chart,
                           pie_chart=pie_chart,
                           **nav_data)
