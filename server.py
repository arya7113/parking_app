from flask import Flask
from flask_bootstrap import Bootstrap
from app.internals.models.model import *

#all the models
def create_app():
    app = Flask(__name__, template_folder="app/templates")
    bootstrap = Bootstrap(app)  
    app.debug = True
    app.config['SECRET_KEY'] = 'secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parkingapp.sqlite3'
    db.init_app(app)
    app.app_context().push()
    return app

app = create_app()

def initialize_db():
    with app.app_context():
        db.create_all()
    db.session.commit()


if __name__ == '__main__':
    initialize_db()
    app.run(debug=True)