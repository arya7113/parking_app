from datetime import timedelta
from flask import make_response
from app.internals.endpoints.__init__ import *
from app.internals.models.model import *
from flask_jwt_extended import jwt_required, create_access_token, current_user
from app.internals.endpoints.auth.form import *


@app.route('/user', methods=['GET'])
@jwt_required()
def user():
    user = current_user
    if user.role != 'user':
        flash("You do not have permission to access this page", "danger")
        return redirect(url_for('admin'))
    nav_data = {
        'page_title': 'User Profile',
        'site_title': {'name': 'My Park Place', 'url': Home_Url, 'active': False},
        'nav_items': [
            {'text': 'Home', 'url': Home_Url, 'active': False},
            {'text': 'Register', 'url': Register_Url, 'active': False},
            {'text': 'Login', 'url': Login_Url, 'active': False}
        ],
        'logout': True
    }
    return render_template('user/user.html', user=current_user, **nav_data, 
                           access_token=request.cookies.get('access_token'))
