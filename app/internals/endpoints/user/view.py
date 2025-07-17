import base64
from datetime import datetime
import io

from matplotlib import pyplot as plt
from app.internals.endpoints.user.view import *
from app.internals.endpoints.__init__ import *
from app.internals.dals.access import role_required
from app.internals.models.model import *
from flask_jwt_extended import jwt_required, create_access_token, current_user
from app.internals.endpoints.user.form import *


def User_Dashboard():
    user_id = get_jwt_identity()

    reservations = (
        Reservation.query.filter_by(user_id=current_user.id)
        .order_by(Reservation.parking_in_time.desc())
        .all())
    lots = Parking_Lots.query.all()
    nav_data = {
        'page_title': 'User Dashboard',
        'site_title': {'name': 'My Park Place', 'url': Home_Url, 'active': False},
        'nav_items': [
            {'text': 'Home', 'url': User_Home_Url, 'active': False},
            {'text': 'Summary', 'url': User_Summary_Url, 'active': False}
        ],
        'logout': True
    }
    return render_template('user/dashboard.html', **nav_data, reservations=reservations,lots=lots, user_id=user_id)

def Book_Spot(lot_id):
    lot = Parking_Lots.query.get_or_404(lot_id)
    spot = Parking_Spot.query.filter_by(lot_id=lot.id, status='available').first()
    form = BookSpotForm()

    if request.method == 'GET':
        form.spot_id.data = str(spot.id)
        form.lot_id.data = str(lot.id)
        form.user_id.data = str(current_user.id)
        form.parking_in_time.data = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if form.validate_on_submit():
        reservation = Reservation(
            spot_id=int(form.spot_id.data),
            user_id=int(form.user_id.data),
            vehicle_number=form.vehicle_number.data,
            parking_in_time=datetime.strptime(form.parking_in_time.data, '%Y-%m-%d %H:%M:%S'),
            parking_out_time=None,  # Set to None initially
            total_amount=0.0,  # Set to 0 initially
            status='active'
        )
        spot.status = 'occupied'
        lot.available_spots -= 1
        db.session.add(spot)
        db.session.add(lot)
        db.session.flush()  # Ensure the spot is updated before adding the reservation
        db.session.add(reservation)
        db.session.commit()
        flash('Spot booked successfully!', 'success')
        return redirect(url_for('user_dashboard'))

    nav_data = {
        'page_title': 'Book Spot',
        'site_title': {'name': 'My Park Place', 'url': Home_Url, 'active': False},
        'nav_items': [
            {'text': 'Home', 'url': User_Home_Url, 'active': False},
            {'text': 'Summary', 'url': User_Summary_Url, 'active': False}
        ],
        'logout': True
    }

    return render_template('user/book_spot.html', form=form, lot=lot, **nav_data)



def Release_Spot(reservation_id):
    reservation = Reservation.query.get_or_404(reservation_id)
    form = ReleaseSpotForm()

    if form.validate_on_submit():
        print("Form submitted successfully")
        
        reservation.status = 'completed'
        reservation.parking_out_time = datetime.now()

        duration = (reservation.parking_out_time - reservation.parking_in_time).total_seconds() / 3600
        reservation.total_amount = round(duration * reservation.spot.parking_lot.price_per_hour, 2)

        reservation.spot.status = 'available'
        db.session.commit()

        flash('Spot released successfully!', 'success')
        return redirect(url_for('user_dashboard'))

    # Prefill the form only on GET
    if request.method == 'GET':
        reservation.parking_out_time = datetime.now()
        duration = (reservation.parking_out_time - reservation.parking_in_time).total_seconds() / 3600
        reservation.total_amount = round(duration * reservation.spot.parking_lot.price_per_hour, 2)

        form.spot_id.data = reservation.spot_id
        form.vehicle_number.data = reservation.vehicle_number
        form.parking_in_time.data = reservation.parking_in_time.strftime('%Y-%m-%d %H:%M:%S')
        form.parking_out_time.data = reservation.parking_out_time.strftime('%Y-%m-%d %H:%M:%S')
        form.total_cost.data = f"{reservation.total_amount:.2f}"

    nav_data = {
        'page_title': 'Release Spot',
        'site_title': {'name': 'My Park Place', 'url': Home_Url, 'active': False},
        'nav_items': [
            {'text': 'Home', 'url': User_Home_Url, 'active': False},
            {'text': 'Summary', 'url': User_Summary_Url, 'active': False}
        ],
        'logout': True
    }

    return render_template('user/release_spot.html', form=form, reservation=reservation, **nav_data)

def User_Summary():
    user_id = current_user.id
    reservations = Reservation.query.filter_by(user_id=user_id, status='completed').all()
    user = User.query.get_or_404(user_id)

    spending_data = {}
    count_data = {}

    for r in reservations:
        if r.total_amount is None:
            continue
        lot_name = r.spot.parking_lot.location_name
        spending_data[lot_name] = spending_data.get(lot_name, 0.0) + r.total_amount
        count_data[lot_name] = count_data.get(lot_name, 0) + 1

    pie_chart = None
    bar_chart = None

    if spending_data:
        # Pie Chart for spending
        pie_labels = list(spending_data.keys())
        pie_values = list(spending_data.values())
        fig1, ax1 = plt.subplots()
        ax1.pie(pie_values, labels=pie_labels, autopct='%1.1f%%', startangle=90)
        ax1.axis('equal')
        pie_io = io.BytesIO()
        plt.savefig(pie_io, format='png')
        pie_io.seek(0)
        pie_chart = base64.b64encode(pie_io.read()).decode('utf8')
        plt.close(fig1)

    if count_data:
        # Bar Chart for reservation count
        bar_labels = list(count_data.keys())
        bar_values = list(count_data.values())
        fig2, ax2 = plt.subplots()
        ax2.bar(bar_labels, bar_values, color='skyblue')
        ax2.set_xlabel('Parking Lot')
        ax2.set_ylabel('Reservations')
        bar_io = io.BytesIO()
        plt.savefig(bar_io, format='png')
        bar_io.seek(0)
        bar_chart = base64.b64encode(bar_io.read()).decode('utf8')
        plt.close(fig2)

    nav_data = {
        'page_title': 'User Summary',
        'site_title': {'name': 'My Park Place', 'url': Home_Url, 'active': False},
        'nav_items': [
            {'text': 'Home', 'url': User_Home_Url, 'active': False},
            {'text': 'Summary', 'url': User_Summary_Url, 'active': True}
        ],
        'logout': True
    }

    return render_template(
        'user/summary.html',
        reservations=reservations,
        user_id=user_id,
        user=user,
        pie_chart=pie_chart,
        bar_chart=bar_chart,
        **nav_data
    )
