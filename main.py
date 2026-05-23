from fastapi import FastAPI, HTTPException

from data import get_table_data, get_tables_meta

app = FastAPI()

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