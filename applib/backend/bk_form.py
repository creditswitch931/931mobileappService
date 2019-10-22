from wtforms import Form, validators, Field
from wtforms.fields import (BooleanField, StringField, 
							TextField, SubmitField, DateField, 
							IntegerField, TextAreaField, SelectField,
							HiddenField, DateTimeField, PasswordField, FileField)
from wtforms.validators import input_required, Email, Length, ValidationError

from wtforms import form, validators, fields
from wtforms.form import Form


# def input_required():

# 	def check_required(form, field):
# 		if not field.data:
# 			raise ValidationError("field is required.")

# 	return check_required



class LoginForm(Form):

	usr_name = StringField("Username", [input_required()], 
							render_kw={"class_": "form-control"})

	psd_wrd = PasswordField("Password", [input_required()],
							render_kw={"class_": "form-control"})
		 
class Service(Form):
	
	name = StringField("Name", [input_required()], 
							render_kw={"class_": "form-control"})
	label = StringField("Label", [input_required()], 
							render_kw={"class_": "form-control"})
	image = FileField('Service Icon', [input_required()], 
							render_kw={"class_": "form-control"})
	
	category_name = StringField("Category Name", [input_required()], 
								render_kw={'class_': "form-control"})



class ServiceItem(Form):

	name = StringField("Name", [input_required()], 
					   render_kw={'class_': "form-control"})

	label = StringField("Label", [input_required()], 
						render_kw={"class_": "form-control"})

	image = FileField('Menu Icon', [input_required()], 
					  render_kw={"class_": "form-control"})
	
	service = SelectField("Service", [input_required()], 
						  render_kw={"class_": "form-control"}, coerce=int)