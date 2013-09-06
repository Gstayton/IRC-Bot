"""Parser module. Adds functionality to Parser class.
Note: Do not overwrite reloadParser() if avoidable"""
import logging
import time
import sys
import random

class Parser(object):
	def __init__(self):
		self.commands = {
				'status' : self.status,
				'joinchannel':self.join,
				'time':self.time,
				'dice':self.dice,
				'roll':self.dice,
				'dick':self.dick,
				'help':self.helpComm
				}
		
	def parse(self, line, client):
		self.irc = client
		logging.debug("Thread start")

		null, data, msg = line.split(':',2)
		userInfo, opcode, target = data.split()
		user, hostmask = userInfo.split('!')

		msg = msg.strip()

		if msg.find(' ') != -1:
			cmd, msg = msg.split(' ',1)
		else:
			cmd = msg

		logging.debug('cmd: '+cmd)
		logging.debug('op : '+opcode)
		logging.debug('tgt: '+target)

		lineDict = {
				'user':user,
				'msg':msg,
				'cmd':cmd,
				'op':opcode,
				'tgt':target,
				'data':data,
				'line':line
		}
		
		logging.debug('Usr: '+lineDict['user'])
		logging.debug('Msg: '+lineDict['msg'])

		if cmd[0] == '!':
			try:
				command = self.commands[cmd.lower()[1:]](lineDict)
				print command
				command
			except:
				e = sys.exc_info()
				logging.debug(e)
		else:
			logging.debug('Command not found')

	def status(self, lineDict):
		self.irc.send('Status OK', lineDict)
		return 'OK'

	def join(self, lineDict):
		self.irc.sendRaw('JOIN '+lineDict['msg'])

	def time(self, lineDict):
		localtime = time.asctime(time.localtime(time.time()))
		self.irc.send(localtime, lineDict)

	def dice(self, line):
		dice = line['msg'].split(' ',1)
		dice = dice[0]
		if line['msg'] == line ['cmd']:
			logging.debug('No arguments given')
		if dice.find('d') != -1:
			num, sides, = dice.split('d')
		else:
			logging.debug('Improper first argument')
		try:
			num = int(float(num))
			sides = int(float(sides))
		except:
			logging.debug('String')
		if (sides >= 1) and (sides <= 9999) and (num >= 1) and (num <= 9999):
			try:
				roll = sum(random.randrange(sides)+1 for die in range(num))
				self.irc.send(roll, line)
			except:
				logging.debug('Improper 2nd Argument')
		else:
			logging.debug('Invalid Range')
	
	def dick(self, line):
		self.irc.send('Sorry, could not find your dick', line)

	def helpComm(self, line):
		print line['op']
		if line['tgt'] != self.irc.nick:
			self.irc.send('Please use /msg Omnius !help to avoid cluttering up the channel', line)
		else:
			self.irc.send('Current commands are:', line)
			self.irc.send('!Help: The command you used to get here...', line)
			self.irc.send('!Dice: Rolls dice in the format of #d#, ie 1d20. Upper limits of 9999',line)
			self.irc.send('!Status: Simple status checker to make sure the bot is OK.',line)
			self.irc.send("!Dick: ... You just had to, didn't you?", line)
