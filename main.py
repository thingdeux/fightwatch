# -*- coding: utf-8 -*-
import cherrypy
import os
import sys
from jinja2 import Environment, PackageLoader
from src.database import createSchema, getStreams, checkLoading
from src.elasticsearch_query import match_query_by_name

the_current_folder = os.path.dirname(os.path.abspath(__file__))
env = Environment(loader=PackageLoader('main', 'templates'))


# Main Site definitions/mappings
class main_site(object):
    def getCDN(self, server_mode):
        # Returns CDN location if server mode is prod, else dev static dir.
        if server_mode == "dev":
            return("/static")
        else:
            return ("http://cdn.fight.watch")

    def default(self, *args):
        # 404 Page
        template = env.get_template('404.html')
        cherrypy.response.status = 404
        return template.render(cdn_environment=self.getCDN(server_mode))

    def loading(self):
        # Loading page:
        # Should only be rendered in case of new feeds being fetched.
        template = env.get_template('loading.html')
        return template.render(cdn_environment=self.getCDN(server_mode))

    def index(self):
        template = env.get_template('index.html')

        try:
            # Get the list of twitch streams
            db_info = getStreams()
        except Exception, err:
            for error in err:
                cherrypy.log("Problem querying: " + str(err))
            return self.default()

        if db_info is True:
            # If DB can't be reached -
            #    return a loading page that auto-refreshes after 3 seconds.
            return self.loading()
        else:
            try:
                return template.render(
                    streams=db_info[0],
                    updated=db_info[1],
                    cdn_environment=self.getCDN(server_mode)
                    )
            except Exception, err:
                for error in err:
                    cherrypy.log("Problem building template: " + str(err))
    index.exposed = True

    def thanks(self):
        # Thanks page after a donation
        template = env.get_template('thanks.html')
        return template.render(cdn_environment=self.getCDN(server_mode))
    thanks.exposed = True

    def fighter(self, name=None, *args):
        # No Name is passed to fighter, return index for fighter template
        if name is None:
            if len(name) < 1:
                template = env.get_template('byFighter.html')
                return template.render(
                    cdn_environment=self.getCDN(server_mode))
        else:
            results = match_query_by_name(name)
            if len(results) > 1:
                template = env.get_template('byFighter.html')
                return template.render(cdn_environment=self.getCDN(server_mode),
                                       name=name,
                                       results=results)
            else:
                template = env.get_template('byFighter.html')
                return template.render(cdn_environment=self.getCDN(server_mode),
                                       name=name,
                                       results=results)

    # Stats Index Handler for ElasticSearch Fight.Watch DB
    def stats(self, route=None, **kwargs):
        # If no route is chosen return index
        if route is None:
            template = env.get_template('stats.html')
            return template.render(cdn_environment=self.getCDN(server_mode))
        # Url is <domain>/stats/fighter
        elif route == "fighter":
            try:
                # Only accepts the 'name' GET parameter, otherwise index
                name = kwargs['name']
            except:
                template = env.get_template('stats.html')
                return template.render(
                    cdn_environment=self.getCDN(server_mode))
            return self.fighter(name)
    stats.exposed = True

    def checkDB(self):
        # Return boolean for whether or not the DB is able to connect.
        return (str(checkLoading()))
    checkDB.exposed = True


# Error page definitions /mappings
def error_page_404(status, message, traceback, version):
    template = env.get_template('404.html')
    cherrypy.response.status = 404
    return template.render(cdn_environment="http://cdn.fight.watch")
# Set the 404 page
cherrypy.config.update({'error_page.404':  error_page_404})


def startServer():
    # Set Cherrypy server settings depending on environment
    if server_mode == "dev":
        cherrypy.config.update({
                               'server.socket_host': '0.0.0.0',
                               'server.socket_port': 8000,
                               })
        conf = {
          '/static': {'tools.staticdir.on': True,
                      'tools.staticdir.dir': os.path.join(the_current_folder,
                                                          'static')
                      },
           '/static/css': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': os.path.join(the_current_folder, 'static/css')   # noqa
                },
           '/static/js': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': os.path.join(the_current_folder, 'static/js')  # noqa
                },
            '/static/images': {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': os.path.join(the_current_folder, 'static/images'),  # noqa
                'tools.staticdir.content_types': {'jpg': 'image/jpeg'}
                },
          'favicon.ico': {
                'tools.staticfile.on': True,
                'tools.staticfile.filename': os.path.join(the_current_folder, "static/favicon.ico")  # noqa
                }
          }

        cherrypy.quickstart(main_site(), config=conf)
    elif server_mode == "production":
        cherrypy.config.update({
            'environment': 'production',
            'log.screen': False,
            'log.error_file': '/home/thingdeux/webapps/fightwatch/fight.watch/error.log',  # noqa
            'server.socket_host': '127.0.0.1',
            'server.socket_port': 28921,
            })
        cherrypy.quickstart(main_site())


if __name__ == "__main__":
    # To start in dev mode pass 'dev' as a param to main.
    argument = sys.argv

    try:
        argument[1]
        if argument[1] == "dev":
            server_mode = "dev"
        else:
            server_mode = "production"
    except:
        server_mode = "production"

    # Make sure DB has tables and is active
    createSchema()
    startServer()
