from flask_jwt_extended import JWTManager, get_jwt_identity, get_jwt
from app.internals.models.model import *
from functools import wraps
from flask import redirect, url_for, flash


jwt = JWTManager()

# @jwt.user_identity_loader
# def load(user):
#     return user.username

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return db.session.query(User).filter_by(username=identity).one_or_none()


def role_required(required_role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            role = claims.get("role", None)
            if role != required_role:
                flash("You do not have permission.", "danger")
                return redirect(url_for("login"))
            return fn(*args, **kwargs)
        return wrapper
    return decorator

