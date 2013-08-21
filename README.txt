
Ongoing IRC Bot project in Python by Kosan Nicholas

Features currently on todo list:
	-> Easily add new functionality to base code
	-> Live updates without killing the processes
	-> Mutability from within the code itself (Clients in IRC channels able to make changes and commit them, either to code itself or just add new responses)
	-> Multi-server connection support
	-> Console input from server side (?)
	-> Piping chat between two servers (A sort of private chat room across multiple servers)
	-> High stability. Automatically reboot dead processes should an error occur to maintain maximum uptime, even without moderator intervention

Currently Implemented:
	-> Nothing. Working on re-write old code-base from scratch due to longevity away from the project.


Basic desired code outline
vvvvvvvvvvvvvvvvvvvvvvvvvv
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