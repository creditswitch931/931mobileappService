from wtforms import Form, validators, Field
from wtforms.fields import (BooleanField, StringField, 
                            TextField, SubmitField, DateField, 
                            IntegerField, TextAreaField, SelectField,
                            HiddenField, DateTimeField, PasswordField, FileField)
from wtforms.validators import Email, Length, ValidationError

from wtforms import form, validators, fields
from wtforms.form import Form

from applib.forms import is_required
from applib import model as m 



class LoginForm(Form):

    usr_name = StringField("Username", [is_required()], 
                            render_kw={"class_": "form-control"})

    psd_wrd = PasswordField("Password", [is_required()],
                            render_kw={"class_": "form-control"})
         


class Service(Form):
    
    name = StringField("Name", [is_required()], 
                            render_kw={"class_": "form-control"})
    label = StringField("Label", [is_required()], 
                            render_kw={"class_": "form-control"})
    image = FileField('Service Image', [], 
                            render_kw={"class_": "form-control"})
    
    category_name = StringField("Category Name", [is_required()], 
                                render_kw={'class_': "form-control"})

    active = BooleanField("Active", [], default=False)


class ServiceItem(Form):

    name = StringField("Name", [is_required()], 
                       render_kw={'class_': "form-control"})

    label = StringField("Label", [is_required()], 
                        render_kw={"class_": "form-control"})
    label_desc = StringField("Label Description", [is_required()],
                              render_kw={'class_': "form-control"}
                             )

    image = FileField('Menu Icon', [], 
                      render_kw={"class_": "form-control"})

    service_id = SelectField("Service", [is_required()], 
                            choices=[(0, 'Select Service')],
                            render_kw={"class_": "form-control"}, 
                            coerce=int)

    active = BooleanField("Active") 



class ServicePlan(Form):

    code =StringField("Item", [is_required()], 
                      render_kw={'class_': "form-control"})
    label = StringField("Label", [is_required()], render_kw={'class_': "form-control"})
    group_name = StringField("Group Name", [is_required()], render_kw={'class_': "form-control"})
    service_id = SelectField("Service Item", [is_required()], choices=[(0, 'Select ServiceItem')],
                             coerce=int, render_kw={"class_": "form-control"})

    extra_field = StringField('Extra Field', [is_required()],
                    render_kw={'class_':'form-control'}
                  )
