from app.internals.endpoints.user.view import *
from app.internals.endpoints.__init__ import *
from app.internals.dals.access import role_required
from app.internals.models.model import *
from flask_jwt_extended import jwt_required, create_access_token, current_user
from app.internals.endpoints.auth.form import *


@app.route('/user/dashboard', methods=['GET'])
@jwt_required()
@role_required('user')
def user_dashboard():
    return User_Dashboard()

@app.route('/user/release_spot/<int:reservation_id>', methods=['GET','POST'])
@jwt_required()
@role_required('user')
def release_spot(reservation_id):
    return Release_Spot(reservation_id)

@app.route('/user/book_spot/<int:lot_id>', methods=['GET', 'POST'])
@jwt_required()
@role_required('user')
def book_spot(lot_id):
    return Book_Spot(lot_id)

@app.route('/user/summary', methods=['GET'])
@jwt_required()
@role_required('user')
def user_summary():
    return User_Summary()