from flask_wtf import FlaskForm,RecaptchaField
from wtforms import TextField, SubmitField,IntegerField,validators, ValidationError,HiddenField
from wtforms.fields.html5 import EmailField,TelField,DateField
import datetime

class ContactUs(FlaskForm):
    first_name = TextField("First Name ",[validators.Required("First Name is Mandatory!")])
    last_name = TextField("Last Name ",[validators.Required("Last Name is Mandatory!")])
    email = EmailField("Email ",[validators.Required("Email is Mandatory!")])
    phone=TelField("Phone",[validators.Required("Phone is Mandatory")])
    message = TextField("Message")
    recaptcha = RecaptchaField()
    submit = SubmitField("Send")

# class Subscriber(FlaskForm):
#     email = EmailField("email ",[validators.Required("email is Mandatory!")])
#     submit = SubmitField("Send")


def chkdate(form, field):
    if field.data < form.check_in.data:
        raise ValidationError('Departure Date cannot be before Arrival Date')

def chktoday(form,field):
    if field.data < datetime.date.today():
        raise ValidationError('Arrival Date can\'t be less than today')


class Booking(FlaskForm):
    room_type= HiddenField()
    check_in=DateField("Arrival Date",  [validators.Required("Select Established Date"),chktoday], format='%Y-%m-%d')
    check_out=DateField("Departure Date",  [validators.Required("Select Established Date"), chkdate] , format='%Y-%m-%d')
    adults = TextField("Adults",[validators.Required("No of Adults travelling are Mandatory!")])
    children = TextField("Children")
    name_booking = TextField("Name",[validators.Required("First Name is Mandatory!")])
    email_booking = EmailField("email ",[validators.Required("email is Mandatory!")])
    # recaptcha = RecaptchaField()
    submit = SubmitField("Send")
