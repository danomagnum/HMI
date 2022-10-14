from .Task import Task

class CustomTask1(Task):
	def task_logic(self, read, write):
		write('builtin/incvalue2', int(read('builtin/incvalue')) + 10)
