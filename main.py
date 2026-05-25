from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException

from data import get_table_data, get_tables_meta, get_db_mb_size

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"null|http://192\.168\.\d+\.\d+.*|http://localhost.*",
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def status():
    return { 'status': 'ok' }

@app.get('/get-metas')
def get_metas():
    try:
        return get_tables_meta()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get('/get-table/{id}')
def get_table(id:str):
    try:
        return get_table_data(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get('/get-datastore-size')
def get_datastore_size():
    try:
        return { 'size-mb': get_db_mb_size() }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))