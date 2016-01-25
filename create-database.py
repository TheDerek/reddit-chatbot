import sqlite3 as lite
import sys
import json
import os
import util


def create_tables(cursor):
    sql = cursor

    print("Creating tables....")
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
      term TEXT NOT NULL, frequency INTEGER NOT NULL, comment_name TEXT
      NOT NULL, FOREIGN KEY (comment_name) REFERENCES comments (name), FOREIGN KEY
      (term) REFERENCES terms (term) )''')

    con.commit()


def fill_tables(comments, cursor):
    # Fill the comments table
    rows = []
    for comment in comments:
        rows.append((comment['name'], comment['body'], comment['score'],
                     comment['parent_id'], comment['subreddit']))

    cursor.executemany('''INSERT INTO comments (name, body, score, parent_name,
      subreddit) VALUES (?, ?, ?, ?, ?)''', rows)
    con.commit()


    # Fill the comment terms table
    print("Indexing terms...")
    comment_count = len(comments)
    table_terms = {}
    table_comment_terms = []
    progress = 0

    # Loop through all comments
    for index, comment in enumerate(comments):
        terms = util.tokenize(comment['body'], stopwords)
        comment_terms = {}

        # Loop through all terms in a comment
        for term in terms:

            # Add terms to the term table
            if term not in table_terms:
                table_terms[term] = 1
            else:
                table_terms[term] += 1

            # Add terms to the comment_terms record
            if term not in comment_terms:
                comment_terms[term] = 1
            else:
                comment_terms[term] += 1

        # Create the comment_terms records for future serialising
        for term, frequency in comment_terms.items():
            table_comment_terms.append((term, frequency, comment['id']))

        if (index / comment_count) * 100 > progress:
            print(str(progress) + "%")
            progress += 10

    # Add the gathered data to the database
    print("Adding index data to database...")

    rows = [(term, frequency) for term, frequency in table_terms.items()]
    cursor.executemany('''INSERT INTO terms (term, frequency) VALUES
      (?, ?)''', rows)

    cursor.executemany('''INSERT INTO comment_terms
      (term, frequency, comment_name) VALUES (?, ?, ?)''', table_comment_terms)
    con.commit()


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
