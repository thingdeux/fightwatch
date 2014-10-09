from challonge_parse import process_tournament_matches
from elasticsearch import Elasticsearch
import json
import sys
# Cred is not included in the repo. Holds DB and elasticsearch connection info
from cred import get_elastic


def create_player_data(player_data, index):
    print player_data['sets']


def create_match_data(player_data, index):
    for player in player_data:
        create_player_data(player, index)
        # Index (add) each match into elasticsearch
        for match in player['matches']:
            get_elastic().index(id=None,
                                index=player['index'],
                                doc_type="matches",
                                body=match)


def process_tournament(subdomain, url):
    # Get Tournament data back as JSON
    tournament_data = process_tournament_matches(subdomain, url)
    index = tournament_data['INDEX']
    create_match_data(tournament_data['DATA'], index)


def initial_elastic_load(set_to_load="all"):
    sets = {}
    # Wednesday Night Fights URLS
    sets['wnf'] = (
        # 2014

        # Season 3
        ('levelup', 'wnf2014_3_1_usf4'),
        ('levelup', 'wnf2014_3_2_usf4'),
        ('levelup', 'wnf2014_3_3_usf4'),
        ('levelup', 'wnf2014_3_4_usf4'),
        ('levelup', 'wnf2014_3_5_usf4'),
        ('levelup', 'wnfae2014_3_6_usf4'),
        ('levelup', 'wnfae2014_3_7_usf4'),
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
        ('levelup', 'wnfae2014_1_2_ae'),
        # 2013

        # Season 5
        ('levelup', 'wnfae2013_5_7_ae'),
        ('levelup', 'wnfae2013_5_6_ae'),
        ('levelup', 'wnfae2013_5_5_ae'),
        ('levelup', 'wnfae2013_5_4_ae'),
        ('levelup', 'wnfae2013_5_3_ae'),
        ('levelup', 'wnfae2013_5_1_ae'),
        # Season 4
        ('levelup', 'wnfae2013_4_6_ae'),
        ('levelup', 'wnfae2013_4_5_ae'),
        ('levelup', 'wnfae2013_4_4_ae'),
        ('levelup', 'wnfae2013_4_3_ae'),
        ('levelup', 'wnfae2013_4_1_ae'),
        # Season 3
        ('levelup', 'wnfae2013_ae_3_5'),
        ('levelup', 'wnfae2013_ae_3_4'),
        ('levelup', 'wnfae2013_ae_3_3'),
        ('levelup', 'wnfae2013_ae_3_1'),
        # Season 2
        ('levelup', 'wnfae2013_ae_2_7'),
        ('levelup', 'wnfae2013_ae_2_4'),
        ('levelup', 'wnfae2013_ae_2_3'),
        # Season 1
        ('levelup', 'wnfae2013_1_13_ae_se'),
        ('levelup', 'wnfae2013_1_12_ae_se'),
        ('levelup', 'wnfae2013_ae_1_11_se'),
        ('levelup', 'wnfae2013_ae_1_9_se'),
        ('levelup', 'wnfae2013_ae_1_8_se'),
        ('levelup', 'wnfae2013_ae_1_7_se'),
        ('levelup', 'wnfae2013_ae_1_6_se'),
        ('levelup', 'wnfae2013_ae_1_5_se'),
        ('levelup', 'wnfae2013_ae_1_4_se'),
        ('levelup', 'wnfae2013_ae_1_3_s'),
        ('levelup', 'wnfae2013_ae_1_2_s'),
        ('levelup', 'wnfae2013_ae_1_1_s'),

        # 2012
        # Season 6
        ('levelup', 'wnfae_ae_6_3'),
        # Season 5
        ('levelup', 'wnfae_ae_5_6'),
        ('levelup', 'wnfae_ae_5_5'),
        # Season 4
        ('levelup', 'wnfae2012_ae_4_4'),
        ('levelup', 'wnfae2012_AE_4_3'),
        ('levelup', 'wnfae2012_ae_4_2'),
        ('levelup', 'wnfae2012_ae_4_1'),
        # 4th of July
        ('levelup', 'wnfae_ae_4th'),
        # Season 3
        ('levelup', 'wnfae_AE_3_7'),
        ('levelup', 'wnfae_AE_3_6'),
        ('levelup', 'wnfae_AE_3_5'),
        ('levelup', 'wnfae_AE_3_4'),
        ('levelup', 'wnfae_AE_3_3'),
        ('levelup', 'ae_3_2'),
        # Season 2
        ('levelup', 'ae_2_7'),
        ('levelup', 'wnfae_AE_2_6')
    )
    # NLBC
    sets['nlbc'] = (
        # 2013
        ('nextlevel', 'NLBC1AE'),
        ('nextlevel', 'NLBC2AE'),
        ('nextlevel', 'NLBC3AE'),
        ('nextlevel', 'NLBC4AE'),
        ('nextlevel', 'NLBC5AE'),
        ('nextlevel', 'NLBC6AE2012'),
        ('nextlevel', 'NLBC7AE2012'),
        ('nextlevel', 'NLBC8AE2012'),
        ('nextlevel', 'NLBC9AE2012'),
        ('nextlevel', 'NLBC10AE2012'),
        ('nextlevel', 'NLBC11AE2012'),
        ('nextlevel', 'NLBC12AE2012'),
        ('nextlevel', 'NLBC13AE2012'),
        ('nextlevel', 'NLBC14AE2012'),
        ('nextlevel', 'NLBC15AE2013'),
        ('nextlevel', 'NLBC16AE2012'),
        ('nextlevel', 'NLBC17AE2012'),
        ('nextlevel', 'NLBC18AE2012'),
        ('nextlevel', 'NLBC19AE2012'),
        ('nextlevel', 'NLBC20AE2012'),
        ('nextlevel', 'NLBC21AE2012'),
        ('nextlevel', 'NLBC22AE2012'),
        ('nextlevel', 'NLBC23AE2012'),
        ('nextlevel', 'NLBC24AE2012'),
        ('nextlevel', 'NLBC25AE2012'),
        ('nextlevel', 'NLBC26AE2012'),
        ('nextlevel', 'NLBC27AE2012'),
        ('nextlevel', 'NLBC28AE2012'),
        ('nextlevel', 'NLBC29AE2012'),
        ('nextlevel', 'NLBC30AE2012'),
        ('nextlevel', 'NLBC31AE2012'),
        ('nextlevel', 'NLBC32AE2012'),
        ('nextlevel', 'NLBC33AE2012'),
        ('nextlevel', 'NLBC34AE2012'),
        ('nextlevel', 'NLBC35AE2012'),
        ('nextlevel', 'NLBC36AE2012'),
        ('nextlevel', 'NLBC37AE2012'),
        ('nextlevel', 'NLBC38AE2012'),
        ('nextlevel', 'NLBC39AE2012'),
        ('nextlevel', 'NLBC40AE2012'),
        ('nextlevel', 'NLBC41AE2012'),
        ('nextlevel', 'NLBC42AE2012'),
        ('nextlevel', 'NLBC43AE2012'),
        ('nextlevel', 'NLBC44AE2012'),
        ('nextlevel', 'NLBC45AE2012'),
        ('nextlevel', 'NLBC46AE2012'),
        ('nextlevel', 'NLBC47AE2012'),
        ('nextlevel', 'NLBC48AE2012'),
        ('nextlevel', 'NLBC49AE2012'),
        ('nextlevel', 'NLBC50AE2012'),
        ('nextlevel', 'NLBC51AE2012'),

        # 2014
        ('nextlevel', 'nlbc90usf4'),
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
        ('nextlevel', 'NLBC52AE2012')
    )
    # Big Two
    sets['bigtwo'] = (
        # 2012
        ('nextlevel', 'bigtwo27ae'),
        ('nextlevel', 'bigtwo29ae'),
        ('nextlevel', 'bigtwo30ae'),
        ('nextlevel', 'bigtwo31ae'),
        ('nextlevel', 'bigtwo32ae'),
        ('nextlevel', 'bigtwo33ae'),
        ('nextlevel', 'bigtwo35AE'),
        ('nextlevel', 'bigtwo36ae'),
        ('nextlevel', 'bigtwo37ae'),
        ('nextlevel', 'bigtwo38AE'),
        ('nextlevel', 'bigtwo39ae'),
        ('nextlevel', 'Bigtwo40AE'),
        ('nextlevel', 'bigtwo41AE'),
        ('nextlevel', 'bigtwo42ae'),
        ('nextlevel', 'bigtwo43ae'),
        ('nextlevel', 'bigtwo44ae'),
        ('nextlevel', 'bigtwo45ae'),
        ('nextlevel', 'bigtwo47ae'),
        ('nextlevel', 'bigtwo48AE'),
        ('nextlevel', 'bigtwo49AE'),
        ('nextlevel', 'bigtwo50AE'),
        ('nextlevel', 'bigtwo51AE'),
        ('nextlevel', 'bigtwo52AE'),
        ('nextlevel', 'bigtwo53ae'),
        ('nextlevel', 'bigtwo54AE'),
        ('nextlevel', 'bigtwo55AE'),
        ('nextlevel', 'bigtwo56AE'),
        ('nextlevel', 'bigtwo57AE'),
        ('nextlevel', 'bigtwo58AE')
    )
    # Majors
    sets['majors'] = (
        # Sega Cup
        ('levelup', 'segacup2014_pool1'),
        ('levelup', 'segacup2014_pool2'),
        ('levelup', 'segacup2014_pool3'),
        ('levelup', 'segacup2014_pool4'),
        ('levelup', 'segacup2014_pool5'),
        ('levelup', 'segacup2014_pool6'),
        ('levelup', 'segacup2014_pool7'),
        ('levelup', 'segacup2014_pool8'),
        ('levelup', 'segacup2014_top16'),
        # SoCal Regionals 2014
        ('levelup', 'scr2014_ae_pool1'),
        ('levelup', 'scr2014_ae_pool2'),
        ('levelup', 'scr2014_ae_pool3'),
        ('levelup', 'scr2014_ae_pool4'),
        ('levelup', 'scr2014_ae_pool5'),
        ('levelup', 'scr2014_ae_pool6'),
        ('levelup', 'scr2014_ae_pool7'),
        ('levelup', 'scr2014_ae_pool8'),
        ('levelup', 'scr2014_ae_pool9'),
        ('levelup', 'scr2014_ae_pool10'),
        ('levelup', 'scr2014_ae_pool11'),
        ('levelup', 'scr2014_ae_pool12'),
        ('levelup', 'scr2014_ae_pool13'),
        ('levelup', 'scr2014_ae_pool14'),
        ('levelup', 'scr2014_ae_pool15'),
        ('levelup', 'scr2014_ae_pool16'),
        ('levelup', 'scr2014_ae_top32'),
        ('levelup', 'scr2014_ae_top8'),
        # Sega Cup 2013
        ('levelup', 'segacup_top16'),
        ('levelup', 'segacup_pool1'),
        ('levelup', 'segacup_pool2'),
        ('levelup', 'segacup_pool3'),
        ('levelup', 'segacup_pool4'),
        ('levelup', 'segacup_pool5'),
        ('levelup', 'segacup_pool6'),
        ('levelup', 'segacup_pool7'),
        ('levelup', 'segacup_pool8'),
        # SoCal Regionals 2013
        ('levelup', 'ae_top32_scr2013'),
        # SoCal Regionals 2011
        ('levelup', 'scr2011_ssf4ae'),
    )

    # Process one set of subdomain/url sets for tournaments
    def processSet(set_to_process):
        print ("Processing: " + set_to_process)
        for subdomain, url in sets[set_to_process]:
            try:
                print "Processing: " + str(url)
                process_tournament(subdomain, url)
            except Exception as err:
                print "Load Error"
                print err

    # Process all sets if nothing is passed to initial load func.
    if set_to_load == "all":
        for key in sets.keys():
            processSet(key)
    else:
        processSet(set_to_load)

if __name__ == "__main__":
    load_type = sys.argv[1]
    initial_elastic_load(load_type)

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
