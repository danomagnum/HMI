class NotEnoughOperands(Exception):
	pass

class Operand(object):
	operand_count = 0
	def __init__(self, operands = None):
		self.input = False
		self.output = False
		if operands is not None:
			if len(operands) == self.operand_count:
				self.operands = operands
			else:
				raise NotEnoughOperands()
		else:
			if self.operand_count == 0:
				self.operands = []
	def logic(self, read, write):
		self.output = self.input

class XIC(Operand):
	operand_count = 1
	def logic(self, read, write):
		if read(self.operands[0]):
			self.output = self.input
		else:
			self.output = False

		return self.output

class XIO(Operand):
	operand_count = 1
	def logic(self, read, write):
		if not read(self.operands[0]):
			self.output = self.input
		else:
			self.output = False

		return self.output


class OTE(Operand):
	operand_count = 1
	def logic(self, read, write):
		self.output = self.input
		write(self.operands[0], self.input)
		return self.output

