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
password = None
#####################

def login(email, password):
	if password == None:
		if email != None:
			email = email
			password = getpass.getpass('Password: ')
		else:
			email = "levkiselev@gmail.com"
			#email = raw_input("Email: ")
			password = getpass.getpass('Password: ')
			if not api.security.login(email, password):
				exit(1)
			token = api.token
	else: email = email; password = password

def choose_serv():
	global url
	global email
	global password
	global token
	global api

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
	login()
	print('Your token: ' +token)

def games_list():
	glist = api.games.list()
	print
	for key, value in glist['data'].iteritems():
		print(value['id'] + ': ' + value['title'])
	print

def choose_game():
	global choosed_game
	games_list()
	choosed_gameid = raw_input("Please choose game: ")
	game = api.games.choose(choosed_gameid)
	choosed_game = game['data']['title']
	print('Choosed game ' + game['data']['title'])
	print

def quests_list():
		quests = api.quests.list({'filter_completed' : True, 'filter_open' : True, 'filter_current' : True})
		formattablequests = '{:<8}|{:<15}|{:<20}|{:<10}|{:<5}'
		print "\n"+formattablequests.format('Quest ID', 'Subject + Score', 'Name', 'Status', 'Solved')
		print formattablequests.format('--------', '---------------', '--------------------', '----------', '-----')
		for key, value in enumerate(quests['data']):
			print formattablequests.format(value['questid'], value['subject'] + ' ' + value['score'], value['name'], value['status'], value['solved'])
		print

def time(): print datetime.now().strftime('%d/%m/%y::%H:%M:%S')

#def choose_quest():


allFunc = {"t(ime)?":time,"ch(ange|oose)? serv":choose_serv, r'ch(oose)? ?g(ame)?':choose_game, "g(ame)? ?l(ist)?":games_list,\
"q(uests?)? ?l(ist)?": quests_list}

#login(email, password)
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
			tcmd = cmds[2]
		except IndexError: pass

		else:
			for i in allFunc:
				if re.match(i, fcmd+scmd+tcmd):
					allFunc[i](scmd, tcmd)
				else: print "unknown command"

		finally:
			try:
				scmd = cmds[1]
			except  IndexError:
				for i in allFunc:
					if re.match(i, fcmd):
						allFunc[i]()
					else: print "unknown command"
			else:
				for i in allFunc:
					if re.match(i, fcmd+scmd):
						allFunc[i](scmd)
					else: print "unknown command"

		# for i in allFunc:
		# 	if re.match(i, fcmd):
		# 		allFunc[i]()
		# 	elif re.match(i, fcmd+scmd):
		# 		allFunc[i](scmd)
		# 	elif re.match(i, fcmd+scmd+tcmd):
		# 		allFunc[i](scmd, tcmd)
		# else:
		# 	print "uncnown command"
		# for w in allFunc:
		# 	if re.match(w, command):
		# 		allFunc[w]()


# 	elif re.match(r'^quest show ([0-9]+)$', command):
# 		match = re.match(r'^quest show ([0-9]+)$', command)
# 		questid = match.group(1)
# 		quest = api.quests.get(questid)
# 		print '   Subject: ' + quest['data']['subject']
# 		print '     Score: ' + quest['data']['score']
# 		print '      Name: ' + quest['data']['name']
# 		print '    Author: ' + quest['data']['author']
# 		print '      Text: '
# 		print quest['data']['text']
# 		print ""
# 	elif re.match(r'^quest pass ([0-9]+) (.*)$', command):
# 		match = re.match(r'^quest pass ([0-9]+) (.*)$', command)
# 		questid = match.group(1)
# 		answer = match.group(2)
# 		result = api.quests.trypass(questid, answer)
# 		if result['result'] == 'ok':
# 			print "quest passed"
# 		else:
# 			print result['error']['message']
