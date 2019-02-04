from flask import Blueprint,render_template,g,request,redirect,url_for,flash
from t2k import mongo
import datetime
from bson import json_util, ObjectId
from t2k.site.forms import ContactUs,Booking
import json

mod=Blueprint('site', __name__,
                            template_folder='templates',
                            static_folder='static',
                             static_url_path='/static'
                             )


def get_commons():
    import phonenumbers
    res = mongo.db.hotels.find_one({ "_id" : ObjectId('5c013a9d2ccb025bd4d8295a') },
                     { "_id":1, "hotelname": 1,"estd":1,"rating": 1,"long_desc":1,"chain": 1,"hoteladdress":1,"hoteltype": 1,
                     "short_desc":1,"state": 1,"longitude":1,"city_center_distance": 1,
                     "floors":1,"postal_code": 1,"rooms":1,"latitude": 1,"airport_distance":1,"city":1,"country":1,"phno":1,"phno2":1,"email":1,"plus_code":1, "locality":1})
    g.hotelname = res['hotelname']
    g.long_desc = res['long_desc']
    g.hoteladdress = res['hoteladdress']
    g.country = res['country']
    g.hotel_id = res['_id']
    g.email=res['email']
    g.phno=phonenumbers.format_number(phonenumbers.parse(str(res['phno']), 'IN'), phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    g.phno2=phonenumbers.format_number(phonenumbers.parse(str(res['phno2']), 'IN'), phonenumbers.PhoneNumberFormat.INTERNATIONAL)
def get_rooms_facility():
    rooms = mongo.db.rooms.find({ "hotel_id" : ObjectId('5c013a9d2ccb025bd4d8295a') },{"room_name" : 1,
                                                                        "room_type" : 1,
                                                                        "room_desc" : 1,
                                                                        "room_price" : 1,
                                                                        "room_capacity" : 1,
                                                                        "room_len" : 1,
                                                                        "room_brd" : 1,
                                                                        "total_rooms" : 1, "_id": 1})

    rlist =[]
    for x in rooms:
        rlist.append(x)

    return g.rlist

@mod.route('/')
def index():
    get_commons()
    # lst = get_rooms_facility()
    rooms = mongo.db.rooms.find({ "hotel_id" : ObjectId('5c013a9d2ccb025bd4d8295a') },{"room_name" : 1,
                                                                        "room_type" : 1,
                                                                        "room_desc" : 1,
                                                                        "room_price" : 1,
                                                                        "room_capacity" : 1,
                                                                        "room_len" : 1,
                                                                        "room_brd" : 1,
                                                                        "total_rooms" : 1, "_id": 1})

    rlist =[]
    for x in rooms:
        rlist.append(x)
    return render_template('site/index.html', rlist=rlist, title='Welcome')


@mod.route('/about',methods=['GET','POST'])
def about():
    get_commons()
    return render_template('site/about.html', title='About')

@mod.route('/faq',methods=['GET','POST'])
def faq():
    get_commons()
    return render_template('site/faq.html', title='FAQs')

@mod.route('/rooms',methods=['GET','POST'])
def rooms():
    get_commons()
    rooms = mongo.db.rooms.find({ "hotel_id" : ObjectId('5c013a9d2ccb025bd4d8295a') },{"room_name" : 1,
                                                                        "room_type" : 1,
                                                                        "room_desc" : 1,
                                                                        "room_price" : 1,
                                                                        "room_capacity" : 1,
                                                                        "room_len" : 1,
                                                                        "room_brd" : 1,
                                                                        "total_rooms" : 1, "_id": 1})

    rlist =[]
    for x in rooms:
        rlist.append(x)
    return render_template('site/rooms.html',rlist=rlist, title='Rooms')

@mod.route('/room_detail/<string:id>',methods=['GET','POST'])
def room_detail(id):
    get_commons()

    rd = mongo.db.rooms.find_one({ "_id" : ObjectId(str(id)) },{"room_name" : 1,
                                                                    "room_type" : 1,
                                                                    "room_desc" : 1,
                                                                    "room_price" : 1,
                                                                    "room_capacity" : 1,
                                                                    "room_len" : 1,
                                                                    "room_brd" : 1,
                                                                    "total_rooms" : 1, "_id": 1})

    res_fac = mongo.db.rooms.aggregate([ {   "$match" : { "_id" : ObjectId(str(id)),  }
                                                       },
                                                   {
                                                     "$lookup":
                                                       {
                                                         "from": "facility",
                                                         "localField": "facilities",
                                                         "foreignField": "_id",
                                                         "as": "facilities"
                                                       }

                                                 },

                                                    { "$project" : {"facilities":1}}
                                                ])
    facilities=[]
    for x in res_fac:
        for i in range(len(x['facilities'])):
            facilities.append(str(x['facilities'][i]['facility_name']))


    form = Booking(request.form)
    data = {
        'check_in': form.check_in.data,
        'check_out':form.check_out.data,
        'adults':form.adults.data,
        'children':form.children.data,
        'name_booking': form.name_booking.data,
        'email_booking':form.email_booking.data,
        'room_type':form.room_type.data
        }
    print data
    if request.method == 'POST':
        print
        if form.validate():
            results = mongo.db.booking.insert_one({ "hotel_id" : ObjectId(g.hotel_id) ,
                                                    'check_in': request.form['check_in'].strftime("%Y%m%d"),
                                                    'check_out':request.form['check_out'].strftime("%Y%m%d"),
                                                    'adults':form.adults.data,
                                                    'children':form.children.data,
                                                    'name_booking': form.name_booking.data,
                                                    'email_booking':form.email_booking.data,
                                                    'room_type':form.room_type.data,
                                                    'request_date': datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") })

            return render_template('site/thanks.html')
        else:
            flash('Fill all fields for correct processing','error')
    return render_template('site/room_detail.html', facilities=facilities,rd=rd,form=form,id=id,title=rd['room_name'])





@mod.route('/contactus',methods=['GET','POST'])
def contactus():
    get_commons()
    form = ContactUs(request.form)
    if request.method == 'POST':
        data = {
            'first_name': form.first_name.data,
            'last_name':form.last_name.data,
            'email':form.email.data,
            'phone':form.phone.data,
            'message': form.message.data
            }
        print data
        if form.validate():
            results = mongo.db.leads.insert_one({ "hotel_id" : ObjectId(g.hotel_id) , 'first_name': form.first_name.data, 'last_name':form.last_name.data,'email':form.email.data,'phone':form.phone.data,'message': form.message.data,'requestdate':str(datetime.datetime.now()) })
            return render_template('site/thanks.html')
        else:
            flash('Fill all fields for correct processing','error')
    return render_template('site/contactus.html', form=form,title='Contact Us')

# @mod.route('/booking',methods=['POST'])
# def booking():
#     get_commons()
#     form = Booking(request.form)
#     if request.method == 'POST':
#         data = {
#             'check_in': form.check_in.data,
#             'check_out':form.check_out.data,
#             'adults':form.adults.data,
#             'children':form.children.data,
#             'name_booking': form.name_booking.data,
#             'email_booking':form.email_booking.data,
#             'room_type':form.room_type.data
#             }
#         print data
#         if form.validate():
#             results = mongo.db.booking.insert_one({ "hotel_id" : ObjectId(g.hotel_id) ,
#                                                     'check_in': form.check_in.data.strftime("%Y%m%d"),
#                                                     'check_out':form.check_out.data.strftime("%Y%m%d"),
#                                                     'adults':form.adults.data,
#                                                     'children':form.children.data,
#                                                     'name_booking': form.name_booking.data,
#                                                     'email_booking':form.email_booking.data,
#                                                     'room_type':form.room_type.data,
#                                                     'request_date': datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") })
#             return render_template('site/thanks.html')
#     return render_template('site/room_detail.html')

@mod.route('/gallery',methods=['GET','POST'])
def gallery():
    get_commons()
    return render_template('site/gallery.html',title='Gallery')

@mod.route('/thanks',methods=['GET','POST'])
def thanks():
    get_commons()
    return render_template('site/thanks.html', title='Thanks')







# @mod.route('/', subdomain="<user>", defaults={'path':''})
# def uindex(user):
#     return 'Welcome to your subdomain, {}'.format(user)
#
