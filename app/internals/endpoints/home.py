from app.internals.endpoints.__init__ import *
from app.internals.endpoints.auth.form import *
from app.internals.models.model import *


@app.route(Home_Url, methods=['GET'])
def home():
    nav_data = {
        'page_title': 'Home',
        'site_title': {'name': 'My Park Place', 'url': Home_Url, 'active': True},
        'nav_items': [
            {'text': 'Home', 'url': Home_Url, 'active': True},
            {'text': 'Register', 'url':Register_Url, 'active': False},
            {'text': 'Login', 'url': Login_Url, 'active': False}
        ],
        'logout': False
        
    }

    return render_template('home.html', **nav_data) 


