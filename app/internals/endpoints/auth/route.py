from datetime import timedelta
from flask import make_response
from app.internals.endpoints.__init__ import *
from app.internals.models.model import *
from flask_jwt_extended import jwt_required, create_access_token, current_user
from app.internals.endpoints.auth.form import *
from app.internals.endpoints.admin.route import *
from app.internals.endpoints.user.route import *


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    nav_data = {
        'page_title': 'Login',
        'site_title': {'name': 'My Park Place', 'url': Home_Url, 'active': False},
        'nav_items': [
            {'text': 'Home', 'url': Home_Url, 'active': False},
            {'text': 'Register', 'url': Register_Url, 'active': False},
            {'text': 'Login', 'url': Login_Url, 'active': True}
        ],
        'logout': False
    }
    if request.method == 'GET':
        return render_template('auth/login.html',form=form,**nav_data)
    
    username = request.form.get('username', None)
    password = request.form.get('password', None)

    user = User.query.filter_by(username=username).one_or_none()
    if not user or not user.check_password(password):
        flash("Wrong username or password", "danger")
        return render_template('auth/login.html',form=form,**nav_data)
    
    access_token = create_access_token(
    identity=user.username,
    additional_claims={
        "id": user.id,
        "role": user.role
    },
    expires_delta=timedelta(hours=1)
    )

    if user.role == 'admin':
        flash("Welcome Admin", "success")
        resp = make_response(redirect(url_for('admin_dashboard')))
    else:
        flash("Welcome User", "success")
        resp = make_response(redirect(url_for('user')))
    resp.set_cookie(
        "access_token",
        access_token,
        httponly=True,   # JavaScript cannot read it (protects from XSS)
        secure=False     # True if using HTTPS
    )
    return resp
    

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    nav_data = {
        'page_title': 'Register',
        'site_title': {'name': 'My Park Place', 'url': Home_Url, 'active': False},
        'nav_items': [
            {'text': 'Home', 'url': Home_Url, 'active': False},
            {'text': 'Register', 'url': Register_Url, 'active': True},
            {'text': 'Login', 'url': Login_Url, 'active': False}
        ],
        'logout': False
    }
    if request.method == "POST":
        if form.validate_on_submit():
            existing_user_username = User.query.filter_by(username=form.username.data).first()
            existing_user_email = User.query.filter_by(email=form.email.data).first()
            
            if existing_user_username:
                flash('Username already exists.')
                return render_template('auth/register.html', form=form, **nav_data)
            
            if existing_user_email:
                flash('Email already exists.')
                return render_template('auth/register.html', form=form, **nav_data)
            
            try:
                new_user = User(
                    username = request.form.get('username', None),
                    email = request.form.get('email', None),
                    password = request.form.get('password', None),
                    name = request.form.get('name', None),
                    phone_number = request.form.get('phone_number', None),
                    address = request.form.get('address', None),
                    pin_code = request.form.get('pin_code', None),
                    role = request.form.get('role', 'user')
                )
                new_user.set_password(new_user.password)
                db.session.add(new_user)
                db.session.commit()
                flash('Registration successful!')
                return redirect(url_for('login'))
            except db.IntegrityError:
                db.session.rollback()
                flash('Database error: Duplicate entry.')
            except Exception as e:
                db.session.rollback()
                flash(f'Error: {str(e)}')
    return render_template('auth/register.html', form=form, **nav_data)



@app.route('/logout', methods=['GET'])
@jwt_required()
def logout():
    resp = make_response(redirect(url_for('login')))
    resp.set_cookie(
        "access_token",
        '',  # Clear the cookie 
        httponly=True,   # JavaScript cannot read it (protects from XSS)
        secure=False,    # True if using HTTPS
        expires=0        # Set expiration to 0 to delete the cookie
    )
    flash("You have been logged out", "success")
    return resp



