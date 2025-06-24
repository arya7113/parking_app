from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from enum import Enum
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(50),unique=True, nullable=False)
    email = db.Column(db.String(30),unique=True,nullable=False)
    password = db.Column(db.String(255),nullable=False)
    name = db.Column(db.String(50),nullable=False)
    phone_number = db.Column(db.Integer(), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    pin_code = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime(), default=db.func.current_timestamp(), nullable=False)
    role = db.Column(db.Enum('admin', 'user'),default='user', nullable=False)

    def set_password(self, password):   
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'name': self.name,
            'phone_number': self.phone_number,
            'address': self.address,
            'pin_code': self.pin_code,
            'created_at': self.created_at,
            'role': self.role
        }

class Parking_Lots(db.Model):
    __tablename__ = 'parking_lots' 
    id = db.Column(db.Integer(), primary_key=True)
    location_name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    pin_code = db.Column(db.String(10), nullable=False)
    total_spots = db.Column(db.Integer(), nullable=False)
    available_spots = db.Column(db.Integer(), nullable=False)
    price_per_hour = db.Column(db.Float(), nullable=False)
    is_active = db.Column(db.Boolean(), default=True, nullable=False)

class Parking_Spot(db.Model):
    __tablename__ = 'parking_spot'
    id = db.Column(db.Integer(), primary_key=True)
    lot_id = db.Column(db.Integer(), db.ForeignKey('parking_lots.id'), nullable=False)
    spot_number = db.Column(db.String(10), nullable=False)
    status = db.Column(db.Enum('available', 'occupied'), default='available', nullable=False)
    parking_lot = db.relationship('Parking_Lots', backref=db.backref('spots', lazy=True))

class Reservation(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    spot_id = db.Column(db.Integer(), db.ForeignKey('parking_spot.id'), nullable=False)
    vehicle_number = db.Column(db.String(15), nullable=False)
    parking_in_time = db.Column(db.DateTime(), nullable=False)
    parking_out_time = db.Column(db.DateTime(), nullable=False)
    total_amount = db.Column(db.Float(), nullable=False)
    status = db.Column(db.Enum('active', 'completed', 'cancelled'), default='active', nullable=False)
    user = db.relationship('User', backref=db.backref('reservations', lazy=True))
    spot = db.relationship('Parking_Spot', backref=db.backref('reservations', lazy=True))