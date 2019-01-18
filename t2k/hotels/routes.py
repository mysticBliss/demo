from flask import Blueprint,render_template
mod=Blueprint('hotels', __name__ ,  template_folder='templates', static_folder=None #, static_url_path='/theme-albert')
                )
mod.static_folder = 'static'
mod.add_url_rule('/<path:filename>',
              endpoint='static',
              view_func=mod.send_static_file,
              subdomain='<subdomain>')

# optional. If not set, the above view_func will be passed <tenant> as a parameter.
@mod.url_value_preprocessor
def before_route(endpoint, values):
    if values is not None:
        values.pop('subdomain', None)


# @mod.route('/<string:hotelname>/', methods=['GET','POST'])
# def index(hotelname):
#     print hotelname
#     return render_template('hotels/index.html',  subdomain=hotelname) #"Welcome " +hotelname

# @mod.route('/')
# def index():
#     # print subdomain
#     # print staticurl
#     # print mod.static_url_path
#     return render_template('hotels/index.html') #"Welcome " +hotelname


@mod.route('/', subdomain="rosepetal")
def index():
    return render_template('hotels/index.html',subdomain='platform')
#
# @mod.route('/', subdomain="events")
# def events():
# 	return render_template('hotels/index.html', subdomain='EVENTS')

@mod.route('/about')
def about(hotelname):
    return render_template('hotels/about.html')

 # Add static URL rules
# mod.add_url_rule('/static/<path:filename>',
#                  endpoint='static',
#                  view_func=mod.send_static_file)
# mod.add_url_rule('/static/<path:filename>',
#                  endpoint='static',
#                  subdomain='<subdomain>',
#                  view_func=mod.send_static_file)
#
# @mod.before_request
# def check_logged_in():
#     return
