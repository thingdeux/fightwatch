# -*- coding: utf-8 -*-
import requests
from database import Stream, multiStreamInsert, setLoading

TWITCH_API_URL = "https://api.twitch.tv/kraken"
GAME_VERIFICATION = []
STREAM_LIMIT = 4


def loadStreams():
    # List of games to pass the queryTwitch function.
    STREAMS_TO_QUERY = ["Street Fighter", "Ultimate Marvel", "King of Fighter",
                        "Injustice", "Super Smash", "Mortal Kombat",
                        "Killer Instinct"]

    search_phrases = STREAMS_TO_QUERY

    def queryTwitch(query):
        query_url = TWITCH_API_URL + "/search/streams?q="
        limit = "&limit=" + str(STREAM_LIMIT)
        try:
            r = requests.get(query_url + str(query) + limit)
            return r.json()
        except:
            return (False)

    sending_to_db = []
    streamLoads = 0
    for search_phrase in search_phrases:
        try:
            results = queryTwitch(search_phrase)['streams']
        except:
            results = ""

        for stream in results:
            for a_game in STREAMS_TO_QUERY:
                try:
                    if a_game.lower() in stream['game'].encode("UTF-8").lower():  # noqa
                        # Can be inserted into the DB because they match the
                        # query (sometimes weird twitch streams are returned)
                        # Filtering them out
                        try:
                            trimmed_status = str(stream['channel']['status'])
                            if len(trimmed_status) < 1:
                                trimmed_status = str(stream['channel']
                                                     ['display_name'])
                        except:
                            trimmed_status = " - "

                        sending_to_db.append(
                            Stream(
                                game=search_phrase,
                                display_game=stream['game'],
                                url=stream['channel']['url'],
                                preview_location=stream['preview']['medium'],
                                channel_name=stream['channel']['display_name'],
                                viewers=stream['viewers'],
                                status=trimmed_status)
                        )
                        streamLoads = streamLoads + 1
                except:
                    pass

    # Verify at least one stream exists
    setLoading(True)
    if streamLoads >= 1:
        multiStreamInsert(sending_to_db)
    else:
        # No streams exist so call multistream
        # insert with no content to force delete.
        multiStreamInsert(False)

    setLoading(False)


# Polls twitch for different variations of game names
# ex: Street Fighter II, Street Fighter EX
# Used to verify that only certain games are being returned.
def loadGamesVerification(search_phrases):
    returned_list = {}
    built_url = "https://api.twitch.tv/kraken/search/games?q="
    typie = "&type=suggest"

    for phrase in search_phrases:
        r = requests.get(built_url + str(phrase) + typie)
        for thing in r.json()['games']:
            try:
                returned_list[phrase].append(str(thing['name']))
            except:
                returned_list[phrase] = [str(thing['name']), ]

    return (returned_list)

if __name__ == "__main__":
    loadStreams()
