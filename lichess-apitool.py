import json
import sys
try:
    # For Python 3.0 and later
    from urllib.request import urlopen, Request, URLError
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen, Request, URLError

"""This script can be used to query the lichess API."""
"""Results are returned in plain text."""
"""Author: Henri Nieminen, henri.nieminen@gmail.com"""
"""Version: 0.02"""

api_url_user = 'http://en.lichess.org/api/user/'
lichess_users = 'lichess-users.txt'


def tv_urls():
    """
    Returns all the tv urls of users listed in lichess-users.txt that are online.
    """
    #  TODO: <@MJXII_ICE> or better still: PLAYING (blah); SPECTATING: (blah); ONLINE: (blah)
    message = list()
    user_list = read_file_to_list(lichess_users)
    if not user_list:
        return 'No users listed in lichess-users.txt'
    first = True
    for item in user_list:
        # Make sure that the item is not an empty line
        if item.strip() != '':
            # Insert the 'tv url' of a player that is playing
            tmpstr = get_tv_url_online((api_url_user + item), item)
            if tmpstr != '':
                if not first:
                    message.append("* " + tmpstr + " ")
                else:
                    message.append(tmpstr + " ")
                    first = False

    if not len(message) > 0:
        return 'No activity on lichess.'
    else:
        return str().join(message)


def help_text():
    """Return the list of commands as a string"""
    str = "Commands: "
    for s in commands:
        str += '.' + s + ' '
    return str


def ranking():
    """
    Returns a string presentation of players with order by highest ranking.
    Currently returns blitz game rankings.
    """
    msg = ""
    ranking_list = []
    user_list = read_file_to_list(lichess_users)
    if not user_list:
        return 'No users listed in lichess-users.txt'
    for user in user_list:
        jsondata = get_api_response((api_url_user + user), 'perfs')
        ranking_list.append((user, jsondata['blitz']['rating']))
    # Sort the list, reverse order (from highest to smallest)    
    ranking_list.sort(reverse=True, key=lambda tup: tup[1])

    for i, item in enumerate(ranking_list):
        # i+1 to start from 1
        msg += str(i+1) + '.' + str(item[0]) + ': ' + str(item[1]) + ' \ '
    return msg
    
    
def read_file_to_list(file_path):
    """
    Reads a given file path line by line and returns it as a list.
    """
    contents = list()
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Make sure that the line does not start with # (hash) or that line is not empty string
                if not line.lstrip().startswith('#') or line == '':
                    # Remove newlines (\n) at the end.
                    contents.append(line.rstrip('\n'))
        return contents
    except IOError:
        sys.exit('Error: Cannot open file ' + file_path)
    
    
def get_tv_url_online(full_url, username):
    """
    Check if user is online:
    1. Make sure that we are not trying with empty username (extra precaution)
    2. Make sure that the user is online
    """
    if len(username) > 0 and user_is_online(full_url):
        return get_tv_url(username)
    else:
        return ''


def user_is_online(full_url):
    if get_api_response(full_url, 'online'):
        return False
    else:
        return True


def get_tv_url(username):
    return 'http://lichess.org/@/%s/tv' % username


def get_api_response(url, item):
    response = get_data(url)
    data = response.read()
    jsondata = json.loads(data)
    return jsondata[item]


def get_data(url):
    req = Request(url, headers={'Accept': 'application/json'})
    try:
        return urlopen(req)
    except URLError:
        sys.exit('Error: Cannot open the url')
   
        
def run(command):
    """Run command."""
    try:
        return commands[command]()
    except KeyError:
        return "Error: Command '%s' does not exist." % command


# ### Main
def main():
    try:
        print(run(sys.argv[1]))
    except IndexError:
        print('Error: Missing argument')
        print(help_text())


# ### Run main
if __name__ == '__main__':
    # List of commands this script runs when delivered in argv[1]
    commands = {'help': help_text, 'tv': tv_urls, 'top': ranking, }
    main()