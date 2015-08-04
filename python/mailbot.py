#!/usr/bin/env python
#Written by paulbe,  github code written by elimisteve

import feedparser, socket, time, pywapi, string

#Connection info for IRC
USER = 'CLUG_Helperbot'  #set bot name
botname     = USER #+ "_bot"
network     = 'irc.freenode.net' #set irc network to connect to
chatchannel = '#cochiselinux' #set channel to connect to
port = 6667  #set port number
end = '\n'


#Variables
website = "CochiseLinuxUsersGroup.github.io"  #CLUG website
mailing = "https://www.freelists.org/feed/cochiselinux" #CLUG mailing list feed
#ghubr1 = "https://github.com/CochiseLinuxUsersGroup/CochiseLinuxUsersGroup.github.io/commits/master.atom" #github feed
#ghubr2 = "https://github.com/CochiseLinuxUsersGroup/projectcode/commits/master.atom" #github feed
#d = feedparser.parse(mailing) #setup parsing for mailing list
#ghun1d = feedparser.parse(ghubr1) #setup parsing for github
#ghun2d = feedparser.parse(ghubr2) #setup parsing for github
result = pywapi.get_weather_from_noaa('KFHU') #setup weather results ('location')

premess = 'PRIVMSG ' + chatchannel + ' :'
irc = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
irc.connect( ( network, port ) )
print irc.recv( 4096 )
irc.send( 'NICK ' + botname + end )
irc.send( 'USER ' + USER + 'bot botty bot bot: Python IRC' + end )
irc.send( 'JOIN ' + chatchannel + end )

#mail parsing


#
# Helper Functions
#
def irc_msg(msg):
    """Sends msg to channel"""
    irc.send(premess + msg + end)
    return

def getuser():
    """Returns nick of current message author"""
    try:
        #user = data.split()[2].strip(':')
        #user = data.split()[0].split('~')[0].strip(':!')
        user = data.split()[0].split('!')[0].strip(':')
    except:
        user = data.split('!')[0].strip(':')
    return user

#
# GitHub  code from elimisteve, thanks!
#
account_name = 'cochiselinuxusersgroup'
branch = 'master'
repo_names = ['cochiselinuxusersgroup.github.io', 'projectcode']
SLEEP_SECONDS = float(60*2.4)/len(repo_names)  # Check each repo once/couple minutes

def check_github():
    old_version = {}
    for repo in repo_names:
        old_version[repo] = feedparser.parse(
            'https://github.com/' + account_name +
            '/' + repo + '/commits/' + branch + '.atom'
            )

#    time.sleep(SLEEP_SECONDS)  # Wait then compare

    for repo in repo_names:
        new = feedparser.parse('https://github.com/' + account_name +
                               '/' + repo + '/commits/' + branch + '.atom')
        try:
            if ':!lastpush' in data.lower():
				author = new.entries[0].author_detail.href.split('/')[-1]
				commit_msg = new.entries[0].title
				print '\n'
				print"[" + repo + "] " + author + ": " + commit_msg
				print '\n'
				irc_msg("[" + repo + "] " + author + ": " + commit_msg)
        except:
            print "GitHub fucked up, I think. Here's what they gave us:"
            print new


#There is a delay here for some reason.          
def check_mail():
	mail_old = {}
	for mail in mailing:
		mail_old[mailing] = feedparser.parse("https://www.freelists.org/feed/cochiselinux")
		
	for mail in mailing:
		new_mail = feedparser.parse("https://www.freelists.org/feed/cochiselinux")
		
		try:
			if ':!lastmail' in data.lower():
				mail_msg = new_mail.entries[0].title
				irc_msg( mail_msg )
				return
		except:
			print "Do da"
			print new_mail


#Main Loop
while True:
	data = irc.recv ( 4096 )
	datasp = data.split(' :')[0]
	datasp = str(datasp)

	username = getuser()

	if 'PING' in data:
		irc.send( 'PONG ' + data.split()[1] + end )

	#Display info for website and mailing list
	if ':!info' in data.lower():
		irc_msg( 'Website: ' + website )
		irc_msg( 'Mailing archive: ' + mailing )
		
	#Show last email title
	#I want to make this more verbose
	#Moved to for loop, if that breaks uncomment this ( bot will have to be restarted to update last mail if used this way )
#	if ':!lastmail' in data.lower():
#		len(d['entries'])
#		irc_msg( 'Latest mail: ')
#		irc_msg( d.feed.title )
#		irc_msg( d['entries'][0]['title'] )
	
	
	#Show current weather in SV	
	if ':!weather' in data.lower():
		irc_msg("Sierra Vista current weather: " + result['temp_f'] + "F and " + result['weather'])
		
	#Display help functions, list available commands
	if ':!help' in data.lower():
		irc_msg( "Available commands: ")
		irc_msg( "!info - Show website and mailing information")
		irc_msg( "!lastmail - Show the title of the latest email to the mailing list")
		irc_msg( "!lastpush - Show the last commits to github repos")
		irc_msg( "!weather - Show current weather in sierra vista")
		irc_msg( "more to come")
	
	print data
	check_github()
	check_mail()

		
