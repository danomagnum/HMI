# used for a driver to read a tag by tagpath from a given driverlist
def read_external(tagpath, driverlist):
	driver, tag = tagpath.split('/',1)
	return driverlist[driver].read(tag)[tag]
# used for a driver to write a tag by tagpath from a given driverlist
def write_external(tagpath, value, driverlist):
	driver, tag = tagpath.split('/',1)
	driverlist[driver].write(tag, value)
# setup functions so you don't need to pass in the driverlist every time
def setup_readwrite(driverlist):
	read_function = lambda x: read_external(x, driverlist)
	write_function = lambda y, value: write_external(y, value, driverlist)
	return (read_function, write_function)
	
class BaseDriver(object):
	def __init__(self, cfg):
		self.cfg = cfg

	def read(self, tag):
		return {tag: tag}
	def write(self, tag, value):
		return tag
	def tick(self, driverlist):
		pass
