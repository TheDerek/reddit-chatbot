import sqlite3 as lite
import sys
import json
import os
import util


def create_tables(cursor):
    sql = cursor

    # Create the comments table
    sql.execute('''CREATE TABLE comments (id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL UNIQUE, body TEXT NOT NULL, score INTEGER,
      parent_name TEXT, subreddit TEXT, FOREIGN KEY (parent_name) REFERENCES
      comments (name))''')

    # Create the table of all terms used in the comments
    sql.execute('''CREATE TABLE terms (id INTEGER PRIMARY KEY AUTOINCREMENT,
      term TEXT NOT NULL UNIQUE, frequency INTEGER NOT NULL)''')

    # Create the table which links the comments to the terms
    sql.execute('''CREATE TABLE comment_terms (id INTEGER PRIMARY KEY AUTOINCREMENT,
      term_id INTEGER NOT NULL, frequency INTEGER NOT NULL, comment_id INTEGER
      NOT NULL, FOREIGN KEY (comment_id) REFERENCES comments (id), FOREIGN KEY
      (term_id) REFERENCES terms (id) )''')


def fill_tables(comments, cursor):
    # Fill the comments table
    rows = []
    for comment in comments:
        rows.append((comment['name'], comment['body'], comment['score'],
                     comment['parent_id'], comment['subreddit']))

    cursor.executemany('''INSERT INTO comments (name, body, score, parent_name,
      subreddit) VALUES (?, ?, ?, ?, ?)''', rows)

    # Fill the comment terms table
    terms = {}
    comment_terms = ()
    for comment in comments:
        words = util.tokenize(comment['body'], stopwords)
        for term in words:
            if term not in terms:
                terms[term] = 1
            else:
                terms[term] += 1




if __name__ == '__main__':
    # Setup
    file_name = sys.argv[1]
    database_name = file_name + ".db"
    stopwords = open("assets/stopwords.txt").readlines()

    # Remove any existing databases
    print("Saving '" + file_name + "' to '" + database_name + "'.")
    os.remove(database_name)

    # Initiate the database
    con = lite.connect(database_name)
    cursor = con.cursor()
    create_tables(cursor)

    # Open up the data we will use to create the database
    data = open(file_name, 'r').read()
    comments = json.loads(data)

    # Fill the tables with data
    fill_tables(comments, cursor)

    con.commit()
    con.close()
