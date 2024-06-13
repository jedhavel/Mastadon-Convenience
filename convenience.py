'''
Convenience wrapper around Mastodon API for specialized use within a closed VLAN with no outside dependencies. For more robust functionality,
especially when building custom UX for apps, prefer to use more fully featured Mastodon.py library. 
'''

import json
import requests




MAXACCTS = 150	# Max number of user accounts that you expect on your system
BASEURL = "https://<domain.tld>/" # replace `mastadon.social` with your apps domain dot tld ie `mastadon.social`
DEBUG = true
USER_STAT_OFILE = "active_user_stats.txt"

apiurl = baseurl + "api/v1/"


'''
Runs automatically if you just call the script from cmd line.
Saves toots per user, and total toots to `USER_STAT_OFILE`
'''
def saveStatsForActiveUsers():
	total_tootz = 0
	with open(USER_STAT_OFILE, "w") as ofile:
		ofile.write("ID\tTOOTS\tACCTNAME\n")
		for u in range(1, MAXACCTS):
                        try:
                                if DEBUG:
                                        print("\n\nUID: " + str(u) + "\n\n")
                                result = requests.get(apiurl + "accounts/" + str(u))
                                if DEBUG:
                                        print("Result: " + str(result) + "\n")
                                jdata = json.loads(result.decode('utf-8'))
				ofile.write(jdata["id"] + "\t")
				ofile.write(str(jdata["statuses_count"]) + "\t")
				ofile.write(jdata["username"] + "\n")
			except KeyError:
				print("Key Error | User not found")
		ofile.write("Total Toots: " + str(total_tootz))
getStatsForActiveUsers()

'''
Pull account data for all user accounts
'''
def getAccts():
        accts = []
        for u in range(1, MAXACCTS):
		accts.append(getAcct(u))
	return accts

'''
Returns -1 if username not found
'''
def getIdFromUsername(username):
        _id = -1
        for acct in getAccounts():
                if acct["username"] == username:
                        _id = acct["id"]
        return _id

'''
Returns -1 if ID not found
'''
def getUsernameFromId(_id):
        username = -1
        for acct in getAccounts():
                if acct["id"] == _id:
                        username = acct["username"]
        return username

'''
Pull account data for a user account
'''
def getAcctById(_id):
        if DEBUG:
		print("\n\nUID: " + str(_id) + "\n\n")
        try:
                result = requests.get(apiurl + "accounts/" + str(u))
                if DEBUG:
                       print("Result: " + str(result) + "\n")
        except KeyError:
                print("Key Error | User not found")
	return json.loads(result.decode('utf-8'))

def getAcctByUsername(username):
        return getAcctById(getIdFromUsername(username))

def getUserTootsById(_id):
        result = requests.get(apiurl + "accounts/" + str(_id) + "/statuses")
        return json.loads(result.decode('utf-8'))

def getUserTootsByUsername(username):
	_id = getIdFromUsername(username)
	if _id != -1:
                return json.loads(getUserTootsById(_id).decode('utf-8'))
