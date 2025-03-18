import sqlite3
import json

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("posts.db", isolation_level=None)

# Create users table with a JSON data column to store user details
conn.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL
)
""")

# Function to create a new user
def create_user(username, posts):
    data = {
        "username": username,
        "posts": posts
    }
    conn.execute("INSERT INTO users (data) VALUES (?)", (json.dumps(data),))
    return True

# Function to retrieve all usernames
def get_all_usernames():
    rows = conn.execute("SELECT json_extract(data, '$.username') FROM users").fetchall()
    return [row[0] for row in rows]

# Function to retrieve all posts for a particular user
def get_posts_for_user(username):
    #row = conn.execute("SELECT data FROM users WHERE json_extract(data, '$.username') = ?", (username,)).fetchone()
    row = conn.execute(
        "SELECT json_extract(data, '$.posts') FROM users WHERE json_extract(data, '$.username') = ?",
        (username,)).fetchone()
    return json.loads(row[0]) if row else []

# Function to add a post for a user
def add_post_for_user(username, post):
    row = conn.execute("SELECT data FROM users WHERE json_extract(data, '$.username') = ?", (username,)).fetchone()
    if row:
        user_data = json.loads(row[0])  # Convert JSON text back to dictionary
        user_data["posts"].append(post)
        conn.execute("UPDATE users SET data = ? WHERE json_extract(data, '$.username') = ?", 
                     (json.dumps(user_data), username))
        return True
    else:
        return False

# Function to delete a user
def delete_user(username):
    pass

# Function to delete a specific post for a user, post_index is the array index of the post
def delete_post_from_user(username, post_index):
    pass

# Function to search posts by a keyword and return users with the provided keyword in
# any of their posts.
#
# For instance, using our starter database, the function call
# search_posts_by_keyword('SQL') would return
#   [ {"username": "alice", "posts": ["Hello world!", "SQLite is great!", "Storing Python dicts as text!"]},
#     {"username": "bob", "posts": ["My first post", "Learning SQL today"]} ]
def search_posts_by_keyword(keyword):
    pass

# CLI Functionality
def main():
    while True:
        print("\nChoose an option:")
        print("1. Create user")
        print("2. List all usernames")
        print("3. Get posts for a user")
        print("4. Add post for a user")
        print("5. Delete user")
        print("6. Delete specific post for a user")
        print("7. Search posts by keyword")
        print("8. Exit")
        
        choice = input("Enter your choice: ")

        if choice == "1":
            username = input("Enter username: ")
            posts = input("Enter initial posts (comma-separated): ").split(",")
            posts = [post.strip() for post in posts]
            if create_user(username, posts):
                print()
                print(f'User {username} successfully created')

        elif choice == "2":
            print()
            print(get_all_usernames())

        elif choice == "3":
            username = input("Enter username to retrieve posts: ")
            print()
            print(get_posts_for_user(username))

        elif choice == "4":
            username = input("Enter username to add a post for: ")
            post = input("Enter the post content: ")
            print()
            if add_post_for_user(username, post):
                print("Post successfully added")
            else:
                print("Error adding post")

        elif choice == "8":
            print()
            print("Exiting...")
            break
        else:
            print()
            print("Invalid choice, please try again.")
    
    conn.close()
    print("Database connection closed.")

if __name__ == "__main__":
    main()
