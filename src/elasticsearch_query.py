# Cred is not included in the repo. Holds DB and elasticsearch connection info
from cred import get_elastic
import json
import sys

def match_query_by_name(name):
    query = "(name: *" + name.lower() + "*)"

    # Returns Hits / Shards / Took / Timed_out
    try:
        query = get_elastic().search(
            doc_type="matches",
            # Comma-Seperated string of fields to return
            fields="name",
            q=query,
            _source=False,
            explain=False
        )

        # Create a list with all of the names from the results
        # Cast the results into a set to remove duplicates
        final_names = set([
            results['fields']['name'][0]for results in query['hits']['hits']])

        # Create a python dictionary of the individual names as
        # JSON conversation of sets is not possible.
        to_return = {
            "names": [x for x in final_names]
        }

        return json.dumps(to_return)

    except Exception as err:
        print err
        return ("No Results Found or Major Error")


def get_fighter_winloss(names):
    name_list = names.split(',')
    query = "("
    if len(name_list) > 1:
        for count, name in enumerate(name_list):
            if count > 0:
                query = query + ' OR ' + '(raw_name: "' + str(name) + '")'
            else:
                # Should be the first or last in the series
                query = query + '(raw_name: "' + str(name) + '")'
    else:
        query = '(raw_name: "' + str(name_list[0]) + '")'    

    losses = get_elastic().count(
        index="levelup,nextlevel",
        doc_type="matches",
        q=query + ") AND (outcome: LOSS)"
    )

    wins = get_elastic().count(
        index="levelup,nextlevel",
        doc_type="matches",
        q=query + ") AND (outcome: WIN)"
    )

    return json.dumps({
        "wins": wins['count'],
        "losses": losses['count']
    })

if __name__ == "__main__":
    argument = sys.argv[1]
    match_query_by_name(argument)
