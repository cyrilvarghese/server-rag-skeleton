import sqlite3
from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from sqlite_apis.data.model import Role, Tag
roles_router = APIRouter();

db_path = '../server/sqlite_apis/data/singular-db.sqlite'

def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@roles_router.get("/{role_id}/tags", response_model=List[Tag])
async def read_tags_by_role(role_id: int):
    """API endpoint to fetch tags associated with a role ID."""
    try:
        tags = get_tags_by_role_id(role_id)
        if not tags:
            raise HTTPException(status_code=404, detail="No tags found for this role")
        return tags
    except sqlite3.DatabaseError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
def get_tags_by_role_id(role_id: int) -> List[Dict[str, Any]]:
    """Retrieve tags for a given role ID from the database."""
    conn = get_db_connection();
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT Tags.id, Tags.name, Tags.description, Tags.color
        FROM Tags
        INNER JOIN Roles_Tags ON Tags.id = Roles_Tags.tag_id
        WHERE Roles_Tags.role_id = ?
    """, (role_id,))

    rows = cursor.fetchall()
    tags = [dict(row) for row in rows]

    cursor.close()
    conn.close()

    return tags



def get_role_with_tags(role_id: int) -> Dict[str, Any]:
    """Retrieve a role and its associated tags from the database."""
    conn = get_db_connection();
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Fetch the role details
    cursor.execute("""
        SELECT id, name, description
        FROM Roles
        WHERE id = ?
    """, (role_id,))
    role_row = cursor.fetchone()

    if role_row is None:
        return {}

    role = dict(role_row)

    # Fetch the associated tags
    cursor.execute("""
        SELECT Tags.id, Tags.name, Tags.description, Tags.color
        FROM Tags
        INNER JOIN Roles_Tags ON Tags.id = Roles_Tags.tag_id
        WHERE Roles_Tags.role_id = ?
    """, (role_id,))

    tags_rows = cursor.fetchall()
    role['allowed_tags'] = [dict(tag) for tag in tags_rows]

    cursor.close()
    conn.close()

    return role

@roles_router.get("/{role_id}", response_model=Role)
async def read_role_with_tags(role_id: int):
    """API endpoint to fetch a role and its associated tags."""
    role = get_role_with_tags(role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role