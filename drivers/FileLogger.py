from .drivers import BaseDriver
class FileLogger(BaseDriver):
	def __init__(self, cfg):
		assert 'file' in cfg
		self.filename = cfg['file']
		self.file = Open(filename, 'a')
	def write(self, tag, value):
		self.file.write(tag + ':' + value)
	def __del__(self):
		self.file.close()
