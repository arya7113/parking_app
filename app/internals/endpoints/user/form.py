from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField    
from wtforms.validators import DataRequired, Email

class ReleaseSpotForm(FlaskForm):
    spot_id = StringField('Spot ID', validators=[DataRequired()])
    vehicle_number = StringField('Vehicle Number', validators=[DataRequired()])
    parking_in_time = StringField('Parking Time', validators=[DataRequired()])
    parking_out_time = StringField('Release Time', validators=[DataRequired()])
    total_cost = StringField('Total cost', validators=[DataRequired()])
    submit = SubmitField('Release Spot')
    
class BookSpotForm(FlaskForm):
    spot_id = StringField('Spot ID', render_kw={'readonly': True})
    lot_id = StringField('Lot ID', render_kw={'readonly': True})
    user_id = StringField('User ID', render_kw={'readonly': True})
    parking_in_time = StringField('Parking Time', render_kw={'readonly': True})
    vehicle_number = StringField('Vehicle Number', validators=[DataRequired()])
    submit = SubmitField('Reserve Spot')