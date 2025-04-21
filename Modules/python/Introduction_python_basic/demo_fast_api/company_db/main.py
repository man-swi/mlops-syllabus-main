from fastapi import FastAPI
from company_service.routers.router import router
import sqlite3

app = FastAPI()

app.include_router(router)


def _create_tables(db):
    """
    Create tables required for company for work
    """
    cur = db.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS employees
                 (id INTEGER PRIMARY KEY, name TEXT, email TEXT, department TEXT)''')
    db.commit()

@app.on_event("startup")
def startup_event():
    db = sqlite3.connect('company.db', check_same_thread=False)
    _create_tables(db)
    app.state.db = db

