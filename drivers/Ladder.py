from .drivers import BaseDriver, setup_readwrite
from .Task import Task, MajorFault, MinorFault
import re

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


INSTRUCTIONS = {
	r'XIC':XIC,
	r'XIO':XIO,
	r'OTE':OTE
}
RUNG_END = r';'
BRANCH_START = r'BST'
BRANCH_END = r'BND'
BRANCH_NEXT = r'NXB'


class Ladder(Task):
	def custom_cfg(self, cfg):
		if 'logic' in cfg:
			self.logic = cfg['logic']

	def custom_read(self, tag):
		if tag == 'logic':
			return {'logic': self.logic}
		
	def custom_write(self, tag, value):
		if tag == 'edit':
			print('edited')
			self.logic = value

	def task_logic(self, read, write):
		preparse(self.logic, read, write)


def preparse(text, read, write):
	rungs = text.split(RUNG_END)
	for rung in rungs:
		pieces = rung.split(' ')[::-1]
		parse(pieces, True, read, write)

def parse(pieces, power_state, read, write):
	piece = ''
	power_state_initial = power_state
	power_state_branch_result = False

	while pieces:
		piece = pieces.pop()
		if piece in INSTRUCTIONS:
			inst = INSTRUCTIONS[piece]
			ops = pieces[- inst.operand_count:]
			pieces = pieces[:- inst.operand_count]
			
			logic = inst(ops)
			logic.input = power_state
			power_state = logic.logic(read, write)

		elif piece ==  BRANCH_START:
			pieces, power_state = parse(pieces, power_state, read, write)
		elif piece ==  BRANCH_NEXT:
			power_state_branch_result = power_state_branch_result or power_state
			power_state = power_state_initial
		elif piece ==  BRANCH_END:
			power_state_branch_result = power_state_branch_result or power_state
			return pieces, power_state_branch_result

