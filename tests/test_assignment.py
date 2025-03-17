import pytest
import sqlite3
import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app import create_user, delete_user, get_all_usernames, delete_post_from_user, get_posts_for_user, search_posts_by_keyword
import app

@pytest.fixture
def setup_db():
    # Setup a fresh database before each test
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT NOT NULL
    )
    """)
    app.cursor = cursor
    yield cursor
    conn.close()

def test_delete_user(setup_db):
    # Arrange
    create_user("alice", ["Post 1", "Post 2"])
    create_user("bob", ["Hello world!"])
    
    # Act
    delete_user("alice")
    
    # Assert
    usernames = get_all_usernames()
    assert "alice" not in usernames
    assert "bob" in usernames
    
def test_delete_post_from_user(setup_db):
    # Arrange
    create_user("alice", ["Post 1", "Post 2", "Post 3"])
    
    # Act
    delete_post_from_user("alice", 1)  # Delete the second post
    
    # Assert
    posts = get_posts_for_user("alice")
    assert len(posts) == 2
    assert "Post 2" not in posts
    
def test_search_posts_by_keyword(setup_db):
    # Arrange
    create_user("alice", ["Hello SQL!", "SQLite is great!"])
    create_user("mary", ["hello first post", "Learning today"])
    create_user("bob", ["My first post", "Learning SQL today"])    
    
    # Act
    result = search_posts_by_keyword("SQL")
    
    # Assert
    assert len(result) == 2
    assert '{"username": "alice", "posts": ["Hello SQL!", "SQLite is great!"]}' in result
    assert '{"username": "bob", "posts": ["My first post", "Learning SQL today"]}' in result
