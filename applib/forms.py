
from wtforms import (Form, Field, BooleanField, StringField, 
                     validators, PasswordField, SelectField,
                     IntegerField, ValidationError, HiddenField)

from wtforms.validators import Email, Length, ValidationError

from applib import model as m


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


class BaseForm(Form):

    def init_func(self):
        pass


class RegistrationForm(BaseForm):    
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


    
class LoginForm(BaseForm):     
    username = StringField('Username', [is_required()])
    password = PasswordField('Password', [is_required()])
    mac_address = StringField("Mac Address")

    

class ForgotForm(BaseForm):
    email = StringField("Email or Phone", [validators.Email()]) # custom validaton 
    


class Airtime(BaseForm):
    amount = IntegerField('Enter amount', [is_required(), check_zero_sign()])
    phone = IntegerField('Phone Number', [is_required(), number_check(), validate_phone()])
    


class ElectricityValidate(BaseForm):
    meterNumber = IntegerField("Meter Number", [is_required(), number_check()])    


class IkejaPrePaid(BaseForm):
    customerDtNumber = HiddenField('CustomerDtNumber')
    customerAccountType = HiddenField("customerAccountType")
    providerRef = HiddenField('ProviderRef No')
    meterNumber = StringField('Meter Number', [is_required(), number_check()])
    name = StringField('Name', [is_required()])
    address = StringField('Address')
    amount = IntegerField('Amount', [is_required(), check_zero_sign()])
    phone = IntegerField('Phone Number', [is_required(), number_check(), validate_phone()])


class EkoPrePaid(BaseForm):
    customerDtNumber = HiddenField('CustomerDtNumber')
    providerRef = HiddenField('ProviderRef No')
    meterNumber = StringField('Meter Number', [is_required(), number_check()])
    name = StringField('Name', [is_required()])
    address = StringField('Address')
    amount = IntegerField('Amount', [is_required(), check_zero_sign()])
    phone = IntegerField('Phone Number', [is_required(), number_check(), validate_phone()])


class IbadanPrePaid(BaseForm):
    customerDtNumber = HiddenField('CustomerDtNumber')
    providerRef = HiddenField('ProviderRef No')
    name = StringField('Name', [is_required()])
    meterNumber = StringField('Meter Number', [is_required(), number_check()])
    address = StringField('Address')
    amount = IntegerField('Amount', [is_required(), check_zero_sign()])
    phone = IntegerField('Phone Number', [is_required(), number_check(), validate_phone()])


class AbujaPrePaid(BaseForm):
    customerDtNumber = HiddenField('CustomerDtNumber')
    providerRef = HiddenField('ProviderRef No')
    meterNumber = StringField('Meter Number', [is_required(), number_check()])
    name = StringField('Name', [is_required()])
    address = StringField('Address')
    amount = IntegerField('Amount', [is_required(), check_zero_sign()])
    phone = IntegerField('Phone No', [is_required(), number_check(), validate_phone()])


class Data(BaseForm):
    amount = SelectField('Select Plans', [is_required()],                                   
                         choices=[(None, 'Select Plan')]
                        )

    phone = IntegerField('Phone No', [is_required()])


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
    customerNo = IntegerField("Smartcard No", [is_required(), number_check()])


class Startimes(BaseForm):

    customerName = StringField("Customer Name")
    smartCardCode = IntegerField('Smartcard No', [is_required(), number_check()])
    balance = StringField("Balance")
    amount = IntegerField('Amount', [is_required(), check_zero_sign()])    
    phone = IntegerField('Phone', [is_required(), validate_phone()])


class GotvValidation(BaseForm):

    service_plans = SelectField("Select Plan", 
                                [is_required()], 
                                 choices=[(None, 'Select Package')]
                                )

    smartCardCode = IntegerField('Smartcard No', [is_required(), number_check()])

    def init_func(self):        
        self.service_plans.choices = self.service_plans.choices + m.ServicePlan.get_choices("gotvplan")
 


class Gotv(BaseForm):
    
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
                                         (11, 'Twelve Months'), 
                                        ]
                                )

    phone = IntegerField('Phone No', [is_required()])
    
    

class DstvValidation(BaseForm):

    service_plans = SelectField("Select Plan", 
                                [is_required()], 
                                 choices=[(None, 'Select Package')]
                                )

    smartCardCode = IntegerField('Smartcard No', [is_required(), number_check()])

    def init_func(self):        
        self.service_plans.choices = self.service_plans.choices + m.ServicePlan.get_choices("dstvpackage")
 

    

class Dstv(BaseForm):
    
    productCodes = HiddenField('Product Code')
    
    customerName = StringField("Customer Name")
    customerNo = IntegerField('Smartcard No', [is_required(), number_check()])
    amount = IntegerField('Amount', [is_required(), check_zero_sign()])    
    invoicePeriod = SelectField("Invoice Period", 
                                [is_required()], coerce=int,
                                choices=[(0, 'Subscription Period'),
                                         (1, 'One Month'), (2, 'Two Months'), 
                                         (3, 'Three Months'), (4, 'Four Months'), 
                                         (5, 'Five Months'), (6, 'Six Months'), 
                                         (7, 'Seven Months'), (8, 'Eight Months'), 
                                         (9, 'Nine Months'), (10, 'Ten Months'), 
                                         (11, 'Twelve Months'), 
                                        ]
                                )

    phone = IntegerField('Phone No', [is_required()])

    
    
    




