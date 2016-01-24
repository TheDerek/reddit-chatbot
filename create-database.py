import sqlite3 as lite
import sys
import json
import os

if __name__ == '__main__':
    file_name = sys.argv[1]
    database_name = file_name + ".db"

    # Remove any existing databases
    print("Saving '" + file_name + "' to '" + database_name + "'.")
    os.remove(database_name)

    # Initiate the database
    con = lite.connect(database_name)
    sql = con.cursor()

    # Create the comments table
    sql.execute('''CREATE TABLE comments (id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL UNIQUE, body TEXT NOT NULL, score INTEGER,
      parent_name TEXT, subreddit TEXT, FOREIGN KEY (parent_name) REFERENCES
      comments (name))''')

    # Create the index tables
    sql.execute('''CREATE TABLE comment_terms (id INTEGER PRIMARY KEY AUTOINCREMENT,
      term NOT NULL, frequency INTEGER NOT NULL, comment_id INTEGER
      NOT_NULL, FOREIGN KEY (comment_id) REFERENCES comments (id))''')

    # Open up the data we will use to create the database
    data = open(file_name, 'r').read()
    comments = json.loads(data)

    rows = []
    for comment in comments:
        rows.append((comment['name'], comment['body'], comment['score'],
                     comment['parent_id'], comment['subreddit']))

    sql.executemany('''INSERT INTO comments (name, body, score, parent_name,
      subreddit) VALUES (?, ?, ?, ?, ?)''', rows)

    con.commit()
    con.close()
