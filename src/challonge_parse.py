import challonge
import json


try:
    open_cred_file = open("cred.json", 'r')
    # Read values from json creds file [Not pushed to Repo]
    cred = json.loads(open_cred_file.read())
    username = cred['credentials']['username']
    api_key = cred['credentials']['APIKEY']
    # register challonge credentials
    challonge.set_credentials(username, api_key)
except Exception as err:
    print err


# Participant class definition
class Player:
    def __init__(self, player_data):
        try:
            self.id = player_data['id']
            self.name = player_data['name']
            self.matches = []
            self.opponent_history = {}
            self.final_rank = player_data['final-rank']
        except Exception as err:
            print err
            return None

    # Add the results of a match
    def add_match(self, opponent, outcome, tournament):
        try:
            self.matches.append([opponent,
                                outcome,
                                tournament])
        except Exception as err:
            print err

    # Track rounds won and loss against a particular opponent
    def track_sets(self, opponent, wins, losses):
        try:
            # Add an opponents
            self.opponent_history[opponent][0] += wins
            self.opponent_history[opponent][1] += losses
        except:
            self.opponent_history[opponent] = [wins, losses]


def process_tournament_matches(subdomain, tournament_url):
    if subdomain is not False:
        tournament_url_or_id = subdomain + "-" + tournament_url
    # Retrieve a tournament by its id (or its url)
    tournament = challonge.tournaments.show(tournament_url_or_id)
    tournament_name = tournament['name']
    # tournament_date = tournament['start-at']
    # Retrieve participant information for the tournament
    participants = challonge.participants.index(tournament_url_or_id)
    # Retrieve match information for the tournament
    matches = challonge.matches.index(tournament_url_or_id)
    players = {}

    # Build list of participants for tournament
    for participant in participants:
        try:
            players[participant['id']] = Player(participant)
        except Exception as err:
            print err

    # Iterate over each match and update player class
    for match in matches:
        winner = players[match['winner-id']]
        loser = players[match['loser-id']]
        winner.add_match(loser.name, "WIN", tournament_name)
        loser.add_match(winner.name, "LOSS", tournament_name)

        """
        Match sets are provided as wins-losses
        split them into a list with just the ints
        """
        match_score = match['scores-csv'].split('-')
        winner.track_sets(loser.name, int(match_score[0]), int(match_score[1]))
        loser.track_sets(winner.name, int(match_score[1]), int(match_score[0]))

process_tournament_matches('nextlevel', 'nlbc82usf4')
