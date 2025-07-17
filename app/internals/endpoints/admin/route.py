from app.internals.endpoints.admin.view import *
from app.internals.dals.access import *
from app.internals.endpoints.__init__ import *
from app.internals.models.model import *
from flask_jwt_extended import jwt_required, create_access_token, current_user
from app.internals.endpoints.auth.form import *
from app.internals.endpoints.admin.form import *

@app.route('/admin/dashboard', methods=['GET'])
@jwt_required()
@role_required('admin')
def admin_dashboard():
    return Admin_Dashboard()


@app.route('/admin/add_lot', methods=['GET', 'POST'])
@jwt_required()
@role_required('admin')
def add_parking_lot():
    return Add_Parking_Lot()

@app.route('/admin/edit_lot/<int:lot_id>', methods=['GET', 'POST'])
@jwt_required()
@role_required('admin')
def edit_parking_lot(lot_id):
    return Edit_Parking_Lot(lot_id)

@app.route('/admin/delete_lot/<int:lot_id>', methods=['POST'])
@jwt_required()
@role_required('admin')
def delete_parking_lot(lot_id):
    return Delete_Parking_Lot(lot_id)

@app.route('/admin/users', methods=['GET'])
@jwt_required()
@role_required('admin')
def admin_users_view():
    return Admin_User_View()

@app.route('/admin/spot/<int:spot_id>', methods=['GET'])
@jwt_required()
@role_required('admin')
def view_spot(spot_id):
    return View_Spot(spot_id)

@app.route('/admin/delete_spot/<int:spot_id>', methods=['POST'])
@jwt_required()
@role_required('admin')
def delete_spot(spot_id):
    return Delete_Spot(spot_id)

@app.route('/admin/view_lot/<int:lot_id>', methods=['GET'])
@jwt_required()
@role_required('admin')
def view_parking_lot(lot_id):
    return View_Parking_Lot(lot_id)

@app.route('/admin/summary')
@jwt_required()
@role_required('admin')
def admin_summary():
    return Admin_Summary()