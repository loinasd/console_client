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
email = ""
url = 'http://fhq.sea-kg.com/api/'
api = FHQFrontEndLib(url)

#####################

def login(mail):
	global token
	if mail=='':
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
	global api
	if not ur:
		print("1: http://fhq.sea-kg.com/api/\n2: http://fhq.keva.su/api/\n3: http://localhost/fhq/api/")
		numsrv = raw_input("Please choose server: ")
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
	api = FHQFrontEndLib(url)
	login(email)
	print('Your token: ' +token)

def games_list(none):
	glist = api.games.list()["data"]
	for g in glist:
		print "%s)  %s \t (%s) " % (glist[g]["id"] ,glist[g]["title"],glist[g]["type_game"])#, glist[g][u"date_start"]
	print

def choose_game(game):
	global choosed_game
	if game:
		try:
			choosed_gameid = int(game)
		except: 
			print "unknown id"
			games_list(None)
			choosed_gameid = int(raw_input("Please choose game: "))
	else:
		games_list(None)
		choosed_gameid = int(raw_input("Please choose game: "))
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

def info(none):
	i = r.get(site+"/api/public/info.php").json()
	if i["result"] == "ok":
		print "Sucssess..."
		print "Lead Time (sec):", i["lead_time_sec"]
		data = i["data"]
		print "Cities:   ",
		for city in data["cities"]:
			print city, ", ",
		quests = data["quests"]
		print
		print "Quests: %s  " % quests["count"], 
		print "All attempts: %s  " % quests["attempts"], 
		print "Solved: %s  " % quests["solved"]
		win = data["winners"]
		for game in win:
			print game + ": "
			gam = win["%s" % game]
			for user in gam:
				print "    ", user["user"], " --> ", user["score"]
	else: print "error"

def logout(none):
	out = {"token":api.token}
	requests.post(url+"security/logout.php", params=out)

def change_password(none):
	old_pass = getpass.getpass("Password: ")
	new_pass = getpass.getpass("New Password: ")
	confirm = getpass.getpass("Confirm new Password: ")
	p = {'old_password':old_pass, "new_password":new_pass, "new_password_confirm":confirm}
	answer = requests.post(url+"users/change_password.php", params=p)
	print answer.text

def user_info(uid):
	if not uid:
		uid = raw_input("user id: ")
	answ = requests.post(url+"users/get.php", params={'userid':uid})
	print answ
	print answ.text


allFunc = {
r"t(ime)?"								:time,
r"i(nfo)?"								:info,
r"ch(ange|oose)?serv"			:choose_serv,
r'ch(ange|oose)?g(ame)?'	:choose_game,
r"g(ame)?l(ist)?"					:games_list,
r"q(uests?)?l(ist)?"			:quests_list,
r"l(o?g)?in"							:login,
r"sh(ow)?q(uest)?"				:show_quest,\
r"l(o?g)?out"							:logout,
r"ch(ange)?pass(word)?"		:change_password,
r"u(ser)?i(nfo)?"					:user_info

}

login(email)
print "All commands types without any whitespace symbols.\nUsage: <command> [params]\nType 'help' for command list."
while True: 
	command = raw_input(choosed_game + "/" + choosed_quest + "> ")
	if command == "exit" or command =="ex": break
	elif command == "h" or command == "help":
		for func in allFunc:
			print func + '\t\t%s' % allFunc[func].__name__
	else:
		cmds = command.split()
		fcmd = cmds.pop(0)
		scmd = " ".join(cmds)
		for i in allFunc:
			if re.match(i, fcmd+scmd):
				allFunc[i](scmd)
