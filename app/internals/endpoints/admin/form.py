from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField    
from wtforms.validators import DataRequired, Email

class AddParkingLotForm(FlaskForm):
    location_name = StringField('Location Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    pin_code = StringField('Pin Code', validators=[DataRequired()])
    total_spots = StringField('Total Spots', validators=[DataRequired()])
    price_per_hour = StringField('Price Per Hour', validators=[DataRequired()])
    submit = SubmitField('Add Parking Lot')

class EditParkingLotForm(FlaskForm):
    location_name = StringField('Location Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    pin_code = StringField('Pin Code', validators=[DataRequired()])
    total_spots = StringField('Total Spots', validators=[DataRequired()])
    price_per_hour = StringField('Price Per Hour', validators=[DataRequired()])
    submit = SubmitField('Update')