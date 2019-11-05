
from wtforms import (Form, Field, BooleanField, StringField, 
                     validators, PasswordField, SelectField,
                     IntegerField, ValidationError, HiddenField)

from wtforms.validators import Email, Length, ValidationError


def check_zero_sign():

    def negative(form, field):
        if not field.data:
            raise ValidationError('field is required')
        if float(field.data) < 1:
            raise ValidationError("less than or eq 0 not allowed.")
    return negative


def number_check():

    def check_numeric(form, field):
        if not str(field.data).isdigit():
            raise ValidationError("numeric values only.")
    return check_numeric

def validate_phone():

    def check_format(form, field):
        
        if not field.data:
            raise ValidationError('field is required')

        if len(field.data) < 11 or len(field.data) > 11:
            raise ValidationError("should be 11 digits only.")
        
        # revisit this function to ensure that the phone number is properly validated 

    return check_format



def alphanum_check():

    def check_alphanumeric(form, field):
        if not field.data:
            raise ValidationError('field is required')
            
        if not str(field.data).isalnum():
            raise ValidationError("valid input required.")
    return check_alphanumeric


def is_required():

    def check_required(form, field):
        if not field.data:
            raise ValidationError("field is required.")

    return check_required


class RegistrationForm(Form):    
    first_name = StringField("First Name")
    last_name = StringField("Last Name")
    email = StringField('Email Address', [Email("invalid email address")])
    phone = IntegerField('Phone', [is_required()])
    mac_address = StringField('Mac Address', [])
    password = PasswordField('Password', [
                                            validators.EqualTo(
                                            'password_confirmation', 
                                            "both passwords must match")])

    password_confirmation = PasswordField("Confirm Password")


    
class LoginForm(Form):     
    username = StringField('Username', [is_required()])
    password = PasswordField('Password', [is_required()])
    mac_address = StringField("Mac Address")

    

class ForgotForm(Form):
    email = StringField("Email or Phone", [validators.Email()]) # custom validaton 
    


class Airtime(Form):
    amount = IntegerField('Enter amount', [is_required(), check_zero_sign()])
    phone = IntegerField('Phone Number', [is_required(), number_check(), validate_phone()])
    


class ElectricityValidate(Form):
    meterNumber = IntegerField("Meter Number", [is_required(), number_check()])    


class IkejaPrePaid(Form):
    customerDtNumber = HiddenField('CustomerDtNumber')
    customerAccountType = HiddenField("customerAccountType")
    providerRef = HiddenField('ProviderRef No')
    meterNumber = StringField('Meter Number', [is_required(), number_check()])
    name = StringField('Name', [is_required()])
    address = StringField('Address')
    amount = IntegerField('Amount', [is_required(), check_zero_sign()])
    phone = IntegerField('Phone Number', [is_required(), number_check(), validate_phone()])


class EkoPrePaid(Form):
    customerDtNumber = HiddenField('CustomerDtNumber')
    providerRef = HiddenField('ProviderRef No')
    meterNumber = StringField('Meter Number', [is_required(), number_check()])
    name = StringField('Name', [is_required()])
    address = StringField('Address')
    amount = IntegerField('Amount', [is_required(), check_zero_sign()])
    phone = IntegerField('Phone Number', [is_required(), number_check(), validate_phone()])


class IbadanPrePaid(Form):
    customerDtNumber = HiddenField('CustomerDtNumber')
    providerRef = HiddenField('ProviderRef No')
    name = StringField('Name', [is_required()])
    meterNumber = StringField('Meter Number', [is_required(), number_check()])
    address = StringField('Address')
    amount = IntegerField('Amount', [is_required(), check_zero_sign()])
    phone = IntegerField('Phone Number', [is_required(), number_check(), validate_phone()])


class AbujaPrePaid(Form):
    customerDtNumber = HiddenField('CustomerDtNumber')
    providerRef = HiddenField('ProviderRef No')
    meterNumber = StringField('Meter Number', [is_required(), number_check()])
    name = StringField('Name', [is_required()])
    address = StringField('Address')
    amount = IntegerField('Amount', [is_required(), check_zero_sign()])
    phone = IntegerField('Phone No', [is_required(), number_check(), validate_phone()])


class Data(Form):
    amount = SelectField('Select Plans', [is_required()],                                   
                                  choices=[(None, 'Select Plan'),
                                           ("100", "40MB, 1day"),
                                           ("200", "150MB, 7days"),
                                           ("1000", "1GB, 30days"),
                                           ("4000", "5.5GB, 30days")
                                           ]
                                )
    phone = IntegerField('Phone No', [is_required()])



class ValidateIUC(Form):
    customerNo = IntegerField("Smartcard No", [is_required(), number_check()])


class Startimes(Form):

    customerName = StringField("Customer Name")
    smartCardCode = IntegerField('Smartcard No', [is_required(), number_check()])
    balance = StringField("Balance")
    amount = IntegerField('Amount', [is_required(), check_zero_sign()])    
    phone = IntegerField('Phone', [is_required(), validate_phone()])


class GotvValidation(Form):

    service_plans = SelectField("Select Plan", 
                                [is_required()], 
                                 choices=[(None, 'Select Package'),
                                           ('gotv_value', 'GOtv Value'),
                                           ('gotv_pls', 'GOtv Plus'),
                                           ('gotv_max', 'GOtv Max'),
                                           ('goLite_month', 'GOtv Lite Monthly'),
                                           ('goLite_quarter', 'GOtv Lite Quarterly')
                                    ]
                                )

    smartCardCode = IntegerField('Smartcard No', [is_required(), number_check()])



class Gotv(Form):
    
    productCodes = HiddenField('Product Code')

    customerNo = IntegerField('Smartcard No', [is_required(), number_check()])  
    customerName = StringField("Customer Name")
    amount = IntegerField('Amount', [is_required(), check_zero_sign()])

    invoicePeriod = SelectField("Invoice Period", 
                                [is_required()], coerce=int,
                                choices=[(0, 'Subscription Period'),
                                         (1, 'One Month'), (2, 'Two Months'), 
                                         (3, 'Three Months'), (4, 'Four Months'), 
                                         (5, 'Five Months'), (6, 'Six Months'), 
                                         (7, 'Seven Months'), (8, 'Eight Months'), 
                                         (9, 'Nine Months'), (10, 'Ten Months'), 
                                         (11, 'Eleven Months'), (12, 'Twelve Months'), 
                                        ]
                                )

    phone = IntegerField('Phone No', [is_required()])
    
    

class DstvValidation(Form):

    service_plans = SelectField("Select Plan", 
                                [is_required()], 
                                 choices=[(None, 'Select Package'),
                                    ("PRWE36", "DStv Premium"),
                                    ("PRWASIE36", "DStv Premium Asia"),
                                    ("ASIAE36", "Asian Bouqet"),
                                    ("FTAE36", "DStv FTA Plus")
                                    ]
                                )

    smartCardCode = IntegerField('Smartcard No', [is_required(), number_check()])


class Dstv(Form):
    
    productCodes = HiddenField('Product Code')
    
    customerName = StringField("Customer Name")
    customerNo = IntegerField('Smartcard No', [is_required(), number_check()])
    amount = IntegerField('Amount', [is_required(), check_zero_sign()])    
    invoicePeriod = SelectField("Invoice Period", 
                                [is_required()],
                                choices=[(0, 'Subscription Period'),
                                         (1, 'One Month'), (2, 'Two Months'), 
                                         (3, 'Three Months'), (4, 'Four Months'), 
                                         (5, 'Five Months'), (6, 'Six Months'), 
                                         (7, 'Seven Months'), (8, 'Eight Months'), 
                                         (9, 'Nine Months'), (10, 'Ten Months'), 
                                         (11, 'Eleven Months'), (12, 'Twelve Months'), 
                                        ]
                                )

    phone = IntegerField('Phone No', [is_required()])

    
    
    




