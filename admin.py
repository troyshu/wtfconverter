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
	

class ConversionFactor(db.Model):
  """Models a conversion factor."""
  fromUnit = db.StringProperty()
  toUnit = db.StringProperty()
  factor = db.FloatProperty()
  


def conversionFactors_key():
  """Constructs a Datastore key for a PastConversions entity with guestbook_name."""
  return db.Key.from_path('ConversionFactors','default_conversionFactors')


class MainPage(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		auth=0
		if user:
			if user.nickname()=='tmshu1':
				url = users.create_logout_url(self.request.uri)
				url_linktext='Logout'
				auth=1
			else:
				url = users.create_login_url(self.request.uri)
				url_linktext = 'Login'
		else:
			url = users.create_login_url(self.request.uri)
			url_linktext = 'Login'
		
		template_values = {
				'auth':auth,
				'url':url,
				'url_linktext':url_linktext
		}
		
		template = jinja_environment.get_template('add.html')
		self.response.out.write(template.render(template_values))
		
	def post(self):
		factor = float(cgi.escape(self.request.get('factor')).replace(",", ""))
		fromUnit = cgi.escape(self.request.get('fromUnit'))
		toUnit = cgi.escape(self.request.get('toUnit'))
		conversion = ConversionFactor(parent=conversionFactors_key())
		conversion.fromUnit = fromUnit
		conversion.toUnit = toUnit
		conversion.factor = factor
		conversion.put()
		
		#also put in the inverse
		factor = 1/factor
		temp = fromUnit
		fromUnit = toUnit
		toUnit = temp
		conversion = ConversionFactor(parent=conversionFactors_key())
		conversion.fromUnit = fromUnit
		conversion.toUnit = toUnit
		conversion.factor = factor
		conversion.put()
		
		print 'GREAT SUCCESS'
		
		self.redirect('/admin?' + urllib.urlencode({'status': '1'}))

app = webapp2.WSGIApplication([('/admin', MainPage)],
                              debug=True)