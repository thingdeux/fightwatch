import cherrypy
import requests
import os
from jinja2 import Template, Environment, PackageLoader


server_mode = "dev"
the_current_folder = os.path.dirname(os.path.abspath(__file__))
env = Environment(loader=PackageLoader('main', 'templates'))


class main_site(object):	
	def getStreams(self, search_phrases):
		def queryTwitch(query):
			twitch_url = "https://api.twitch.tv/kraken/search/streams?q="
			limit = "&limit=4"
			r = requests.get(twitch_url + str(query) + limit)
			return r.json()

		json_dict = {}
		for search_phrase in search_phrases:
			json_dict[search_phrase] = queryTwitch(search_phrase)
		
		return (json_dict)

	def index(self):			
		template = env.get_template('index.html')		
		returned_json = self.getStreams(["Street Fighter", "Ultimate Marvel", "King of Fighter", 
										"Injustice", "Super Smash", "Mortal Kombat", "Killer Instinct" ])		

		return  template.render(json=returned_json)
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
	                             'log.error_file': '/home/thingdeux/webapps/dev/joshandlinz.com/error.log',
	                             'server.socket_host': '127.0.0.1',
	                             'server.socket_port': 17472,
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
	startServer()