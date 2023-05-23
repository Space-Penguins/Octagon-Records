#! python3
# Compiles a list of all UFC fighters

import requests, bs4, re
from db_connection import connect_to_db, close_connection
from requests.exceptions import HTTPError

# Connect to the database
print("Connection to database...")
db = connect_to_db()
print("Database connected")

# Create a cursor object
cursor = db.cursor()

UFCStart = 26
UFCEnd = 51

url = 'https://en.wikipedia.org/wiki/UFC_'

def add_participant_name_to_db(name):
    print("Adding", name, "to Participants")
    query = "INSERT INTO Participants (participant_name) VALUES (%s);"
    cursor.execute(query, ([name]))

def add_event_name_to_db(urlNumber):
    print("Adding event", urlNumber, "to Events")
    query = "INSERT INTO Events (event_name) VALUES (%s);"
    cursor.execute(query, ([urlNumber]))

def add_connection_between_participants_and_event(participant_id, event_id):
    query = "INSERT INTO Participants_Events (participant_id, event_id) VALUES (%s, %s);"
    cursor.execute(query, (participant_id, event_id))

for urlNumber in range(UFCStart, UFCEnd):
    # Download the page
    full_url = url + str(urlNumber)

    print("Connecting to UFC ", urlNumber)

    try:
        res = requests.get(full_url)
        res.raise_for_status() 
    except HTTPError as e:
        if e.response.status_code == 404:
            print("Page not found. Trying alternative URL.")
            alternative_url = 'https://en.wikipedia.org/wiki/Draft:UFC_' + str(urlNumber)
            res = requests.get(alternative_url)
        else:
            print("An HTTP error occured", e)

    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    table = soup.find("table",{"class":"toccolours"})
    fighters = table.findAll("a")
    for fighter in fighters:
        
        name = fighter.text
        if not (re.search("\[(.*?)\]", name) and name):
        
            query="SELECT * FROM Participants WHERE participant_name = %s"
            cursor.execute(query, (name,))
            participant_exist = cursor.fetchone()


            # Check if the participant is already registered in the database
            if participant_exist:
                query = """SELECT Events.event_name
                        FROM Participants
                        JOIN Participants_Events ON Participants.participant_id = Participants_Events.participant_id
                        JOIN Events ON Participants_Events.event_id = Events.event_id
                        WHERE Participants.participant_name = %s AND Events.event_name = %s;"""
                cursor.execute(query, (name, urlNumber))
                event_exist = cursor.fetchone()

                if event_exist:
                    print("Event allready registerd for", name)
                else:
                    # Insert event name into database
                    add_event_name_to_db(urlNumber)
                    event_id = cursor.lastrowid # Get the id from Events table

                    # Get participant_id from Participants table
                    query="SELECT participant_id FROM Participants WHERE participant_name = %s"
                    cursor.execute(query, (name,))
                    participant_id = cursor.fetchone()

                    # Make the connection between Participants and Events table
                    add_connection_between_participants_and_event(participant_id[0], event_id)

            else:
                # Insert participants name into database
                add_participant_name_to_db(name)
                participant_id = cursor.lastrowid # Get the id from Participants table

                # Insert event name into database
                add_event_name_to_db(urlNumber)
                event_id = cursor.lastrowid # Get the id from Events table

                # Make the connection between Participants and Events table
                add_connection_between_participants_and_event(participant_id, event_id)

            db.commit()            

close_connection(db)