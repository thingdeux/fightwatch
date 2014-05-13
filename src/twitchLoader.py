import requests

STREAMS_TO_QUERY = ["Street Fighter", "Ultimate Marvel", "King of Fighter", 
					"Injustice", "Super Smash", "Mortal Kombat", "Killer Instinct" ]

def loadStreams(search_phrases):
	def queryTwitch(query):
		twitch_url = "https://api.twitch.tv/kraken/search/streams?q="
		limit = "&limit=4"
		r = requests.get(twitch_url + str(query) + limit)
		return r.json()

	json_dict = {}
	for search_phrase in search_phrases:
		json_dict[search_phrase] = queryTwitch(search_phrase)
	
	return (json_dict)




#returned_json = self.getStreams()

if __name__ == "__main__":
	loadStreams(STREAMS_TO_QUERY)