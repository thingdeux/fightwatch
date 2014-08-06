# Fight.Watch #

<img src="https://raw.github.com/thingdeux/fightwatch/master/static/images/example.png"></img>

## Summary ##
This is the code repository for the website [Fight.Watch](http://fight.watch), a fast web portal using twitch.tv API for easy access to fighting game streams. The fighting game community is growing quickly, to promote faster growth I created an easy way for fans or potential fans to quickly see the top active streams for the most popular fighting games.


## Of Note ##
* Dynamic shifting of boostrap column assignment based on number of streams twitch returns.
* Interesting implementation of passing CDN prefix to jinja templates in production while allowing for local static testing in dev.

### Technology Used ###

* Python 2.7
* CherryPy
* SQLAlchemy (and mySQL)
* Jinja2
* Twitch.API
