from .drivers import BaseDriver, setup_readwrite
from datetime import datetime
import traceback

class MajorFault(Exception):
	pass
class MinorFault(Exception):
	pass

class Task(BaseDriver):
	def __init__(self, cfg):
		if 'period' in cfg:
			self.period = int(cfg['period'])
		else:
			self.period = 0
		if 'logsize' in cfg:
			self.logsize = int(cfg['logsize'])
		else:
			self.logsize = 100
		self.paused = 'paused' in cfg
		self.lastcall = datetime.now()
		self.timing_last = 0
		self.timing_max = 0
		self.log_list = []
		self.faulted = 0

		self.custom_cfg(cfg)

		self.log("Startup")
	
	def custom_cfg(self, cfg):
		pass

	def log_popped(self, log_entry):
		# implement this if you want to log everything to a database, etc.
		pass

	def log (self, message):
		if len(self.log_list) > self.logsize:
			self.log_popped(self.log_list.pop(0))
		timestamp = datetime.now()
		self.log_list.append((timestamp, message))
	def read(self, tag):
		if tag == 'paused':
			return {tag: self.paused}
		if tag == 'log':
			return {tag: self.log_list}
		if tag == 'status':
			status = 0
			if self.paused:
				status += 1
			if self.faulted:
				status += 2
			return {tag: status}
		if tag == 'timing_last':
			return {tag: self.timing_last}
		if tag == 'timing_max':
			return {tag: self.timing_max}
		return self.custom_read(tag)

	def custom_read(self, tag):
		pass

	def write(self, tag, value):
		if tag == 'fault_reset':
			if int(value) == 0:
				return
			self.faulted = 0
			timestamp = datetime.now()
			self.log("Faults Reset")
		if tag == 'log_clear':
			if int(value) == 0:
				return
			self.log_list = []
			timestamp = datetime.now()
			self.log("Log Cleared")
		if tag == 'play':
			if self.paused:
				self.log("Started")
				self.paused = False
		if tag == 'pause':
			if not self.paused:
				self.log("Paused")
				self.paused = True
		if tag == 'timing_max':
			self.log("Reset Timing Max")
			self.timing_max = 0
		self.custom_write(tag, value)
	
	def custom_write(self, tag, value):
		pass

	def tick(self, driverlist):
		if self.paused:
			return
		if self.faulted:
			return
		ts1 = datetime.now()
		delta = ts1 - self.lastcall
		delta = delta.total_seconds() * 1000
		if delta > self.period:
			try:
				read, write = setup_readwrite(driverlist)
				self.task_logic(read, write)
			except MinorFault as e:
				self.log(traceback.format_exc())
			except MajorFault as e:
				self.faulted = 1
				self.log(traceback.format_exc())
			except Exception as e:
				self.faulted = 1
				self.log(traceback.format_exc())
			ts2 = datetime.now()
			execution_time = ts2 - ts1
			self.timing_last = execution_time.total_seconds()
			if self.timing_last > self.timing_max:
				self.timing_max = self.timing_last
			self.lastcall = ts1
	def task_logic(self, read, write):
		raise MajorFault("Task Logic Not Overridden")


# use this for a template for any other custom tasks.  Still subclass Task though.
class CustomTask(Task):
	def custom_cfg(self, cfg):
		pass

	def log_popped(self, log_entry):
		# implement this if you want to log everything to a database, etc.
		pass

	def custom_read(self, tag):
		pass

	def custom_write(self, tag, value):
		pass

	def task_logic(self, read, write):
		raise MajorFault("Task Logic Not Overridden")
