
from wtforms import (Form, Field, BooleanField, StringField, 
                     validators, PasswordField, SelectField,
                     IntegerField, ValidationError, HiddenField)

from wtforms.validators import Email, Length, ValidationError

from applib import model as m


def check_zero_sign():

    def negative(form, field):
        if float(field.data) < 1:
            raise ValidationError("field must not be less than zero.")

    return negative


def number_check():

    def check_numeric(form, field):
        if not str(field.data).isdigit():
            raise ValidationError("numeric values only.")
    return check_numeric


def validate_phone():

    def check_format(form, field):
        
        item = field.data 

        if item.startswith("234"):
            item = item.replace("234", "0")
            field.data = item
        if len(item) < 11:
            raise ValidationError("phone number digits is less than 11 characters")
                
        if len(item) > 12:
            raise ValidationError("phone number digits is greater than 11 characters ")
        
        # revisit this function to ensure that the phone number is properly validated 

    return check_format



def alphanum_check():

    def check_alphanumeric(form, field):
            
        if not str(field.data).isalnum():
            raise ValidationError("valid input required.")
    return check_alphanumeric


def is_required():

    def check_required(form, field):
        if not field.data:
            raise ValidationError("field is required.")

    return check_required



def field_required(field):

    if field.data is None:
        return False, " Field is required"

    return True, None

def field_alphanum(field):

    if not str(field.data).isalnum():
        return False, " Field is required"

    return True, None


def field_numeric(field):
    if not str(field.data).isdigit():
        return False, " Field should be numeric"

    return True, None


def field_nonzero(field):

    if float(field.data) < 1:
        return False, " Field is less than 1"

    return True, None 


def field_phone(field):

    item = field.data 

    if item.startswith("234"):
        item = item.replace("234", "0")
        field.data = item
    
    if len(item) < 11:
        return False, " Field is less than 11 characters"
            
    if len(item) > 12:
        return False, " Field is greater than 11 characters"


    return True, None 


CHECKERFUNC = {
    "required": field_required,
    "alphanum": field_alphanum,
    "numeric": field_numeric,
    "lessthanzero": field_nonzero,
    "phonefield": field_phone
}


def global_validator(*args):
    
    def run_validation(form, field):
        
        for val in args:
            output = CHECKERFUNC[val](field)

            if not output[0]:
                raise ValidationError(field.label.text + output[1])
                break


    return run_validation

class BaseForm(Form):
    __readonlyfields__ = []
    def init_func(self):
        pass


class RegistrationForm(BaseForm):    
    first_name = StringField("First Name", [global_validator("required")])
    last_name = StringField("Last Name", [global_validator("required")])
    email = StringField('Email Address', [is_required(), Email("invalid email address")])
    phone = IntegerField('Phone', [global_validator("required", "numeric", "phonefield")])
    mac_address = StringField('Mac Address')
    password = PasswordField('Password', [is_required(),
                                            validators.EqualTo(
                                            'password_confirmation', 
                                            "both passwords must match"),
                                            Length(min=6)])

    password_confirmation = PasswordField("Confirm Password", [global_validator("required")])


    
class LoginForm(BaseForm):     
    username = StringField('Username', [global_validator("required")])
    password = PasswordField('Password', [global_validator("required")])
    mac_address = StringField("Mac Address")
    code = StringField("Code")
    

class ForgotForm(BaseForm):
    email = StringField("Email or Phone", [validators.Email()]) # custom validaton 
    


class Airtime(BaseForm):
    # number_check()
    amount = IntegerField('Amount', [global_validator("required", "numeric", "lessthanzero")])
    phone = IntegerField('Phone No', [global_validator("required", "numeric", "phonefield")]) 
    


class ElectricityValidate(BaseForm):
    meterNumber = IntegerField("Meter Number", [global_validator("required", "numeric")])    


class IkejaPrePaid(BaseForm):
    __readonlyfields__ = ["customerDtNumber", "name", 
                         "address", "meterNumber", "customerAccountType",
                         "providerRef"]
    customerDtNumber = HiddenField('CustomerDtNumber')
    customerAccountType = HiddenField("customerAccountType")
    providerRef = HiddenField('ProviderRef No')
    meterNumber = StringField('Meter Number', [global_validator("required", "numeric")]) 
    name = StringField('Name', [global_validator("required")])
    address = StringField('Address')
    amount = IntegerField('Amount', [global_validator("required", "numeric", "lessthanzero")])
    phone = IntegerField('Phone No', [global_validator("required", "numeric", "phonefield")])


class EkoPrePaid(BaseForm):
    __readonlyfields__ = ["customerDtNumber", "name", 
                         "address", "meterNumber", "customerAccountType",
                         "providerRef"]

    customerDtNumber = HiddenField('CustomerDtNumber')
    providerRef = HiddenField('ProviderRef No')
    meterNumber = StringField('Meter Number', [global_validator("required", "numeric")])
    name = StringField('Name', [global_validator("required")])
    address = StringField('Address')
    amount = IntegerField('Amount', [global_validator("required", "numeric", "lessthanzero")])
    phone = IntegerField('Phone No',  [global_validator("required", "numeric", "phonefield")])


class IbadanPrePaid(BaseForm):
    __readonlyfields__ = ["customerDtNumber", "name", 
                         "address", "meterNumber", "customerAccountType",
                         "providerRef"]
    customerDtNumber = HiddenField('CustomerDtNumber')
    providerRef = HiddenField('ProviderRef No')
    name = StringField('Name', [global_validator("required")])
    meterNumber = StringField('Meter Number',  [global_validator("required", "numeric")])
    address = StringField('Address')
    amount = IntegerField('Amount', [global_validator("required", "numeric", "lessthanzero")])
    phone = IntegerField('Phone No', [global_validator("required", "numeric", "phonefield")])


class AbujaPrePaid(BaseForm):
    __readonlyfields__ = ["customerDtNumber", "name", 
                         "address", "meterNumber", "customerAccountType",
                         "providerRef"]
    customerDtNumber = HiddenField('CustomerDtNumber')
    providerRef = HiddenField('ProviderRef No')
    meterNumber = StringField('Meter Number', [global_validator("required", "numeric")])
    name = StringField('Name', [global_validator("required")])
    address = StringField('Address')
    amount = IntegerField('Amount',[global_validator("required", "numeric", "lessthanzero")])
    phone = IntegerField('Phone No', [global_validator("required", "numeric", "phonefield")])


class Data(BaseForm):
    amount = SelectField('Select Plans', [global_validator("required")],
                         choices=[(None, 'Select Plan')]
                        )

    phone = IntegerField('Phone No', [global_validator("required", "numeric", "phonefield")])


class MtnData(Data):
    def init_func(self):
        self.amount.choices = self.amount.choices + m.ServicePlan.get_choices("mtnplan")

class AirtelData(Data):
    def init_func(self):
        self.amount.choices = self.amount.choices + m.ServicePlan.get_choices("airtelplan")

class GloData(Data):
    def init_func(self):
        self.amount.choices = self.amount.choices + m.ServicePlan.get_choices("gloplan")

class NMobileData(Data):
    def init_func(self):
        self.amount.choices = self.amount.choices + m.ServicePlan.get_choices("ninemobileplan")


class ValidateIUC(BaseForm):
    customerNo = IntegerField("Smartcard No", [global_validator("required", "numeric")])


class Startimes(BaseForm):
    __readonlyfields__ = ["customerName", 'balance', "smartCardCode"]
    customerName = StringField("Customer Name")
    smartCardCode = IntegerField('Smartcard No', [global_validator("required", "numeric")])
    balance = StringField("Balance")
    amount = IntegerField('Amount', [global_validator("required", "numeric", "lessthanzero")])
    phone = IntegerField('Phone No',[global_validator("required", "numeric", "phonefield")])


class GotvValidation(BaseForm):

    service_plans = SelectField("Select Plan", 
                                [global_validator("required")], 
                                 choices=[(None, 'Select Package')]
                                )

    smartCardCode = IntegerField('Smartcard No', [global_validator("required", "numeric")])

    def init_func(self):        
        self.service_plans.choices = self.service_plans.choices + m.ServicePlan.get_choices("gotvplan")
 


class Gotv(BaseForm):
    __readonlyfields__ = ["amount", "customerNo", "customerName" ]
    productCodes = HiddenField('Product Code')

    customerNo = IntegerField('Smartcard No', [global_validator("required", "numeric")])  
    customerName = StringField("Customer Name")
    amount = IntegerField('Amount',  [global_validator("required", "numeric", "lessthanzero")])

    invoicePeriod = SelectField("Invoice Period", 
                                [global_validator("required")], coerce=int,
                                choices=[(0, 'Subscription Period'),
                                         (1, 'One Month'), (2, 'Two Months'), 
                                         (3, 'Three Months'), (4, 'Four Months'), 
                                         (5, 'Five Months'), (6, 'Six Months'), 
                                         (7, 'Seven Months'), (8, 'Eight Months'), 
                                         (9, 'Nine Months'), (10, 'Ten Months'), 
                                         (11, 'Twelve Months'), 
                                        ]
                                )

    phone = IntegerField('Phone No', [global_validator("required", "numeric", "phonefield")])
    
    

class DstvValidation(BaseForm):

    service_plans = SelectField("Select Plan", 
                                [global_validator("required")], 
                                 choices=[(None, 'Select Package')]
                                )

    smartCardCode = IntegerField('Smartcard No', [global_validator("required", "numeric")])

    def init_func(self):        
        self.service_plans.choices = self.service_plans.choices + m.ServicePlan.get_choices("dstvpackage")
 

    

class Dstv(BaseForm):
    __readonlyfields__ = ["amount", "customerNo", "customerName" ]
    
    productCodes = HiddenField('Product Code')
    
    customerName = StringField("Customer Name")
    customerNo = IntegerField('Smartcard No', [global_validator("required", "numeric")])
    amount = IntegerField('Amount', [global_validator("required", "numeric", "lessthanzero")])
    invoicePeriod = SelectField("Invoice Period", 
                                [global_validator("required")], coerce=int,
                                choices=[(0, 'Subscription Period'),
                                         (1, 'One Month'), (2, 'Two Months'), 
                                         (3, 'Three Months'), (4, 'Four Months'), 
                                         (5, 'Five Months'), (6, 'Six Months'), 
                                         (7, 'Seven Months'), (8, 'Eight Months'), 
                                         (9, 'Nine Months'), (10, 'Ten Months'), 
                                         (11, 'Twelve Months'), 
                                        ]
                                )

    phone = IntegerField('Phone No', [global_validator("required", "numeric", "phonefield")])
    




