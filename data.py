import os, json, subprocess

DATASTORE_PATH = os.path.join(os.path.dirname(__file__), 'datastore')

def __read(filename:str, datastore_path:str=DATASTORE_PATH) -> dict:
    """
    **Read a files content, parsing it to json format.**
    
    *Parameters*:
    - `filename` (str): The name of the file to read.
    - `datastore_path` (str): The path to the files directory. Defaults to a
    relative path from this scripts location.
    
    *Returns*:
    - (dict): The file content.
    """

    with open(os.path.join(datastore_path, filename), 'r') as file:
        return json.load(file)

def __write(filename:str, data:dict, datastore_path:str=DATASTORE_PATH):
    """
    **Write a dictionary to a file, overwriting all its content.**
    
    *Parameters*:
    - `filename` (str): The name of the file to write to.
    - `data` (dict): The data to write to the file.
    - `datastore_path` (str): The path to the files directory. Defaults to a
    relative path from this scripts location.
    """

    with open(os.path.join(datastore_path, filename), 'w') as file:
        json.dump(data, file)

def get_table_data(id:str) -> dict:
    """
    **Read a tables (borgerforslag) data.**
    
    *Parameters*:
    - `id` (str): The tables ID.
    
    *Returns*:
    - (dict): The borgerforslag data.
    """

    return __read(id + '.json')

def appened_new_votes(id:str, votes:int, timestamp:int):
    """
    **Append a new entry of votes to a table (borgerforslag).**
    
    *Parameters*:
    - `id` (str): The ID of the table.
    - `votes` (int): The new amount of votes.
    - `timestamp` (int): The unix timestamp in UTC timezone of when the votes
    was grabbed.
    """

    filename = id + '.json'

    data:dict = __read(filename)

    registered_votes:list = data.get('votes', [])
    registered_votes.append({ 'votes': votes, 'timestamp': timestamp })

    __write(filename, data)

def create_new_table(initial_data:dict):
    """
    **Create a new table (borgerforslag) if one doesn't already exist.**
    
    Raises FileExistsError if the file already exists.

    *Parameters*:
    - `initial_data` (dict): Initial data, must contain the id, title, creation
    timestamp, current votes and a timestamp of when the data was fetched.
    """
    filename = initial_data.get('id') + '.json'

    if os.path.exists(os.path.join(DATASTORE_PATH, filename)):
        raise FileExistsError(f'"{filename}" already exists.')

    __write(filename, {
        'title': initial_data.get('title', 'INGEN TITEL'),
        'created_ts': initial_data.get('created_ts', 0),
        'votes': [{
            'votes': initial_data.get('votes', -1),
            'timestamp': initial_data.get('fetched_ts', 0)
        }]
    })

def get_tables_meta() -> list[str]:
    """
    **Get a list all all the tables in the datastore.**
    
    *Returns*:
    - (list[str]): A list of all table (borgerforslag) IDs that is registered.
    """
    files = os.listdir(DATASTORE_PATH)

    return [f.replace('.json', '') for f in files if f.endswith('.json')]

def get_db_mb_size() -> float:
    """
    **Get the entrie datastores size in megabytes.**
    
    *Returns*:
    - (float): The amount of megabytes the entire datastore takes up.
    """

    total_bytes = subprocess.run(['du', '-sb', 'datastore'],
                                 capture_output=True,
                                 text=True)
    
    return int(total_bytes.stdout.split()[0]) / (1024 * 1024)