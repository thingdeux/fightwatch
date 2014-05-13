import requests
from database import Stream, multiStreamInsert

TWITCH_API_URL = "https://api.twitch.tv/kraken"
STREAMS_TO_QUERY = ["Street Fighter", "Ultimate Marvel", "King of Fighter", 
					"Injustice", "Super Smash", "Mortal Kombat", "Killer Instinct" ]

GAME_VERIFICATION = []
STREAM_LIMIT = 4

def loadStreams(search_phrases):
	def queryTwitch(query):
		query_url = TWITCH_API_URL + "/search/streams?q="
		limit = "&limit=" + str(STREAM_LIMIT)
		r = requests.get(query_url + str(query) + limit)		
		return r.json()

	sending_to_db = []
	for search_phrase in search_phrases:		
		for stream in queryTwitch(search_phrase)['streams']:			
			for a_game in STREAMS_TO_QUERY:				
				if a_game.lower() in str(stream['game']).lower():
					#Can be inserted into the DB because they match the query (sometimes weird twitch streams are returned)
					#Filtering them out					
					sending_to_db.append(
						Stream(game=search_phrase, display_game=stream['game'], url=stream['channel']['url'], 
							preview_location=stream['preview']['medium'],channel_name=stream['channel']['display_name'], viewers=stream['viewers'])
					)
	multiStreamInsert(sending_to_db)
					

					
			


			

	
	#return (json_dict)
	#Convert into format for inserting DB Stream records.
	#for game in json_dict

#Polls twitch for different variations of game names ex: Street Fighter II, Street Fighter EX
#Used to verify that only certain games are being returned.
def loadGamesVerification(search_phrases):
	returned_list = {}
	built_url = "https://api.twitch.tv/kraken/search/games?q="	
	typie = "&type=suggest"

	for phrase in search_phrases:
		r = requests.get(built_url + str(phrase) + typie)		
		for thing in r.json()['games']:
			try:
				returned_list[phrase].append(str(thing['name']) )
			except:
				returned_list[phrase] = [str(thing['name']),]

	return (returned_list)

if __name__ == "__main__":	
	#modified_query = STREAMS_TO_QUERY
	#Custom Rule because twitch doesn't consider Street Fighter and Super Street Fighter to be equal
	#modified_query.append("Super Street Fighter")
	#modified_query.append("The King of Fighters")
	#modified_query.append("Injustice: Gods Among Us")
	#modified_query.append("Super Smash Brothers")
	#GAME_VERIFICATION = loadGamesVerification(modified_query)
	loadStreams(STREAMS_TO_QUERY)