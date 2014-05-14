import cherrypy
import os
import sys
from jinja2 import Template, Environment, PackageLoader
from src.database import createSchema, getStreams

the_current_folder = os.path.dirname(os.path.abspath(__file__))
env = Environment(loader=PackageLoader('main', 'templates'))


class main_site(object):		

	def index(self):			
		template = env.get_template('index.html')		
		active_streams = getStreams()

		if streams == False:
			#If it returns false send a loading page that auto-refreshes after like 3 seconds.	
			return ("Loading dude sorry")
		else:
			return  template.render(streams=active_streams)
				
	index.exposed = True
	



def startServer():
	if server_mode == "dev":
		cherrypy.config.update({ 'server.socket_host': '0.0.0.0',
		                       'server.socket_port': 8000,                         
		                       })
  	elif server_mode == "production":
	    cherrypy.config.update({ 
	                             'environment': 'production',
	                             'log.screen': False,
	                             'log.error_file': '/home/thingdeux/webapps/fightwatch/fight.watch/error.log',
	                             'server.socket_host': '127.0.0.1',
	                             'server.socket_port': 28921,
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

	startServer()