# Fight.Watch #

This is the code repository for the website [Fight.Watch](http://fight.watch), a fast web portal using twitchs API for easy access to fighting game streams.

<img src="https://raw.github.com/thingdeux/fightwatch/master/static/images/example.phg"></img>

## Summary ##
The fighting game community is growing quickly, to promote more growth I created an easy way for fans or potential fans to quickly see the top active streams for their given fighting game.


## Of Note ##
* Dynamic boostrap column assignment bassed on number of streams twitch returned.
* Interesting implementation of passing CDN prefix to jinja templates in production while allowing for local static testing in dev.

### Technology Used ###

* Python 2.7
* CherryPy
* SQLAlchemy (and mySQL)
* Jinja2
* Twitch.API
