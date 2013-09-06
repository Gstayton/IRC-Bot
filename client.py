"""Client file to be started via launch.py"""
import sys, time
import socket, logging
import threading, Queue

import parser 
#custom class file containing parser functions, to be called with possible commands

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s (%(processName)-10s) %(message)s',
                    )

class SockWrap(object):
	def sendRaw(self, string):
		self.conn.send(string+'\r\n')
	
	def send(self, out, line):
		out = str(out)
		logging.debug('Sending: '+out)

		if not line['op']:
			line['op'] = 'PRIVMSG'
		
		if line['tgt'] == self.nick:
			self.conn.send('PRIVMSG '+line['user']+' :'+out+'\r\n')
		else:
			self.conn.send('PRIVMSG '+line['tgt']+' :'+out+'\r\n')

	def connect(self):
		self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			logging.debug('Attempting to connect to '+self.host)
			self.conn.connect((self.host,self.port))
		except:
			logging.debug('Unable to connect to server host %s' % self.host)
			return(1)
		logging.debug('Connected')
		self.sendRaw('NICK %s' % self.nick)
		self.sendRaw('USER Omnius Omnius Omnius :Python IRC by Nathan Thomas')
		self.sendRaw('PRIVMSG NickServ :IDENTIFY botomnius')
		logging.debug('Identified')
		#Loop to listen for server confirmation that cloak has been applied
		while True:
			data = self.conn.recv(512)
			print data
			if data.find('396 '+self.nick) != -1:
				break
		for channel in self.channels:
			logging.debug('Joining channels...')
			self.sendRaw('JOIN %s' % channel)
			logging.debug('Joined '+channel)

class Client(SockWrap):
	def __init__(self, *args):
		self.host = args[0]
		self.port = args[1]
		self.channels = args[2]
		self.nick = args[3]
		self.mainPipe = args[4]
		self.connect()
		self.listen()
	
	def sendmsg(self, dest, msg):
		pass

	def listen(self):
		while True:
			data = self.conn.recv(512)
			print data

			if data.find('PING') != -1:
				self.sendRaw('PONG')
			if data.find('PRIVMSG') != -1:
				if data.find('!#ReloadParser') != -1:
					try: 
						reload(parser)
					except:
						logging.debug('Failed to reload module')
						e = sys.exc_info()
						logging.debug(e)
					continue
				logging.debug('Starting parser thread')
				# Launch parser class into seperate thread of control (Possibly a queue?)
				p = parser.Parser()
				parseThread = threading.Thread(name='parser', target=p.parse, args=(data, self))
				parseThread.daemon = True
				parseThread.start()
			
#class Parser(object):
#	def __init__(self):
#		self.commands = {
#				'reload':self.reloadParser
#		}
#
#	def parse(self, data, client):
#		self.irc = client
#		if data.find('!reload') != -1:
#			print data
#			self.reloadParser()
#	
#	def reloadParser(self):
#		reload(parser)
