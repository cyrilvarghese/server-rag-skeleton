import sqlite3
from typing import List, Dict, Any
from pydantic import BaseModel

from sqlite_apis.data.model import Role, Tag

db_path = '../server/sqlite_apis/data/singular-db.sqlite'

def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn