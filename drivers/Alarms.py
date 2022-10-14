from .drivers import BaseDriver, setup_readwrite
from .Task import Task, MajorFault, MinorFault
from datetime import datetime
import traceback

class MajorFault(Exception):
	pass
class MinorFault(Exception):
	pass

class AlarmPoint(object):
	def __init__(self, tag, description=None, level=0):
		self.tag = tag
		self.description = description
		self.level = level
		self.active = False
		print(tag, " is active")

	def test(self, read):
		if read(self.tag):
			self.active = True
		else:
			self.active = False

	def __str__(self):
		if self.description is not None:
			return self.description
		else:
			return self.tag


class Alarms(Task):
	def custom_cfg(self, cfg):
		self.alarms = []
		if 'alarms' in cfg:
			for alarm in cfg['alarms']:
				newalarm = AlarmPoint(*alarm)
				self.alarms.append(newalarm)

	def custom_read(self, tag):
		if tag == 'active':
			return {'active':[ str(alarm) for alarm in self.alarms if alarm.active ]}
		if tag == 'inactive':
			return {'inactive':[ str(alarm) for alarm in self.alarms if not alarm.active ]}
		if tag == 'all':
			return {'all':[ str(alarm) for alarm in self.alarms ]}

	def custom_write(self, tag, value):
		pass

	def task_logic(self, read, write):
		for alarm in self.alarms:
			alarm.test(read)
