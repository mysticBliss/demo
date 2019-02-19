#
#
#
# try: #python3
#     import urllib.request
#     import urllib.parse
#     def sendSMS(apikey, numbers, sender, message):
#         params = {'apikey': apikey, 'numbers': numbers, 'message' : message, 'sender': sender}
#         f = urllib.request.urlopen('https://api.textlocal.in/send/?'
#             + urllib.parse.urlencode(params))
#         return (f.read(), f.code)
#
#
# except: #python2
#
#     import urllib
#     import urllib2
#     from contextlib import closing
#
#     def sendSMS(apikey, numbers, sender, message):
#         url = 'https://api.textlocal.in/send/?'
#         params = {'apikey': apikey, 'numbers': numbers, 'message' : message, 'sender': sender}
#         data = urllib.urlencode(params)
#         req = urllib2.Request(url, data)
#         with closing(urllib2.urlopen(req)) as response:
#             return (response.read(),response.code)
#
# resp, code = sendSMS('KuJmVw/fhHc-kI6bdeLbiRWOndiU4TppCOYlc2eNyr','919632911213', 'TXTLCL', 'Test with an ampersand  and a note')
# print (resp)
#
