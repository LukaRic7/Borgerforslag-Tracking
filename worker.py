from datetime import datetime, timedelta, timezone
import time

from data import appened_new_votes, create_new_table
from fetching import fetch_all

def seconds_until_next_3rd_hour():
    """
    **Get the amount of seconds until the next 3rd hour.**
    
    *Returns*:
    - (int): The amount of seconds until the next 3rd hour.
    """

    now = datetime.now(tz=timezone.utc)

    next_hour = ((now.hour // 3) + 1) * 3

    if next_hour >= 24:
        next_time = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
    else:
        next_time = now.replace(hour=next_hour, minute=0, second=0, microsecond=0)

    return int((next_time - now).total_seconds())

def run_worker():
    while True:
        suggestions = fetch_all()
        print(f'Fetching borgerforslag, found: {len(suggestions)}', flush=True)

        for suggestion in suggestions:
            try:
                appened_new_votes(
                    suggestion.get('id'), suggestion.get('votes'),
                    suggestion.get('fetched_ts')
                )
            except FileNotFoundError:
                print(f'New borgerforslag detected, ID: {suggestion.get("id")}', flush=True)
                create_new_table(suggestion)

        sleep_time = seconds_until_next_3rd_hour()
        print(f'Sleeping for {sleep_time:,} seconds before fetching again.', flush=True)

        time.sleep(sleep_time)

if __name__ == '__main__':
    run_worker()