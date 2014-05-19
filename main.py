# -*- coding: utf-8 -*-

import cherrypy
import os
import sys
from jinja2 import Template, Environment, PackageLoader
from src.database import createSchema, getStreams, checkLoading
from src.twitchLoader import loadStreams

the_current_folder = os.path.dirname(os.path.abspath(__file__))
env = Environment(loader=PackageLoader('main', 'templates'))

#Main Site definitions/mappings
class main_site(object):	
	def getCDN(self, server_mode):
		if server_mode == "dev":
			return("static")
		else:
			return ("http://cdn.fight.watch")

	def default(self, *args):		
		template = env.get_template('404.html')
		cherrypy.response.status = 404	
		return template.render(cdn_environment=self.getCDN(server_mode) )
	
	def loading(self):		
		template = env.get_template('loading.html')
		return template.render(cdn_environment=self.getCDN(server_mode) )

	def index(self):			
		template = env.get_template('index.html')
				
		try:			
			db_info = getStreams()			
		except Exception, err:			
			for error in err:
				cherrypy.log("Problem querying: " + str(err) )				
			return self.default()
		
		if db_info == True:
			#If it returns false send a loading page that auto-refreshes after 3 seconds.	
			return self.loading()
		else:
			try:				
				return  template.render(streams=db_info[0], updated=db_info[1], cdn_environment=self.getCDN(server_mode) )
			except Exception, err: 
				for error in err:
					cherrypy.log("Problem building template: " + str(err) )				
	index.exposed = True	

	def thanks(self):
		template = env.get_template('thanks.html')
		return template.render(cdn_environment=self.getCDN(server_mode) )		
	thanks.exposed = True

	def checkDB(self):
		return ( str(checkLoading()) )
	checkDB.exposed = True


#Error page definitions /mappings
def error_page_404(status, message, traceback, version):
	template = env.get_template('404.html')
	cherrypy.response.status = 404	
	return template.render(cdn_environment="http://cdn.fight.watch" )

cherrypy.config.update ({'error_page.404':  error_page_404 })


def startServer():
	if server_mode == "dev":
		cherrypy.config.update({ 'server.socket_host': '0.0.0.0',
		                       'server.socket_port': 8000,                         
		                       })				
		conf = {
		  '/static': { 'tools.staticdir.on' : True,
		                'tools.staticdir.dir': os.path.join(the_current_folder, 'static')
		              },        
		   '/static/css': { 'tools.staticdir.on' : True,
		                    'tools.staticdir.dir': os.path.join(the_current_folder, 'static/css')
		                  },
		   '/static/js': { 'tools.staticdir.on' : True,
		                'tools.staticdir.dir': os.path.join(the_current_folder, 'static/js')
		              },           
		    '/static/images': { 'tools.staticdir.on' : True,
		                'tools.staticdir.dir': os.path.join(the_current_folder, 'static/images'),
		                'tools.staticdir.content_types': {'jpg': 'image/jpeg'}
		                  },            
		  'favicon.ico': {
		                  'tools.staticfile.on': True,
		                  'tools.staticfile.filename': os.path.join(the_current_folder, "static/favicon.ico")
		              }
		  }

		cherrypy.quickstart(main_site(), config=conf)
	elif server_mode == "production":
		cherrypy.config.update({ 
		                         'environment': 'production',
		                         'log.screen': False,
		                         'log.error_file': '/home/thingdeux/webapps/fightwatch/fight.watch/error.log',
		                         'server.socket_host': '127.0.0.1',
		                         'server.socket_port': 28921,
		                         })
		cherrypy.quickstart( main_site() )
	
if __name__ == "__main__":
	argument = sys.argv
	
	try:
		argument[1]
		if argument[1] == "dev":
			server_mode = argument[1]
		else:
			server_mode = "production"
	except:
		server_mode = "production"	

	#Make sure DB has tables and is active
	createSchema()
	startServer()