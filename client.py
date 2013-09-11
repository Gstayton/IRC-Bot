"""
Client takes connection info as list and attempts to connect with given info.

Client file to be started via launch.py
imports parser.py for parsing

Recommend looking at a better way to implement a more permanent solution for reload() placement
Possible solution includes a try/except check on import parser, except: import basicParser as parser
"""
import sys, time
import socket, logging
import threading, Queue

import parser 
#custom class file containing parser functions, to be called with possible commands

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s (%(processName)-10s) %(message)s',
                    )

class SockWrap(object):
	"""
	Wrapper for IRC connections.

	Mainly designed to be sub-classed by a proper client class

	"""

	def sendRaw(self, string):
		"""Takes a single string, adds a carriage return, and sends it over the socket to the IRC network"""
		self.conn.send(string+'\r\n')
	
	def send(self, out, tgt):
		"""
		Takes two strings and sends a formatted message over the socket to IRC
		
		out is the message, tgt is the target recipient, either channel or specific user.
		
		"""
		pass

		out = str(out)
		try:
			self.conn.send('PRIVMSG '+tgt+' :'+out+'\r\n')
		except:
			logging.debug('Error in sending')

		#out = str(out)
		#logging.debug('Sending: '+out)

		#if not line['op']:
		#	line['op'] = 'PRIVMSG'
		
		#if line['tgt'] == self.nick:
		#	self.conn.send('PRIVMSG '+line['user']+' :'+out+'\r\n')
		#else:
		#	self.conn.send('PRIVMSG '+line['tgt']+' :'+out+'\r\n')

	def connect(self, connection):
		"""
		Currently re-working: Takes information about server and connects to it. Makes socket a class variable SockWrap.conn

		connection arg should follow format of a dictionary with entries for:
			host
			port
			channels[#channel1,channel2,etc]
			nick
		"""

		self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			logging.debug('Attempting to connect to '+connection['host'])
			self.conn.connect((connection['host'],connection['port']))
		except:
			logging.debug('Unable to connect to server host %s' % connection['host'])
			return(1)
		logging.debug('Connected')
		self.sendRaw('NICK %s' % connection['nick'])
		self.sendRaw('USER Omnius Omnius Omnius :Python IRC by Nathan Thomas')
		f = open('passwd')
		self.sendRaw('PRIVMSG NickServ :IDENTIFY '+f.read())
		logging.debug('Identified')
		#Loop to listen for server confirmation that cloak has been applied
		while True:
			data = self.conn.recv(512)
			print data
			if data.find('396 '+connection['nick']) != -1:
				break
		for channel in connection['channels']:
			logging.debug('Joining channels...')
			self.sendRaw('JOIN %s' % channel)
			logging.debug('Joined '+channel)

class Client(SockWrap):
	"""
	Takes 5 args as input, attempts to connect to server with info defined by args

	Makes use of subclassed SockWrap for all connection methods,

	"""
	
	def __init__(self, connection):
		self.connect(connection)
		self.listen()

	def listen(self):
		"""
		When invoked, listens over Client.conn for data to pass to parser.Handler()
		
		Be sure to have all the rest of the configuration finished before calling this method, as it is intended to run 
		indefinitely until the connection is closed.

		Still needs a way to change certain settings within itself, but currently functionality can only exist within parser
		reload(parser) can be called from inside the IRC via #!ReloadParser, to ensure that there is always a way to 
		get the main functionality up and running even if it fails to load on initial import.
		"""
		while True:
			data = self.conn.recv(512)
			print data

			if data.find('PING') != -1:
				self.sendRaw('PONG')
			if data.find('PRIVMSG') != -1:
				if data.find('#!ReloadParser') != -1:
					try: 
						reload(parser)
					except:
						logging.debug('Failed to reload module')
						e = sys.exc_info()
						logging.debug(e)
					continue
				logging.debug('Starting parser thread')
				# Launch Handler class into seperate thread of control (Possibly a queue?)
				p = parser.Handler()
				parseThread = threading.Thread(name='parser', target=p.called, args=(data, self))
				parseThread.daemon = True
				parseThread.start()


### Attempt at creating a replaceable Parser class to ensure ReloadParser() was always available.
### Reload function is now hardcoded into basic level parser.
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
