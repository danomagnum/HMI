from .drivers import BaseDriver
from functools import reduce
import operator

class Internal(BaseDriver):
	def __init__(self, cfg):
		self.tags = {}
		if 'defaults' in cfg:
			for key, value in cfg['defaults'].items():
				self.tags[key] = value
	def read(self, tag):
		'''
		tagnest = tag.split('.')
		taglevel = self.tags
		for tagpart in tagnest:
			if tagpart in taglevel:
				taglevel = taglevel[tagpart]
			else:
				return {'error': "Error - Tag " + str(tag) + " Does Not Exist"}

		return {tag: taglevel}

		if tag in self.tags:
			return {tag: self.tags[tag]}
		else:
			return {'error': "Error - Tag " + str(tag) + " Does Not Exist"}
		'''
		tagnest = tag.split('.')
		val = reduce(operator.getitem, tagnest, self.tags)
		return {tag: val}
	def write(self, tag, value):
		#self.tags[tag] = value
		'''

		tagnest = tag.split('.')
		taglevel = self.tags
		for tagpart in tagnest:
			if tagpart in taglevel:
				taglevel = taglevel[tagpart]
			else:
				return {'error': "Error - Tag " + str(tag) + " Does Not Exist"}


		print "setting " + str(taglevel) + " to " + str(value)
		taglevel = value
		print "setting " + str(taglevel) + " to " + str(value)

		'''

		if isinstance(value, basestring):

			if '.' in value: #may be a float
				try:
					newval = float(value)
					value = newval
				except:
					pass
			elif value.isdigit():
				try:
					value = int(value)
				except:
					pass

		tagnest = tag.split('.')
		reduce(operator.getitem, tagnest[:-1], self.tags)[tagnest[-1]] = value
