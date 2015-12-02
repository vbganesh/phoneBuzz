from flask.ext.wtf import Form
from wtforms_components import PhoneNumberField
from wtforms.validators import InputRequired

class PhoneNumberForm(Form):
    number = PhoneNumberField(country_code='US', display_format='E164', validators=[InputRequired()])
