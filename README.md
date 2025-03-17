# Skipping Data Modeling

When working with SQLite, you don't always need to design complex relational
schemas—sometimes, storing Python dictionaries as plain text can be a quick
and flexible alternative. By converting dictionaries to strings using
`str()` or `json.dumps()`, developers can store structured data in a
single `TEXT` column without needing multiple tables. This approach is useful
for small-scale applications, prototyping, or cases where data retrieval
doesn't require complex queries. In this tutorial, we’ll explore how to
store, retrieve, and manipulate dictionary data efficiently within SQLite
using Python.

# Table setup

For this tutorial, we can create a simple SQLite table with a TEXT column
to store Python dictionaries as strings. Here’s a basic CREATE TABLE
statement:

```
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL
);

INSERT INTO users (data) VALUES 
('{"username": "alice", "posts": ["Hello world!", "SQLite is great!", "Storing Python dicts as text!"]}'),
('{"username": "bob", "posts": ["My first post", "Learning SQL today"]}'),
('{"username": "charlie", "posts": ["Just joined!", "Excited to be here!", "Exploring databases", "This is fun!"]}');
```

## Notes

  - id: A unique, auto-incremented identifier for each entry.
  - data: A TEXT field where we store Python dictionaries as JSON strings.


# Query with TEXT/JSON fields

SQLite provides built-in JSON functions that allow us to query and extract data directly. Here's how to retrieve all posts for a particular user using only SQLite:  

### Query to Retrieve Posts for a Specific User  
```sql
SELECT json_extract(data, '$.posts') 
FROM users 
WHERE json_extract(data, '$.username') = 'alice';
```

### Explanation:  
- `json_extract(data, '$.username')`: Extracts the `username` field from the stored JSON.  
- `json_extract(data, '$.posts')`: Retrieves the `posts` list for the matching user.  
- The `WHERE` clause ensures we only get posts for the specified user.  

Here's a link to sqlite's json_extract function so you can learn more about it: [https://www.sqlite.org/json1.html#jex](https://www.sqlite.org/json1.html#jex)

# Python and JSON

In Python, you can easily convert a dictionary to a JSON-formatted string using the `json` module, which allows you to store the dictionary as text in a database. This is useful because SQLite doesn’t have a native dictionary type, but it can store text, which JSON provides a structured way to represent.  

## Converting a Dictionary to JSON (for storing in SQLite)  
```python
import json

data = {"username": "alice", "posts": ["Hello world!", "SQLite is great!"]}
json_text = json.dumps(data)  # Convert dictionary to JSON string
print(json_text)  # Output: '{"username": "alice", "posts": ["Hello world!", "SQLite is great!"]}'
```

## Converting JSON Text Back to a Dictionary (for retrieving from SQLite)  
```python
dict_data = json.loads(json_text)  # Convert JSON string back to a dictionary
print(dict_data["username"])  # Output: alice
```

Using `json.dumps()` and `json.loads()`, you can store and retrieve Python dictionaries as structured text in SQLite while maintaining flexibility in your data structure.

# Full Example

In the file `app.py`, you will find a full CRUD example that has the following features:

  - Retrieve all usernames.
  - Retrieve all posts for a particular user.
  - Add a post for a user.

You will also noticed there are 3 functions not implemented.  Your assignment is to implement
those 3 functions and add them to the UI.

During development, you may want to reset the database by running the
following in the terminal:

```
sqlite3 posts.db < reset.sql
```