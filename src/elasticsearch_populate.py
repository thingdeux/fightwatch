from challonge_parse import process_tournament_matches
from elasticsearch import Elasticsearch

# Connect to elasticsearch client
es = Elasticsearch()


def create_player_data(player_data, index, doc_type):
    test = 'Coming'


def create_match_data(player_data, index, doc_type):
    for player in player_data:
        for match in player['matches']:
            es.index(id=None,
                     index=player['index'],
                     doc_type=player['doc_type'],
                     body=match)


def process_tournament(subdomain, url):
    # Get Tournament data back as JSON
    tournament_data = process_tournament_matches(subdomain, url)
    index = tournament_data['INDEX']
    doc_type = tournament_data['DOC_TYPE']
    create_match_data(tournament_data['DATA'], index, doc_type)
    create_player_data(tournament_data['DATA'], index, doc_type)


def initial_elastic_load():
    # Wednesday Night Fights URLS
    wnf = (
        # Season 3
        ('levelup', 'wnf2014_3_1_usf4'),
        ('levelup', 'wnf2014_3_2_usf4'),
        ('levelup', 'wnf2014_3_3_usf4'),
        ('levelup', 'wnf2014_3_4_usf4'),
        ('levelup', 'wnf2014_3_5_usf4'),
        ('levelup', 'wnfae2014_3_6_usf4'),
        # Season 2
        ('levelup', 'wnfae2014_2_11_usf4'),
        ('levelup', 'wnfae2014_2_10_usf4'),
        ('levelup', 'wnfae2014_2_9_ae'),
        ('levelup', 'wnfae2014_2_8_ae'),
        ('levelup', 'wnfae2014_2_7_ae'),
        ('levelup', 'wnfae2014_2_6_ae'),
        ('levelup', 'wnfae2014_2_5_ae'),
        ('levelup', 'wnfae_2014_2_4_ae'),
        ('levelup', 'wnfae2014_2_3_ae'),
        ('levelup', 'wnfae2014_2_2_ae'),
        ('levelup', 'wnfae2014_2_1_ae'),
        # Season 1
        ('levelup', 'wnfae2014_1_11_ae'),
        ('levelup', 'wnfae2014_1_10_ae'),
        ('levelup', 'wnfae2014_1_8_ae'),
        ('levelup', 'wnfae2014_1_7_ae'),
        ('levelup', 'wnfae2014_1_6_ae'),
        ('levelup', 'wnfae2014_1_5_ae'),
        ('levelup', 'wnfae2014_1_4_ae'),
        ('levelup', 'wnfae2014_1_3_ae'),
        #('levelup', 'wnfae2014_1_2_ae')
    )
    # NLBC
    nlbc = (
        # 2014
        ('nextlevel', 'nlbc89usf4'),
        ('nextlevel', 'nlbc88usf4'),
        ('nextlevel', 'nlbc87usf4'),
        ('nextlevel', 'nlbc86_usf4'),
        ('nextlevel', 'nlbc85_usf4'),
        ('nextlevel', 'nlbc84usf4'),
        ('nextlevel', 'nlbc83_usf4'),
        ('nextlevel', 'nlbc82usf4'),
        ('nextlevel', 'nlbc81usf4'),
        ('nextlevel', 'nlbc80usf4'),
        ('nextlevel', 'nlbc79usf4'),
        ('nextlevel', 'nlbc78usf4'),
        ('nextlevel', 'nlbc77usf4'),
        ('nextlevel', 'nlbc76usf4'),
        ('nextlevel', 'nlbc75usf4'),
        ('nextlevel', 'nlbc74usf4'),
        ('nextlevel', 'nlbc73usf4'),
        ('nextlevel', 'nlbc72ae2012'),
        ('nextlevel', 'nlbc71ae2012'),
        ('nextlevel', 'nlbc70ae2012'),
        ('nextlevel', 'nlbc69ae2012'),
        ('nextlevel', 'nlbc68ae2012'),
        ('nextlevel', 'nlbc67ae2012'),
        ('nextlevel', 'NLBC66AE2012'),
        ('nextlevel', 'nlbc65ae2012'),
        ('nextlevel', 'nlbc64ae2012'),
        ('nextlevel', 'nlbc63ae2012'),
        ('nextlevel', 'nlbc62ae2012'),
        ('nextlevel', 'NLBC61AE2012'),
        ('nextlevel', 'nlbc60ae2012'),
        ('nextlevel', 'NLBC59AE2012'),
        ('nextlevel', 'NLBC58AE2012'),
        ('nextlevel', 'NLBC57AE2012'),
        ('nextlevel', 'NLBC56AE2012'),
        ('nextlevel', 'NLBC55AE2012'),
        ('nextlevel', 'NLBC54AE2012'),
        ('nextlevel', 'NLBC53AE2012'),
        #('nextlevel', 'NLBC52AE2012')
    )


    for subdomain, url in nlbc:
        try:
            print "Processing: " + str(url)
            process_tournament(subdomain, url)
        except Exception as err:
            print "Load Error"
            print err

    for subdomain, url in wnf:
        try:
            print "Processing: " + str(url)
            process_tournament(subdomain, url)
        except Exception as err:
            print "Load Error"
            print err


#initial_elastic_load()


"""
This needs to be added to the mapping configuration file
For ElasticSearch
.../config/mappings/_default

{
    "matches": {
        "properties": {
            "opponent": {
                "type": "multi_field",
                "fields": {
                    "opponent": {"type": "string", "index": "analyzed"},
                    "raw_opponent": {"type": "string", "index": "not_analyzed"}
                }
            }
        }
    }
}
"""
