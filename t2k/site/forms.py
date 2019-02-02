from flask_wtf import FlaskForm
from wtforms import TextField, SubmitField,IntegerField,validators, ValidationError,HiddenField
from wtforms.fields.html5 import EmailField,TelField,DateField

class ContactUs(FlaskForm):
    first_name = TextField("First Name ",[validators.Required("First Name is Mandatory!")])
    last_name = TextField("Last Name ",[validators.Required("Last Name is Mandatory!")])
    email = EmailField("email ",[validators.Required("email is Mandatory!")])
    phone=TelField("Phone",[validators.Required("Phone is Mandatory")])
    message = TextField("Message")
    submit = SubmitField("Send")

class Subscriber(FlaskForm):
    email = EmailField("email ",[validators.Required("email is Mandatory!")])
    submit = SubmitField("Send")

class Booking(FlaskForm):
    room_type= HiddenField()
    check_in=DateField("Arrival Date",  [validators.Required("Select Arrival Date")], format='%Y-%m-%d')
    check_out=DateField("Departure Date",  [validators.Required("Select Departure Date")], format='%Y-%m-%d')
    adults = TextField("Adults",[validators.Required("No of Adults travelling are Mandatory!")])
    children = TextField("Children")
    name_booking = TextField("Name",[validators.Required("First Name is Mandatory!")])
    email_booking = EmailField("email ",[validators.Required("email is Mandatory!")])
    submit = SubmitField("Send")
