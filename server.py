from flask import Flask
from flask_bootstrap import Bootstrap
from app.internals.models.model import *
from app.internals.models.model_func import create_Admin
from app.internals.config import *
from app.internals.dals.access import jwt

#all the models
def create_app():
    app = Flask(__name__, template_folder="app/templates")
    bootstrap = Bootstrap(app)  
    app.debug = True
    app.config.from_object(LocalDevlopmentConfig)
    db.init_app(app)
    jwt.init_app(app)
    app.app_context().push()
    return app

app = create_app()

def initialize_db():
    with app.app_context():
        db.create_all()
    db.session.commit()

#routes
from app.internals.endpoints.home import *
from app.internals.endpoints.auth.route import *
from app.internals.endpoints.admin.route import *
from app.internals.endpoints.user.route import *    


if __name__ == '__main__':
    initialize_db()
    admin_exists = User.query.filter_by(role='admin').first()
    if not admin_exists:
        try:
            create_Admin()
            print("Admin created successfully!")
        except Exception as e:
            print(f"Error creating admin: {e}")
    app.run()