"""
launcher.py handles the launching and managing of multiple processes for the various server connections of pybot.
connections is a list of servers that the bot will attempt to connect to, including multiple channels.
activeConnections is a list of currently active client.py processes, as well as an established pipe to each oth them
Piping is not currently used, but should be once an overriding command line interface has been established.
"""
import sys, time
import logging
import Queue

from multiprocessing import Process, Pipe

import client # Custom client.py file, handles IRC connections/communications. One connection per client.

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s (%(processName)-10s) %(message)s',
                    )

class Main(object):
	"""
	Takes no arguments, though may eventually be controlled via an external configuration file.

	Stores currently active connections in self.activeConnections.

	Starts client in a seperate process for each server in connections.

	"""
	activeConnections = {}
	#[server, port, [#channels],nick]
	#connections = {
	#'freenode':['irc.freenode.net',6667,['#Omnius'],'Omnius']
	#}
	connections = {
			'freenode':{'host':'irc.freenode.net','port':6667,'channels':['#Omnius'],'nick':'Omnius'}
			}

	def start(self):
		for network in self.connections:
			parentPipe, childPipe = Pipe()
			self.activeConnections[network] = {'cPipe':childPipe, 'pPipe':parentPipe}
			self.activeConnections[network]['process'] = Process(target=client.Client,args=[self.connections[network]])
			self.activeConnections[network]['process'].start()
			
		time.sleep(5)

if __name__ == '__main__':
	m = Main()
	m.start()

"""
Main()
	Initialization of clients into processes
		-> Clients connect to respective IRC servers, handling connections
		-> Clients spawn threads to handle parsing
		-> Clients use event flags to signal status to main()
		-> Clients have some way of communicating between each other (?)
	Handling of event flag responses
	Monitor status of each Client process, restarting dead processes

			Client()
				-> Maintain connection to IRC server
				-> Code for parsing basic IRC and detecting possible commands to be sent to parser
				-> Code for finalizing update started by main process
				-> Detailed logging of connected server
				-> Ability to recieve and send private messages

					functions()
						-> Threaded process to handle various functions
						-> Code to be reloaded by Client for updates
						-> Contains parsing for commands
						-> Contains command definitions
						-> May spawn child threads for various long-running commands

			Mail() [Requires ability to communicate with seperate processes] -Implemented pipe for this
				-> Check for new Mail
				-> Parse commands from mail
				-> Ability to send straight to any given server connection

Update()
	Handles live updating of Client code
		-> Minimal/No downtime of Client processes
			-> Initial Client process runs minimal script with update code, imports main code which is updated live
		-> Initiated by Client processes after authentication
		-> Retrieve update via either online raw or IRC file transfer

"""
