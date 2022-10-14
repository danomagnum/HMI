# coding: utf-8

from pymodbus.client.sync import ModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian

c = ModbusTcpClient('192.168.0.10')

# read one bit
a = c.read_discrete_inputs(0x4000,1)
# access the response data.  It is one byte minimum no matter what
a.bits[0]


# read one 16 bit integer
b = c.read_holding_registers(0x70C6, 1)
# access the response data, it is the length specified in the read command
b.registers[0]

# read two 16 bit values then convert them to floats
e = c.read_holding_registers(0x70C6, 2)
d = BinaryPayloadDecoder.fromRegisters(a.registers, byteorder=Endian.Big, wordorder=Endian.Little)
d.decode_32bit_float()
