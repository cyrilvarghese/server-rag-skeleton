from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sqlite3
from typing import Optional,List

from sqlite_apis.data.model import Tag
tags_router = APIRouter();
# Pydantic model to validate data


# Database connection function
def get_db_connection():
    conn = sqlite3.connect('../server/sqlite_apis/data/singular-db.sqlite')
    conn.row_factory = sqlite3.Row
    return conn

# CRUD Operations

# List all tags
@tags_router.get("/", response_model=list[Tag])
def list_tags():
    conn = get_db_connection()
    tags = conn.execute('SELECT id,name, description, color  FROM Tags').fetchall()
    conn.close()
    return [dict(tag) for tag in tags]
# Create a new tag
@tags_router.post("/", response_model=Tag)
def create_tag(tag: Tag):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Insert the new tag
    cursor.execute('INSERT INTO Tags (name, description, color) VALUES (?, ?, ?)', 
                   (tag.name, tag.description, tag.color))
    new_tag_id = cursor.lastrowid
    
    # Associate the tag with roles
    for role_id in tag.role_ids:
        try:
            cursor.execute('INSERT INTO Roles_Tags (role_id, tag_id) VALUES (?, ?)', 
                           (role_id, new_tag_id))
        except sqlite3.IntegrityError:
            conn.close()
            raise HTTPException(status_code=400, detail=f"Role ID {role_id} does not exist")
    
    conn.commit()
    conn.close()
    return {**tag.model_dump(), "id": new_tag_id}

# Read a single tag by ID
@tags_router.get("/{tag_id}", response_model=Tag)
def read_tag(tag_id: int):
    conn = get_db_connection()
    tag = conn.execute('SELECT * FROM Tags WHERE id = ?', (tag_id,)).fetchone()
    conn.close()
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return dict(tag)

# Update a tag
@tags_router.put("/{tag_id}", response_model=Tag)
def update_tag(tag_id: int, tag: Tag):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE Tags SET name = ?, description = ?, color = ? WHERE id = ?', 
                   (tag.name, tag.description, tag.color, tag_id))
    conn.commit()
    updated_tag = conn.execute('SELECT * FROM Tags WHERE id = ?', (tag_id,)).fetchone()
    conn.close()
    if updated_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return dict(updated_tag)

# Delete a tag
@tags_router.delete("/{tag_id}", response_model=Tag)
def delete_tag(tag_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    tag_to_delete = conn.execute('SELECT * FROM Tags WHERE id = ?', (tag_id,)).fetchone()
    if tag_to_delete is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Tag not found")
    cursor.execute('DELETE FROM Tags WHERE id = ?', (tag_id,))
    conn.commit()
    conn.close()
    return dict(tag_to_delete)

