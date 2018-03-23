COMM!T Web App
=============


<img src="https://jamesdavidmoffet.com/images/commit/login.jpg" height="400" /><img src="https://jamesdavidmoffet.com/images/commit/commit.jpg" height="400" /><img src="https://jamesdavidmoffet.com/images/commit/map.jpg" height="400" />



The COMM!T app keeps people accountable to their friends by letting the friend who invited them know whether or not they checked in at the polls via GPS. COMM!T sends voters reminders with a checkin link that uses Google's Civic Data API to identify polling places for folks to check in. Once a user clicks "COMM!T" their referring friend will be notified on election of their checkin status and commitments cannot be revoked (we provide a few backup options at checkin that give users and their friends an opportunity to hash things out). 

COMM!T is a python flask app that serves a simple bootstrap front end. It was designed to be easily adapted and deployed for free on heroku.

# Install and run project
    
    git clone https://github.com/jimmoffet/commit.git
    cd commit
    pip install -r requirements.txt
    python app.py # run on 127.0.0.1:5000

# Message from Team COMM!T

Your vote matters more than you might think. Local elections are often won by tens of votes and local decisions directly impact you. Tomorrow, we'll send you a check-in link that will confirm your location, plus a few reminders. If you don't check in near a polling place, we'll send a simple message to {Your Referring Friend} that says you didn't check in. You can customize the messages that will be sent when you check in (or don't) using the "customize messages" link after you sign in. We'll have check in options for absentee and non-eligible voters. You'll also get to see how many folks you got to COMM!T. We keep all contact info confidential. Now, go for it!

-Team COMM!T

