from pymodbus.client.sync import ModbusTcpClient
from .drivers import BaseDriver
class Modbus(BaseDriver):
	def __init__(self, cfg):
		self.tags = {}
		self.client = ModbusTcpClient(cfg['address'], cfg['port'])
	def read(self, tag):
		read_type, read_address = tag.split('/', 1)
		read_address = int(read_address)
		if read_type == 'coil':
			result = self.client.read_coils(read_address, 1)
			return {tag: result.bits[0]}
		if read_type == 'reg':
			result = self.client.read_holding_registers(read_address, 1)
			return {tag: result.registers[0]}
		if read_type == 'di':
			result = self.client.read_discrete_inputs(read_address, 1)
			return {tag: result.bits[0]}
	def write(self, tag, value):
		write_type, write_address = tag.split('/', 1)
		write_address = int(write_address)
		if write_type == 'coil':
			value = int(value) == 1
			result = self.client.write_coil(write_address, value)
		if write_type == 'reg':
			value = int(value)
			result = self.client.write_holding_registers(write_address, value)
		if write_type == 'di':
			value = int(value) == 1
			result = self.client.write_discrete_inputs(write_address, 1)

