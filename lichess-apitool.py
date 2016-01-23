import json
import urllib2
import sys

"""This script is used to query the lichess API"""
"""Author: Henri Nieminen, henri.nieminen@gmail.com"""
"""Version: 0.01"""

apiurlusr = 'http://en.lichess.org/api/user/'
linicks = 'linicks.txt'


def tv():
    """Returns all the tv urls of listed lichess players that are playing"""
    #
    #  <@MJXII_ICE> or better still: PLAYING (blah); SPECTATING: (blah); ONLINE: (blah)
    #
    message = ""
    list = readfiletolist(linicks)
    first = True
    
    for item in list:
        # Insert the 'tv url' of a player that is playing
        tmp = gettvurlonline((apiurlusr + item), item)
        if tmp != '':
            if not first:
                message += "* "+ tmp + " "
            else:
                message += tmp + " "
                first = False

    if message == "":
        return 'No activity on lichess'
    else:
        return message


def help():
    """Return the list of commands as a string"""
    str = "Commands: "
    for s in commandlist:
        str += '.' + s + ' '
    return str


def top():
    """Returns a string presentation of players with order by highest ranking"""
    # Currently returns blitz games top list
    msg = ""
    tuplelist = []
    playerlist = readfiletolist(linicks)
    
    for player in playerlist:
        json = getapiresponse((apiurlusr + player), 'perfs')
        tuplelist.append( (player, json['blitz']['rating']) )
    # Sort the list, reverse order (from highest to smallest)    
    tuplelist.sort(reverse=True, key=lambda tup: tup[1])
    
    i = 1
    for item in tuplelist:
        msg += str(i) + '.' + str(item[0]) + ': ' + str(item[1]) + ' \ '
        i+=1
    return msg
    
    
def readfiletolist(file):
    """Reads a given filename line by line and returns it as a list"""
    list = []
    try:
        # Open the file for reading
        with open(file, 'r') as file:
            # Go through the file line by line
            for line in file:
                # Append to list, get rid of possible newlines that come from the file '\n'
                list.append(line.rstrip('\n'))
        return list              
    except IOError:
        sys.exit('Error: Cannot open file ' + file)
    
    
def gettvurlonline(fullurl, username):
    """Check if user is online"""
    # 1. Make sure that we are not trying with empty username
    # 2. Make sure that the user is online
    if len(username) > 0 and userisonline(fullurl) == True:
        return gettvurl(username)
    else:
        return ''


def userisonline(fullurl):
    
    if getapiresponse(fullurl, 'online') == False:
        return False
    else:
        return True


def gettvurl(username):
    return 'http://lichess.org/@/' + username + '/tv'


def getapiresponse(url, item):
    response = getdata(url)
    data = response.read()
    jsondata = json.loads(data)
    return jsondata[item]    


def getdata(url):
    req = urllib2.Request(url, headers = {'Accept' : 'application/json'})
    try:
        return urllib2.urlopen(req)
    except:
        sys.exit('Error: Cannot open the url')
   
        
def runprog(arg):
    """This method controls everything this script does"""

    """Iterate through the list of commands,
    if argv equals to something in the list, run corresponding function"""
    for comm in commandlist:
        if arg == comm:
            return commandlist[comm]()
    # If the arg was not in list of commands, return error        
    return """Error: Command '""" + arg + """' does not exist'"""

###################    
### Main begins ###
###################
def main(arvg):
    # Check that argv[1] is set, run with argv if it exists
    if len(sys.argv) >= 2:
        print runprog(sys.argv[1])
    else:
        print 'Error: Missing argument'

################
### Run main ###
################        
if __name__ == "__main__":
    # List of commands this script runs when delivered in argv[1]
    commandlist = {'help': help, 'tv': tv, 'top':top}
    main(sys.argv[1:])
