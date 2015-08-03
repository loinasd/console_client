#!/usr/bin/python

import requests
import uuid
import getpass
import re
from FHQFrontEndLib import FHQFrontEndLib
from datetime import datetime


########VAR###########
choosed_game = ''
choosed_quest = ''
choosed_gameid = 0
url = 'http://fhq.sea-kg.com/api/'
api = FHQFrontEndLib(url)
email = None
email = "levkiselev@gmail.com"
#####################

def login(mail):
	if mail== None:
		email = raw_input("Email: ")
		password = getpass.getpass('Password: ')
	else:
		email = mail
		password = getpass.getpass('Password: ')
	if not api.security.login(email, password):	exit(1)
	token = api.token

def choose_serv(ur):
	global url
	global email
	global password
	global token
	if not url:
		print("1: http://fhq.sea-kg.com/api/\n2: http://fhq.keva.su/api/\n3: http://localhost/fhq/api/")
		numsrv = raw_input("Please choose server: ")
		url = ''
		if numsrv == '1':
			url = 'http://fhq.sea-kg.com/api/'
		elif numsrv == '2':
			url = 'http://fhq.keva.su/api/'
		elif numsrv == '3':
			url = 'http://localhost/fhq/api/'
		else:
			url = 'http://fhq.sea-kg.com/api/'
		print "Choosed: ", url
	else: url = ur
	login(email)
	print('Your token: ' +token)

def games_list(none):
	#glist = api.games.list()["data"]
	glist= {u'532e2d5f-f6fb-20da-d86d-db3e595645e8': {u'date_stop': u'2015-07-03 18:00:59', u'type_game': u'jeopardy', u'description': u'This game just some collection of quests', u'form': u'online', u'title': u'freehackquest-big-game', u'date_start': u'2015-07-02 19:00:00', u'nick': u'admin', u'state': u'original', u'logo': u'files/games/1.png', u'owner': u'47', u'date_restart': u'2015-07-04 17:00:31', u'permissions': {u'export': False, u'update': False, u'delete': False}, u'maxscore': u'10', u'id': u'1', u'organizators': u'any'}, u'c3e15695-89a3-4ace-c767-9e09b38496b3': {u'date_stop': u'2015-05-11 11:30:00', u'type_game': u'jeopardy', u'description': u'unlicenced copy.\n\nhttps://ctftime.org/event/188/tasks/', u'form': u'online', u'title': u'ASIS Quals CTF 2015', u'date_start': u'2015-05-09 11:30:10', u'nick': u'admin', u'state': u'unlicensed-copy', u'logo': u'files/games/2.png', u'owner': u'47', u'date_restart': u'2015-05-13 14:33:04', u'permissions': {u'export': False, u'update': False, u'delete': False}, u'maxscore': u'775', u'id': u'2', u'organizators': u'ASIS'}}
	glist=glist
	for g in glist:
		print glist[g]["type_game"]+" =>  "+glist[g][u"title"]#+ '\t'+ glist[g][u"date_start"]
		#print glist
	print

def choose_game(game):
	global choosed_game
	if game>=0:
		choosed_gameid = game
	else:
		games_list(None)
		choosed_gameid = raw_input("Please choose game: ")
	game = api.games.choose(choosed_gameid)
	choosed_game = game['data']['title']
	print('Choosed game ' + game['data']['title'])
	print

def quests_list(none):
		quests = api.quests.list({'filter_completed' : True, 'filter_open' : True, 'filter_current' : True})
		formattablequests = '{:<8}|{:<15}|{:<20}|{:<10}|{:<5}'
		print "\n"+formattablequests.format('Quest ID', 'Subject + Score', 'Name', 'Status', 'Solved')
		print formattablequests.format('--------', '---------------', '--------------------', '----------', '-----')
		for key, value in enumerate(quests['data']):
			print formattablequests.format(value['questid'], value['subject'] + ' ' + value['score'], value['name'], value['status'], value['solved'])
		print

def time(none): print datetime.now().strftime('%d/%m/%y::%H:%M:%S')

def show_quest(questid):
	quest = api.quests.get(questid)
	print '   Subject: ' + quest['data']['subject']
	print '     Score: ' + quest['data']['score']
	print '      Name: ' + quest['data']['name']
	print '    Author: ' + quest['data']['author']
	print '      Text: '
	print quest['data']['text']
	print 

def pass_quest(string):
		if re.match(r'^([0-9]+) (.*)$', string):
			match = re.match(r'^([0-9]+) (.*)$', string)
			questid = match.group(1)
			answer = match.group(2)
			result = api.quests.trypass(questid, answer)
			if result['result'] == 'ok':
				print "quest passed"
			else:
				print result['error']['message']
		else:
			print "unknown command"


allFunc = {r"t(ime)?":time,r"ch(ange|oose)?serv":choose_serv, r'ch(oose)?g(ame)?':choose_game, r"g(ame)?l(ist)?":games_list,r"q(uests?)?l(ist)?": quests_list, "lg?(ogin)?":login, "sh(ow)?q(uest)?": show_quest}

#login(email)
while True: 
	command = raw_input(choosed_game + "/" + choosed_quest + "> ")
	if command == "exit" or command =="ex": break
	elif command == "h" or command == "help":
		for func in allFunc:
			print func + '\t\t%s' % allFunc[func].__name__
	else:
		cmds = command.split(" ")
		fcmd = cmds[0]
		try:
			scmd = cmds[1]
		except  IndexError:
			for i in allFunc:
				if re.match(i, fcmd):
					allFunc[i](None)
		else:
			for i in allFunc:
				if re.match(i, fcmd+scmd):
					allFunc[i](scmd)
