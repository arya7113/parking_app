from flask_jwt_extended import JWTManager
from app.internals.models.model import *

jwt = JWTManager()

# @jwt.user_identity_loader
# def load(user):
#     return user.username

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return db.session.query(User).filter_by(username=identity).one_or_none()

