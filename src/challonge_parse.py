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
            self.name = player_data['name'].lower()
            self.matches = []
            self.opponent_history = {}
            try:
                self.final_rank = int(player_data['final-rank'])
            except:
                # Catch Unfinished brackets where there is no "final" rank
                self.final_rank = 0

        except Exception as err:
            print err
            return None

    # Add the results of a match
    def add_match(self, opponent, outcome, tournament):
        try:
            self.matches.append({
                                "name": self.name,
                                "opponent": opponent,
                                "outcome": outcome,
                                "tournament": tournament
                                })
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
    tournament_date = tournament['started-at'].strftime("%Y-%m-%d")
    # Retrieve participant information for the tournament
    participants = challonge.participants.index(tournament_url_or_id)
    # Retrieve match information for the tournament
    matches = challonge.matches.index(tournament_url_or_id)
    players = {}

    # Clean up the class data and make it serializable
    def clean_data(players):
        final_data = {}
        if subdomain is not False:
            final_data['INDEX'] = subdomain
        else:
            final_data['INDEX'] = "FGC"
        final_data['DOC_TYPE'] = "tournament"
        final_data['DATA'] = []

        """
        Iterate over the passed player data and create
        Dictionaries that will be used to populate ElasticSearch
        """
        for key, value in players.iteritems():
            player = players[key]
            final_data['DATA'].append(
                {
                    "index": final_data['INDEX'],
                    "matches": player.matches,
                    "name": player.name,
                    "tournament": tournament_name,
                    "date": tournament_date,
                    "set_history": player.opponent_history,
                    "placed": player.final_rank,
                    "sets": player.opponent_history
                }
            )

        return final_data

    # Build list of participants for tournament
    for participant in participants:
        try:
            players[participant['id']] = Player(participant)
        except Exception as err:
            print err

    # Iterate over each match and update player class
    for match in matches:
        try:
            winner = players[match['winner-id']]
            loser = players[match['loser-id']]
            winner.add_match(loser.name, "WIN", tournament_name)
            loser.add_match(winner.name, "LOSS", tournament_name)

            """
            Match sets are provided as wins-losses
            split them into a list with just the ints
            """
            try:
                match_score = match['scores-csv'].split('-')
            except:
                match_score = [0, 0]
            winner.track_sets(loser.name, int(match_score[0]),
                              int(match_score[1]))
            loser.track_sets(winner.name, int(match_score[1]),
                             int(match_score[0]))
        except Exception as err:
            # If someone forgets to update the brackets and finish the event
            # You end up with no winners/losers in some slots
            pass

    return clean_data(players)
