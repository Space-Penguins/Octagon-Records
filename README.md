# Octagon Records
*UFC spoiler free*

[Octagon Records](https://octagonrecords.up.railway.app/)

Octagon Records is a website where the user can look up a fighter’s carrier in UFC without getting the result of each match.

## datascrapping/UFC_figth_compiler.py
This python code uses beautifulsoup to download Wikipedia pages. Then the code looks for a table on the page where all the participants are listed. It takes the name of the participant and add it to a table {Participants} in the database, then in another table {Events} it adds the event number and finally it links the ID of those two entries in the {Participants_Events} table.

If an entry of a participant already exists, it only adds the event and link it to the participant.

## main.py
This is the flask code that handels the website. In the '/' rout it checks if the user has search for a participant and do a search in the data base for that name. It then returns the event.html page.

## event.html
This page displays a table of all events that the participant has fought in. 