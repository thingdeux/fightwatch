# Cred is not included in the repo. Holds DB and elasticsearch connection info
from cred import get_elastic
import json
import sys


def match_query_by_name(name):
    query = {
        "query": {
            "fuzzy": {
                "name": "*" + name + "*"
            }
        }
    }

    # Returns Hits / Shards / Took / Timed_out
    try:
        query = get_elastic().search(
            # index="levelup",
            doc_type="matches",
            # Comma-Seperated string of fields to return
            fields="name",
            body=json.dumps(query),
            _source=False,
            explain=False
        )

        # Create a list with all of the names from the results
        # Cast the results into a set to remove duplicates
        final_names = set([
            results['fields']['name'][0]for results in query['hits']['hits']])

        print final_names
    except Exception as err:
        print err

if __name__ == "__main__":
    argument = sys.argv[1]
    match_query_by_name(argument)
