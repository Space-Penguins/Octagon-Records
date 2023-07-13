import os
from flask import Flask, render_template, request, url_for
import mysql.connector
import logging

app = Flask(__name__)

# Configure logging
app.logger.setLevel(logging.WARNING)
stream_handler = logging.StreamHandler()
app.logger.addHandler(stream_handler)

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
        # Establish a new database connection
        with mysql.connector.connect(
            host=os.environ.get('MYSQLHOST'),
            user=os.environ.get('MYSQLUSER'),
            password=os.environ.get('MYSQLPASSWORD'),
            database=os.environ.get('MYSQLDATABASE'),
            port=int(os.environ.get('MYSQLPORT', 3306))
        ) as connection:
            cursor = connection.cursor()
            
            cursor.execute(query, (participant,))
            events = cursor.fetchall()

            eventList = []

            for event in events:
                eventList.append(event[0])

            return render_template("events.html", eventList=eventList, name=participant)

    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))