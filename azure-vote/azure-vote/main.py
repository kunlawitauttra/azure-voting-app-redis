from flask import Flask, request, render_template
import os
import pymssql
import socket

app = Flask(__name__)

# Load configurations from environment or config file
app.config.from_pyfile('config_file.cfg')

# Azure SQL Database configurations
server = 'test-failover-group.database.windows.net'
username = 'testadmin'
password = '6yHnmju&'
database = 'test-sg-db'

# Change title to host name to demo NLB
if app.config['SHOWHOST'] == "true":
    title = socket.gethostname()

# Connect to Azure SQL Database
try:
    conn = pymssql.connect(server=server, user=username, password=password, database=database)
except pymssql.Error as e:
    exit(f'Failed to connect to Azure SQL Database: {e}')

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'GET':

        # Get current values from the database
        vote1, vote2 = get_votes_from_db()

        # Return index with values
        return render_template("index.html", value1=vote1, value2=vote2, button1=button1, button2=button2, title=title)

    elif request.method == 'POST':

        if request.form['vote'] == 'reset':
            # Empty the votes in the database
            reset_votes_in_db()

        else:
            # Insert vote result into DB
            vote = request.form['vote']
            add_vote_to_db(vote)

    # Get current values from the database
    vote1, vote2 = get_votes_from_db()

    # Return results
    return render_template("index.html", value1=vote1, value2=vote2, button1=button1, button2=button2, title=title)

def get_votes_from_db():
    # Get the current values of votes from the database
    cursor = conn.cursor()
    cursor.execute(f"SELECT VoteCount FROM Votes WHERE VoteOption = '{button1}'")
    vote1 = cursor.fetchone()[0]
    cursor.execute(f"SELECT VoteCount FROM Votes WHERE VoteOption = '{button2}'")
    vote2 = cursor.fetchone()[0]
    return int(vote1), int(vote2)

def reset_votes_in_db():
    # Reset votes in the database
    cursor = conn.cursor()
    cursor.execute(f"UPDATE Votes SET VoteCount = 0 WHERE VoteOption = '{button1}'")
    cursor.execute(f"UPDATE Votes SET VoteCount = 0 WHERE VoteOption = '{button2}'")
    conn.commit()

def add_vote_to_db(vote):
    # Insert a new vote into the database
    cursor = conn.cursor()
    cursor.execute(f"UPDATE Votes SET VoteCount = VoteCount + 1 WHERE VoteOption = '{vote}'")
    conn.commit()

if __name__ == "__main__":
    app.run()
