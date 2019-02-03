from flask_wtf import FlaskForm
from wtforms import HiddenField, SelectMultipleField, StringField,TextField,TextAreaField,FileField,PasswordField, SubmitField,RadioField,IntegerField,SelectField,validators, ValidationError
from wtforms.fields.html5 import DateField,DecimalField,EmailField

class AddRoom(FlaskForm):
    room_name = TextField("Room Name "
                             ,[validators.Required("Room Name is Mandatory!")]
                            )
    room_type = SelectField('Room Type', choices = [('Single', 'Singles'),('Double', 'Double'),('Triple', 'Triple'),('Quad', 'Quad'),('Queen', 'Queen'),('King', 'King'),('Twin', 'Twin'), ('Studio', 'Studio'), ('Executive Suite', 'Executive Suite'), ('President Suite','President Suite')])
    total_rooms=IntegerField("Total Rooms",[validators.Required("Please enter total rooms in this catergory.")])
    room_capacity=IntegerField("Capacity",[validators.Required("Please enter max capacity of this room.")])
    room_desc=TextAreaField("Description")
    room_price=IntegerField("Price",[validators.Required("Please enter price of this room")])
    room_len=IntegerField("Length",[validators.Required("Please enter length of this room")])
    room_brd=IntegerField("Breath",[validators.Required("Please enter breath of this room")])
    # facilities=SelectMultipleField('Facilities Offered')

class AddFacility(FlaskForm):
    facility_name = TextField("Facility Name "
                             ,[validators.Required("Facility Name is Mandatory!")]
                            )
    facility_type = SelectField('Facility Type', choices = [('Room Related', 'Room Related'),('Hotel Related', 'Hotel Related')])
    facility_serves=IntegerField("Serves",[validators.Required("Please enter max capacity of this room.")])
    facility_desc=TextAreaField("Facility Description")
    facility_price=IntegerField("Facility Price",[validators.Required("Please enter price of this room")])


class RegisterHotel(FlaskForm):
    hotelname = TextField("Search Property Name in Google Maps")
    hotelname1 = TextField("Property Name "
                             ,[validators.Required("Property Name is Mandatory!")]
                            )
    locality = HiddenField()
    plus_code = HiddenField()

    chain = TextField("Chain Name (if any)")
    rating = SelectField('Rating', choices = [('1', '1'),('2', '2'),('3', '3'),('4', '4'),('5', '5'),('0', 'Not Rated')])
    rooms = IntegerField("Total Rooms",[validators.Required("Please enter total rooms in your property.")])
    floors = IntegerField("Total Floor",[validators.Required("Please enter total floors your property has.")])
    hotel_type = SelectField('Hotel Type', choices = [('business', 'Business'),('family', 'Family')])
    estd=DateField("Estd Date",  [validators.Required("Select Established Date")], format='%Y-%m-%d')
    short_desc = TextField("Short Description")
    long_desc = TextAreaField("Long Description")
    address = TextAreaField("Address")
    city = TextField("City",[validators.Required("Please enter City Location")])
    state = TextField("State",[validators.Required("Please enter State Location")])
    country = TextField("Country",[validators.Required("Please enter Country Location")])
    postal_code = IntegerField("Zip Code",[validators.Required("Please enter POSTAL/ZIP Area code")])
    latitude = StringField("Latitude",[validators.Required("Please enter Latitude Information")])
    longitude = StringField("Longitude",[validators.Required("Please enter Longitude Information")])
    airport_distance=DecimalField("Airport Distance",[validators.Required("Please enter how far is Airport")])
    city_center_distance=DecimalField("City Center Distance",[validators.Required("Please enter how far is City Center")])
    images = FileField(u'Logo File')
    phno =IntegerField("Phone No", [validators.Required("Please enter Phone No")])
    phno2 =IntegerField("Additional Phone No")
    email=EmailField("Email ID",[validators.Required("Please enter Email ID")])
    submit = SubmitField("Send")
