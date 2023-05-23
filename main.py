import os
from flask import Flask, render_template, request, url_for
import mysql.connector


# Retrieve the MySQL database credentials from environment variables
mysql_host = os.environ.get('MYSQLHOST')
mysql_user = os.environ.get('MYSQLUSER')
mysql_password = os.environ.get('MYSQLPASSWORD')
mysql_database = os.environ.get('MYSQLDATABASE')
mysql_port = int(os.environ.get('MYSQLPORT', 3306))

# Connect to the MySQL database
connection = mysql.connector.connect(
    host=mysql_host,
    user=mysql_user,
    password=mysql_password,
    database=mysql_database,
    port=mysql_port
)

# Create a cursor object to execute SQL queries
cursor = connection.cursor()


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == "POST":

        participant = request.form.get("participant")

        query = """
                SELECT Events.event_name
                FROM Participants
                JOIN Participants_Events ON Participants.participant_id = Participants_Events.participant_id
                JOIN Events ON Participants_Events.event_id = Events.event_id
                WHERE Participants.participant_name = %s;
                """
        cursor.execute(query, (participant,))
        events = cursor.fetchall()

        eventList = []

        for event in events:
            eventList.append(event[0])

        return render_template("events.html", eventList=eventList, name=participant)

    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))