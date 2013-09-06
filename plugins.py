class container(object):
	def dic(self):
		self.plugCommands = {
				'plugtest':self.plugtest
				}

	def plugtest(self,line):
		self.irc.send('Plugins Test', line)
