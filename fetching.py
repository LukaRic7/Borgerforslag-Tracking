from datetime import datetime, timezone
import requests, re

USER_AGENT  = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36'
URL = 'https://www.borgerforslag.dk/api/proposals/search'
DANISH_MONTHS = {
    'januar': 'January', 'februar': 'February', 'marts': 'March',
    'april': 'April', 'maj': 'May', 'juni': 'June', 'juli': 'July',
    'august': 'August', 'september': 'September', 'oktober': 'October',
    'november': 'November', 'december': 'December',
}

__last_call_ts = 0

def __da2en_date(date:str) -> datetime:
    """
    **Convert a danish date string into a datetime object with the standard
    timezone as UTC.**
    
    *Parameters*:
    - `date` (str): The date to convert, fx "23. Maj 2026"
    
    *Returns*:
    - (datetime): The datetime object.
    """

    # Compile a pattern to recognize months
    pattern = re.compile(r'\b(' + '|'.join(DANISH_MONTHS.keys()) + r')\b')

    # Convert the danish months into english months using a map
    normalized = pattern.sub(lambda m: DANISH_MONTHS.get(m.group(0)), date)

    date_obj = datetime.strptime(normalized, '%d. %B %Y')
    return date_obj.replace(tzinfo=timezone.utc)

def get_next_call_ts() -> int:
    """
    **Get the UTC timestamp of when the next call is projected to happen.**
    
    *Returns*:
    - (int): The UTC timestamp.
    """

    return __last_call_ts + 60*60*3 # Assuming 3 hours intervals

def fetch_all(user_agent:str=USER_AGENT) -> list[dict]:
    """
    **Fetch all currently active borgerforslag and parse them into dicts.**
    
    Raises HTTPError when the fetch did not return OK.

    *Parameters*:
    - `user_agent` (str): Use a custom user agent when fetching. Has a default.
    
    *Returns*:
    - (list[dict]): A list of all the active borgerforslag.
    """

    global __last_call_ts

    payload = {
        'filter': 'active', 'sortOrder': 'NewestFirst',
        'searchQuery': '', 'pageNumber': 0, 'pageSize': 10_000
    }

    headers = {
        'User-Agent': user_agent, 'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br, zstd'
    }

    response = requests.post(URL, json=payload, headers=headers)
    response.raise_for_status()

    data:dict[str, list[dict]] = response.json()
    if not data: return []


    __last_call_ts = int(__da2en_date(suggestion.get('date')).timestamp())

    suggestions = []
    for suggestion in data.get('data'):
        if suggestion.get('status') != 'ongoing':
            continue

        # All dates are converted to UTC as a standard
        suggestions.append({
            'id': suggestion.get('externalId'),
            'title': suggestion.get('title'),
            'created_ts': __last_call_ts,
            'fetched_ts': int(datetime.now(tz=timezone.utc).timestamp()),
            'votes': suggestion.get('votes')
        })
    
    return suggestions