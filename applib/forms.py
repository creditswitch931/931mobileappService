
from wtforms import (Form, Field, BooleanField, StringField, 
                     validators, PasswordField, SelectField,
                     IntegerField, ValidationError)

from wtforms.validators import Email, Length, ValidationError


def check_zero_sign():

    def negative(form, field):
        if float(field.data) < 1:
            raise ValidationError("less than or eq 0 not allowed.")
    return negative


def number_check():

    def check_numeric(form, field):
        if not str(field.data).isdigit():
            raise ValidationError("numeric values only.")
    return check_numeric


def alphanum_check():

    def check_alphanumeric(form, field):
        if not str(field.data).isalnum():
            raise ValidationError("valid input required.")
    return check_alphanumeric


def input_required():

    def check_required(form, field):
        if not field.data:
            raise ValidationError("field is required.")

    return check_required


class RegistrationForm(Form):    
    first_name = StringField("First Name")
    last_name = StringField("Last Name")
    email = StringField('Email Address', [Email("invalid email address")])
    phone = IntegerField('Phone', [input_required()])
    mac_address = StringField('Mac Address', [])
    password = PasswordField('Password', [
                                            validators.EqualTo(
                                            'password_confirmation', 
                                            "both passwords must match")])

    password_confirmation = PasswordField("Confirm Password")

    
class LoginForm(Form):    
     
    username = StringField('Username', [input_required()])
    password = PasswordField('Password', [input_required()])
    mac_address = StringField("Mac Address")

    
class ForgotForm(Form):
    email = StringField("Email or Phone", [validators.Email()]) # custom validaton 
    
    # def validate_email(form, field):
    #     pass


class Airtime(Form):
    select_network = SelectField('Select network', [input_required()], coerce=int,
                                  choices=[(0, 'Select ...'),
                                           (1, 'MTN'),
                                           (2, 'Glo'),
                                           (3, '9mobile'),
                                           (4, 'Airtel')])
    amount = StringField('Enter amount', [input_required(), check_zero_sign()])
    phone = StringField('Phone Number', [input_required()])
    


class Electricity(Form):
    select_disco = SelectField('Select disco', [input_required()], coerce=int,
                                  choices=[(0, 'Select ...'),
                                           (1, 'Ikeja distribution company'),
                                           (2, 'Eko distribution company'),
                                           (3, 'Ibadan distribution company')])
    meter_number = StringField('Enter meter number', [input_required(), number_check()])
    amount = StringField('Enter amount', [input_required(), check_zero_sign()])
    phone = StringField('Phone Number', [input_required()])
    


class Data(Form):
    select_network = SelectField('Select network', [input_required()], 
                                  coerce=int, 
                                  choices=[(0, 'Select ...'),
                                           (1, 'MTN'),
                                           (2, 'Glo'),
                                           (3, '9mobile'),
                                           (4, 'Airtel')])
    amount = StringField('Enter amount', [input_required(), check_zero_sign()])
    phone = StringField('Phone Number', [input_required()])


class Startimes(Form):
    smartcard_number = StringField('Enter smartcard number', 
                                    [input_required(), number_check()])
    amount = StringField('Enter amount', [input_required(), check_zero_sign()])
    phone = StringField('Phone Number', [input_required()])
   

class Gotv(Form):
    select_package = SelectField('Select a package', [input_required()],
                                  choices=[('select', 'Select ...'),
                                           ('gotv_value', 'GOtv Value'),
                                           ('gotv_pls', 'GOtv Plus'),
                                           ('gotv_max', 'GOtv Max'),
                                           ('goLite_month', 'GOtv Lite Monthly'),
                                           ('goLite_quarter', 'GOtv Lite Quarterly')])
    iuc_number = StringField('Enter IUC number', [input_required(), number_check()])
    amount = StringField('Enter amount', [input_required(), check_zero_sign()])
    phone = StringField('Phone Number', [input_required()])
    


class Dstv(Form):
    select_package = SelectField('Select a package', [input_required()],
                                  choices=[('select', 'Select ...'),
                                           ('dstv_access', 'DStv Access'),
                                           ('dstv_family', 'DStv Family'),
                                           ('dstv_compact', 'DStv Compact'),
                                           ('dstv_compact_plus', 'DStv Compact Plus'),
                                           ('dstv_premium', 'DStv Premium'),
                                           ('dstv_premium_asia', 'DStv Premium Asia'),
                                           ('asian_bouqet', 'Asian Bouqet'),
                                           ('dstv_fta_plus', 'DStv FTA Plus')])
    smartcard_number = StringField('Enter smartcard number', [input_required(), number_check()])
    amount = StringField('Enter amount', [input_required(), check_zero_sign()])
    phone = StringField('Phone Number', [input_required()])
    
    




