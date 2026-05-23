import time

from data import appened_new_votes, create_new_table
from fetching import fetch_all

FETCHING_INTERVAL_SEC = 3*60*60

def run_worker():
    while True:
        suggestions = fetch_all()
        print(f'Fetching borgerforslag, found: {len(suggestions)}')

        for suggestion in suggestions:
            try:
                appened_new_votes(
                    suggestion.get('id'), suggestion.get('votes'),
                    suggestion.get('fetched_ts')
                )
            except FileNotFoundError:
                print(f'New borgerforslag detected, ID: {suggestion.get('id')}')
                create_new_table(suggestion)

        time.sleep(FETCHING_INTERVAL_SEC)

if __name__ == '__main__':
    run_worker()