"""
Takes a line from IRC and runs a given method or simply passes if no command is found.

Parser module. Deals with incoming data from the IRC for command interpretation and wtput handling into the IRC
Handler class deals with incoming calls from client.py, handing parsing functions off to the Parser class, and then
passing returns from it to Commands, which handles execution of issued commands.
"""
import logging
import time
import sys
import random

class Handler(object):
	"""
	Always start new threads with Handler.called

	A general handler class, which deals with initial passing of arguments to parser. Also handles initialization of both
	Parser and Commands.

	Eventually intended to also handle 

	"""
	helpDict = {}
	def called(self, parserQ, client):
		parserQ = parserQ[0]
		global irc
		irc = client
		logging.debug('Parser Module')
		
		global parser
		parser = Parser()
		
		while True:
			if parserQ.qsize() != 0:
				line = parserQ.get()
				commands = Commands()
				commands.handler(*parser.lineParse(line, client))
				parserQ.task_done()
	
	def helpAdd(self, string):
		pass
		

class Parser(object):
	def lineParse(self, line, client):
		### In dire need of re-write once Handler is better defined
		self.irc = client

		null, data, msg = line.split(':',2)
		userInfo, opcode, target = data.split()
		user, hostmask = userInfo.split('!')

		msg = msg.strip()

		if msg.find(' ') != -1:
			cmd, msg = msg.split(' ',1)
		else:
			cmd = msg
		print 'DEBUG', cmd, msg
		if cmd[0] == '!':
			try:
				cmd = cmd.lower()[1:]
				#command = self.commands[cmd.lower()[1:]](lineDict)
				#Never change the order of these, if anything needs added, append it to the end of the tuple
				return cmd, msg, user, target

			except:
				e = sys.exc_info()
				logging.debug(e)
				return False
		else:
			logging.debug('Command not found')


class Commands(object):
	
	def handler(self, cmd, msg, user, target, *args):
		commands = {
			'status' : self.status,
			'joinchannel':self.join,
			'time':self.time,
			'dice':self.dice,
			'roll':self.dice,
			'dick':self.dick,
			'help':self.helpComm
			}
		
		commands[cmd](cmd=cmd, msg=msg, user=user, target=target)	

	def status(self, target, **_):
		logging.debug('Status OK')
		irc.send('Status OK', target)

	def join(self, **_):
		msg = line[1]
		irc.sendRaw('JOIN '+msg)

	def time(self, **_):
		localtime = time.asctime(time.localtime(time.time()))
		irc.send(localtime, lineDict)

	def dice(self, msg, cmd, **_):
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
				irc.send(roll, line)
			except:
				logging.debug('Improper 2nd Argument')
		else:
			logging.debug('Invalid Range')
	
	def dick(self, **_):
		irc.send('Sorry, could not find your dick', line)

	def helpComm(self, target, *_):
		if target != self.irc.nick:
			self.irc.send('Please use /msg Omnius !help to avoid cluttering up the channel', line)
		else:
			self.irc.send('Current commands are:', line)
			self.irc.send('!Help: The command you used to get here...', line)
			self.irc.send('!Dice: Rolls dice in the format of #d#, ie 1d20. Upper limits of 9999',line)
			self.irc.send('!Status: Simple status checker to make sure the bot is OK.',line)
			self.irc.send("!Dick: ... You just had to, didn't you?", line)
