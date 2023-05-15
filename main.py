import os
from flask import Flask, render_template, jsonify, request
import mysql.connector

password = os.environ.get('MYSQLPASSWORD')

# Connect to the database using the retrieved password
connection = mysql.connector.connect(
    host='MYSQLHOST',
    user='MYSQLUSER',
    password=password,
    database='MYSQLDATABASE',
    port=int(os.environ.get('MYSQLPORT', 3306))
)

cursor = connection.curosr()


app = Flask(__name__)


@app.route('/')
def index():

    if request.method == "POST":

        if not request.form.get("symbol"):
            return render_template("index.html")

        participant = request.form.get("participant")

        query="""SELECT Events.event_name
                 FROM Participants
                 JOIN Participants_Events ON Participants.participant_id = Participants_Events.participant_id
                 JOIN Events ON Participants_Events.event_id = Events.event_id
                 WHERE Participants.participant_name = 'Chuck Liddell';"""
        cursor.execute(query)
        events = cursor.fetchall()

        return render_template("events.html", events=events)

    else:
        return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
