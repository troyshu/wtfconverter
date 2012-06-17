import cgi
import datetime
import urllib
import webapp2

from google.appengine.ext import db
from google.appengine.api import users

import jinja2
import os

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
	

class PastConversion(db.Model):
  """Models an individual Guestbook entry with an author, content, and date."""
  user = db.UserProperty()
  fromUnit = db.StringProperty()
  toUnit = db.StringProperty()
  value = db.FloatProperty()
  date = db.DateTimeProperty(auto_now_add=True)


def pastConversions_key():
  """Constructs a Datastore key for a PastConversions entity with guestbook_name."""
  return db.Key.from_path('PastConversions','default_pastConversions')


class MainPage(webapp2.RequestHandler):
    def get(self):
        '''guestbook_name=self.request.get('guestbook_name')'''
        '''query = PastConversion.all().ancestor(
            pastConversions_key()).order('date')
        pastConversions = query.fetch(10)'''

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login' 

        template_values = {
            #'pastConversions': pastConversions,
            'url': url,
            'url_linktext': url_linktext,
        }

        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render(template_values))

class Converter(webapp2.RequestHandler):
	def post(self):
		
		#write conversion to database? could be useful for eventual statistics. eg number of conversions per user/visit, most popular units, etc.
		
		# We set the same parent key on the 'Greeting' to ensure each greeting is in
		# the same entity group. Queries across the single entity group will be
		# consistent. However, the write rate to a single entity group should
		# be limited to ~1/second.
		
		number = float(cgi.escape(self.request.get('number')))
		
		#TODO: add checker to make sure nothing but floats entered.
		
		conversion = PastConversion(parent=pastConversions_key())
		if users.get_current_user():
			conversion.user = users.get_current_user()
			
		conversion.fromUnit = 'seconds'
		conversion.toUnit = 'cesium'
		conversion.value = number
		conversion.put()
		
		
		self.redirect('/?' + urllib.urlencode({'number': number}))
	
	
app = webapp2.WSGIApplication([('/', MainPage),
                               ('/convert', Converter)],
                              debug=True)