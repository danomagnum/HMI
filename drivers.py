class Driver(object):
	def __init__(self, cfg):
		pass
	def read(self, tag):
		pass
	def write(self, tag, value):
		pass

class Internal(Driver):
	def __init__(self, cfg):
		self.tags = {}
		if 'defaults' in cfg:
			for key, value in cfg['defaults'].iteritems():
				self.tags[key] = value
	def read(self, tag):
		if tag in self.tags:
			return self.tags[tag]
		else:
			return "Error - Tag " + str(tag) + "Does Not Exist"
	def write(self, tag, value):
		self.tags[tag] = value

class CIP(Driver):
	def __init__(self, cfg):
		pass

class FileLogger(Driver):
	def __init__(self, cfg):
		assert 'file' in cfg
		self.filename = cfg['file']
		self.file = Open(filename, 'a')
	def write(self, tag, value):
		self.file.write(tag + ':' + value)
	def __del__(self):
		self.file.close()
