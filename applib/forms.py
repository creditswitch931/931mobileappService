
from wtforms import (Form, BooleanField, StringField, 
                     validators, PasswordField, SelectField,
                     IntegerField)


class RegistrationForm(Form):    
    first_name = StringField("First Name")
    last_name = StringField("Last Name")
    email = StringField('Email Address', [validators.Email()])
    phone = IntegerField('Phone', [])
    mac_address = StringField('Mac Address', [])
    password = PasswordField('Password')
    password_confirmation = PasswordField("Confirm Password")

    
class LoginForm(Form):    
     
    username = StringField('Username', [])
    password = PasswordField('Password', [])
    mac_address = PasswordField("Mac Address")

    
class ForgotForm(Form):
    email = StringField("Email or Phone", [validators.Email()]) # custom validaton 
    
    def validate_email(form, field):
        pass
        # if the data has @ symbol in it validata for proper email address 
        # elif the data is an integer field then validate for phone number 

