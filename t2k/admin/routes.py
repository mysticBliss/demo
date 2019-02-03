from flask import current_app,Blueprint,render_template,request, flash,redirect,url_for,session
from passlib.hash import sha256_crypt
import datetime
from t2k.admin.forms import RegisterHotel
from t2k import mongo
from t2k import csrf
from functools import wraps
from werkzeug.utils import secure_filename
from bson import json_util, ObjectId
import json
import os


mod=Blueprint('admin', __name__, template_folder='templates', static_folder='static')

# Functions to check Login
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.','warning')
            return render_template('admin/login.html')
    return wrap



@mod.route('/')
@is_logged_in
def index():

        # session['username'] = request.form['username']
    return render_template('admin/dashboard.html')


@mod.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        try:
            results = mongo.db.users.find_one({ "username": request.form['username'] },{ "username": 1, "password" : 1, "DName":1,"access":1})
            print results
            if results is None:
                flash(u'Username doesn\'t exist', 'error')
            else:
                if request.form['username'] == results['username'] and  sha256_crypt.verify(request.form['password'], results['password']):
                    flash("Welcome, %s" %request.form['username'])
                    flash(u'Logging in ', 'success')
                    session['logged_in'] = True
                    session['username'] = request.form['username']

                    # Passing to views
                    session["DName"]=results["DName"]
                    hotel_access=[]
                    for id in json.loads(json_util.dumps(results["access"])):
                        res = mongo.db.hotels.find_one({ "_id" : ObjectId(str(id['$oid'])) },{ "hotelname": 1,"_id":1})
                        hotel_access.append({"hotelname": res['hotelname'], "id" : id['$oid']})


                    session['hotel_id'] = hotel_access[0]['id']
                    session['hotelname'] = hotel_access[0]['hotelname']

                    return render_template('admin/dashboard.html', hotel_access=hotel_access)
                else:
                    flash(u'Invalid Credentials!', 'warning')
                    return render_template('admin.login')
        except Exception as e:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(e).__name__, e.args)
            print (message)
    else:
        if 'logged_in' in session:
            session['username'] = request.form['username']
            return redirect(url_for('admin.dashboard'))
    return render_template('admin/login.html', title="Login")



@mod.route('/dashboard')
@is_logged_in
def dashboard():
    return render_template('admin/dashboard.html', title='Dashboard')


@mod.route('/logout')
@is_logged_in
def logout():
   # remove the username from the session if it is there
   #session.pop('username', None) pops out session for current user
   session.clear()
   flash(u'You are logged out successfully!', 'success')
   return render_template('admin/login.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in set(['png'])

@mod.route('/details',methods=['GET','POST'])
# @csrf.exempt
@is_logged_in
def details():
    print request.method
    form = RegisterHotel(request.form)

    if request.method == 'GET':

        res = mongo.db.hotels.find_one({ "_id" : ObjectId(session['hotel_id']) },
                         { "hotelname": 1,"estd":1,"rating": 1,"long_desc":1,"chain": 1,"hoteladdress":1,"hoteltype": 1,
                         "short_desc":1,"state": 1,"longitude":1,"city_center_distance": 1,
                         "floors":1,"postal_code": 1,"rooms":1,"latitude": 1,"airport_distance":1,
                         "city":1,"country":1,"plus_code":1, "locality":1,"phno":1,"phno2":1,"email":1})

        form.hotelname1.data = res['hotelname']
        form.estd.data= datetime.datetime.strptime(res['estd'], "%Y%m%d").date()
        form.rating.data = res['rating']
        form.long_desc.data = res['long_desc']
        form.chain.data = res['chain']
        form.address.data = res['hoteladdress']
        form.hotel_type.data = res['hoteltype']
        form.short_desc.data = res['short_desc']
        form.state.data = res['state']
        form.longitude.data = res['longitude']
        form.city_center_distance.data = res['city_center_distance']
        form.floors.data = res['floors']
        form.postal_code.data = res['postal_code']
        form.rooms.data = res['rooms']
        form.latitude.data = res['latitude']
        form.airport_distance.data = res['airport_distance']
        form.city.data = res['city']
        form.country.data = res['country']
        form.plus_code.data = res['plus_code']
        form.locality.data = res['locality']
        form.phno.data = res['phno']
        form.phno2.data = res['phno2']
        form.email.data = res['email']


    if request.method == 'POST':
        data = {
            'hotelname': form.hotelname1.data,
            'locality':form.locality.data,
            'chain':form.chain.data,
            'rating':form.rating.data,
            'rooms': form.rooms.data,
            'floors':form.floors.data,
            'hoteltype': form.hotel_type.data,
            'estd': form.estd.data.strftime("%Y%m%d"),
            'short_desc': form.short_desc.data,
            'long_desc':form.long_desc.data,
            'hoteladdress': form.address.data,
            'city':form.city.data,
            'state':form.state.data,
            'postal_code': form.postal_code.data,
            'latitude':form.latitude.data,
            'longitude':form.longitude.data,
            'airport_distance':int(form.airport_distance.data),
            'city_center_distance':int(form.city_center_distance.data),
            'plus_code':form.plus_code.data,
            'country': form.country.data,
            'phno':form.phno.data,
            'phno2':form.phno2.data,
            'email': form.email.data
            }
        print data


        # if 'images' not in request.files:
        #     flash('No file part')
        #     return redirect(request.url)
        # file = request.files['images']
        # # if user does not select file, browser also
        # # submit a empty part without filename
        # if file.filename == '':
        #     flash('No selected file')
        #     return redirect(request.url)
        # if file and allowed_file(file.filename):
        #     filename = secure_filename(file.filename)
        #     print filename
        #     print os.path.join(os.path.dirname(__file__),'admin','static','logo.png')
        #
        #     file.save(os.path.join(os.path.dirname(__file__),'static','logo.png'))

        # Second
        # images = request.files.to_dict()
        # print(form.images.name)
        # try:
        #     for image in images:
        #         print("1")
        #         print(images[image])        #this line will print value for the image key
        #         file_name = images[image].filename
        #         images[image].save('E:\\app\static\img')
        # except Exception as e:
        #     template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        #     message = template.format(type(e).__name__, e.args)
        #     print (message)
        # else:
        #     print 'SUCCESS'
        print  form.estd.data
        print request.form['hotelname']

        if form.validate():
            # Save the comment here.
            flash('Hello ' + form.hotelname.data)
            results = mongo.db.hotels.save({ "_id" : ObjectId(session['hotel_id']) , 'hotelname': form.hotelname1.data,
                                                                                        'locality':form.locality.data,
                                                                                        'chain':form.chain.data,
                                                                                        'rating':form.rating.data,
                                                                                        'rooms': form.rooms.data,
                                                                                        'floors':form.floors.data,
                                                                                        'hoteltype': form.hotel_type.data,
                                                                                        'estd': form.estd.data.strftime("%Y%m%d"),
                                                                                        'short_desc': form.short_desc.data,
                                                                                        'long_desc':form.long_desc.data,
                                                                                        'hoteladdress': form.address.data,
                                                                                        'city':form.city.data,
                                                                                        'state':form.state.data,
                                                                                        'postal_code': form.postal_code.data,
                                                                                        'latitude':form.latitude.data,
                                                                                        'longitude':form.longitude.data,
                                                                                        'airport_distance':int(form.airport_distance.data),
                                                                                        'city_center_distance':int(form.city_center_distance.data),
                                                                                        'plus_code':form.plus_code.data,
                                                                                        'country': form.country.data,
                                                                                        'phno':form.phno.data,
                                                                                        'phno2':form.phno2.data,
                                                                                        'email': form.email.data
                                                                                        })
            flash("Success",'success')

        else:
            flash('All the form fields are required. ')
    return render_template('admin/details.html', form=form, title="Hotel Details") #"Admin Page" + str(UPLOAD_PATH)

@mod.route('/rooms',methods=['GET','POST'])
@is_logged_in
def rooms():
    # from t2k.admin.forms import AddRoom
    # form = AddRoom(request.form)
    rooms = mongo.db.rooms.find({ "hotel_id" : ObjectId(str(session['hotel_id'])) },{"room_name" : 1,
                                                                        "room_type" : 1,
                                                                        "room_desc" : 1,
                                                                        "room_price" : 1,
                                                                        "room_capacity" : 1,
                                                                        "room_len" : 1,
                                                                        "room_brd" : 1,
                                                                        "total_rooms" : 1, "_id": 1})



    if rooms == None:
        flash("No Rooms", 'error')
    #
    # if request.method == 'POST':
    #     print form.roomname.data
    return render_template('admin/rooms.html', rooms=rooms, title="Room Details")

@mod.route('/facility',methods=['GET','POST'])
@is_logged_in
def facility():
    facility = mongo.db.facility.find({})
    if facility == None:
        flash("No Facility Registered", 'error')


    return render_template('admin/facility.html', facility=facility, title="Facility Details")

@mod.route('/edit_facility/<string:id>/', methods=['GET','POST'])
@is_logged_in
def edit_facility(id):
    from t2k.admin.forms import AddFacility
    form = AddFacility(request.form)

    # facilities = mongo.db.facility.find({})

    if request.method == 'GET':
        # selected_facilities = [ ObjectId(str(facility)) for facility in request.form.getlist("facilities")]
        # selected_facilities = [ ObjectId("5c21ea642ccb0249a8267622")]
        res = mongo.db.facility.find_one({ "_id" : ObjectId(str(id)) },{"facility_name" : 1,
                                                                        "facility_type" : 1,
                                                                        "facility_desc" : 1,
                                                                        "facility_price" : 1,"facility_serves":1,
                                                                        "_id": 1})

        form.facility_name.data = res['facility_name']
        form.facility_type.data = res['facility_type']
        form.facility_desc.data = res['facility_desc']
        form.facility_price.data = res['facility_price']
        form.facility_serves.data = res['facility_serves']

    if request.method == 'POST':
        selected_facilities = [ ObjectId(str(facility)) for facility in request.form.getlist("facilities")]
        print selected_facilities
        data = {
            'facility_name': form.facility_name.data,
            'facility_type':form.facility_type.data,
            'facility_desc':form.facility_desc.data,
            'facility_serves':int(form.facility_serves.data),
            'facility_price':int(form.facility_price.data)
            }
        if form.validate():
            # Save the comment here.
            flash('Hello ' + form.facility_name.data)
            results = mongo.db.facility.save({ "_id" : ObjectId(id) , 'facility_name': form.facility_name.data,
                                                                        'facility_type':form.facility_type.data,
                                                                        'facility_desc':form.facility_desc.data,
                                                                        'facility_serves':int(form.facility_serves.data),
                                                                        'facility_price':int(form.facility_price.data)
                                                                         })
            flash("Success",'success')
            return redirect(url_for('admin.facility'))
        else:
            flash('All the form fields are required. ')

    return render_template('admin/edit_facility.html', id=id , form=form, title="Edit Facilty Details")



@mod.route('/edit_room/<string:id>/', methods=['GET','POST'])
@is_logged_in
def edit_room(id):
    from t2k.admin.forms import AddRoom
    form = AddRoom(request.form)

    facilities = mongo.db.facility.find({})

    if request.method == 'GET':
        # selected_facilities = [ ObjectId(str(facility)) for facility in request.form.getlist("facilities")]
        # selected_facilities = [ ObjectId("5c21ea642ccb0249a8267622")]
        res = mongo.db.rooms.find_one({ "_id" : ObjectId(str(id)) },{"room_name" : 1,
                                                                        "room_type" : 1,
                                                                        "room_desc" : 1,
                                                                        "room_price" : 1,
                                                                        "room_capacity" : 1,
                                                                        "room_len" : 1,
                                                                        "room_brd" : 1,
                                                                        "total_rooms" : 1, "_id": 1})

        form.room_name.data = res['room_name']
        form.room_type.data = res['room_type']
        form.room_desc.data = res['room_desc']
        form.room_price.data = res['room_price']
        form.room_capacity.data = res['room_capacity']
        form.room_len.data = res['room_len']
        form.room_brd.data = res['room_brd']
        form.total_rooms.data = res['total_rooms']


        #  Existing facilities
        res_fac = mongo.db.rooms.aggregate([ {   "$match" : { "_id" : ObjectId(str(id)) }
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
        selected_facilities=[]
        for x in res_fac:
            for i in range(len(x['facilities'])):
                selected_facilities.append(ObjectId(str(x['facilities'][i]['_id'])))


    if request.method == 'POST':
        selected_facilities = [ ObjectId(str(facility)) for facility in request.form.getlist("facilities")]
        print selected_facilities
        data = {
            'room_name': form.room_name.data,
            'room_type':form.room_type.data,
            'room_desc':form.room_desc.data,
            'room_price':int(form.room_price.data),
            'room_capacity': int(form.room_capacity.data),
            'room_len':int(form.room_len.data),
            'room_brd': int(form.room_brd.data),
            # 'estd': form.estd.data.strftime("%Y%m%d"),
            'total_rooms': form.total_rooms.data,
            'facilities' : selected_facilities
            }
        if form.validate():
            # Save the comment here.
            flash('Hello ' + form.room_name.data)
            results = mongo.db.rooms.save({ "_id" : ObjectId(id) , 'room_name': form.room_name.data,
                                                                                        'room_type':form.room_type.data,
                                                                                        'room_desc':form.room_desc.data,
                                                                                        'room_price':int(form.room_price.data),
                                                                                        'room_capacity': int(form.room_capacity.data),
                                                                                        'room_len':int(form.room_len.data),
                                                                                        'room_brd': int(form.room_brd.data),
                                                                                        'total_rooms': form.total_rooms.data,
                                                                                        'hotel_id': ObjectId(session['hotel_id']),
                                                                                        'facilities' : [ ObjectId(str(facility)) for facility in request.form.getlist("facilities")]
                                                                                        })
            flash("Success",'success')
            return redirect(url_for('admin.rooms'))
        else:
            flash('All the form fields are required. ')

    return render_template('admin/edit_room.html', id=id ,facilities = facilities,selected_facilities=selected_facilities, form=form, title="Edit Room Details")


@mod.route('/add_room', methods=['GET','POST'])
@is_logged_in
def add_room():
    from t2k.admin.forms import AddRoom
    form = AddRoom(request.form)
    facilities = mongo.db.facility.find({})

    if request.method == 'POST':
        print form.room_name.data
        # selected_facilities = [ ObjectId(str(facility)) for facility in request.form.getlist("facilities")]
        # print 'facilities' : [ ObjectId(str(facility)) for facility in request.form.getlist("facilities")]
        data = {
            'room_name': form.room_name.data,
            'room_type':form.room_type.data,
            'room_desc':form.room_desc.data,
            'room_price':int(form.room_price.data),
            'room_capacity': int(form.room_capacity.data),
            'room_len':int(form.room_len.data),
            'room_brd': int(form.room_brd.data),
            'total_rooms': form.total_rooms.data,
            'hotel_id' : ObjectId(session['hotel_id']),
            'facilities' : [ ObjectId(str(facility)) for facility in request.form.getlist("facilities")]
            }
        if form.validate():

            # Save the comment here.
            flash('Hello ' + form.room_name.data)
            results = mongo.db.rooms.insert_one(data)
            flash("Success",'success')
            return redirect(url_for('admin.rooms'))

        else:
            flash('All the form fields are required. ')

    return render_template('admin/add_room.html',facilities=facilities,  form=form, title="Add New Room Details")

@mod.route('/add_facility', methods=['GET','POST'])
@is_logged_in
def add_facility():
    from t2k.admin.forms import AddFacility
    form = AddFacility(request.form)

    if request.method == 'POST':
        print form.facility_name.data
        data = {
            'facility_name': form.facility_name.data,
            'facility_type':form.facility_type.data,
            'facility_serves':int(form.facility_serves.data),
            'facility_desc':form.facility_desc.data,
            'facility_price': int(form.facility_price.data)
            }
        if form.validate():
            # Save the comment here.
            flash('Hello ' + form.facility_name.data)
            results = mongo.db.facility.insert_one(data)
            flash("Success",'success')
            redirect(url_for('admin.rooms'))

        else:
            flash('All the form fields are required. ')

    return render_template('admin/add_facility.html', form=form, title="Add New Facilty Type")
