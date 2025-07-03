from app.internals.models.model import *
from datetime import datetime
from app.internals.endpoints.__init__ import *  


def create_Admin():
    # Creating dummy admin 
    user_instance = User(
        username='admin',
        email='admin@goat.com',
        password=generate_password_hash('admin123'),
        name= 'Admin',
        phone_number=1234567890,
        address='Admin Address',
        pin_code=123456,
        role='admin',
        created_at=datetime.now()
    )
    db.session.add(user_instance)
    db.session.commit()