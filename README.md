**Lichess-apitool** a is python script for querying lichess-api.

**Features:**
- Return lichess-tv urls for users listed
- Return a sorted list of users and ratings based ordered by rating.
- Query for this data from IRC, irssi script included.

The original use case of this script was to return information of selected lichess users via an irc bot.
It was implemented as a command-line script so that it could be used with different irc clients and bots, and possibly for other purposes too.

**Requirements:**
- Python, versions 2 and 3 are both supported.
- Irssi (irc client), to use the script for relaying messages to irc.
    - Perl is required for running the script.
