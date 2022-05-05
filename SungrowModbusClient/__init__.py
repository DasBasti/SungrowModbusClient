# Copyright (c) 2019 Thomas Fairbank
# Copyright (c) 2022 Bastian Neumann
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian
from pymodbus.client.sync import ModbusTcpClient
import traceback

MIN_SIGNED   = -2147483648
MAX_UNSIGNED =  4294967295

# modbus datatypes and register lengths
sungrow_moddatatype = {
  'S16':1,
  'U16':1,
  'S32':2,
  'U32':2,
  'STR16':8
  }

class Client():
  def __init__(self, modmap, host:str, port:int = 502):
    self.modmap = modmap
    self.host = host
    self.port = port
    self.slave_addr = 0x01
    self.timeout = 3


    self.client = ModbusTcpClient(self.host, 
                         timeout=self.timeout,
                         RetryOnEmpty=True,
                         retries=3,
						 ZeroMode=True,
                         port=self.port)

    self.inverter = {}


  def load_register(self):
    #moved connect to here so it reconnect after a failure
    self.client.connect()
    #iterate through each avaialble register in the modbus map
    for thisrow in self.modmap:
      name = thisrow[0]
      startPos = thisrow[1]-1 #offset starPos by 1 as zeromode = true seems to do nothing for client
      data_type = thisrow[2]
      format = thisrow[3]
    
      #try and read but handle exception if fails
      try:
        received = self.client.read_input_registers(address=startPos,
                                              count=sungrow_moddatatype[data_type],
                                                unit=self.slave_addr)
      except:
        traceback.print_exc()
        return
      
      # 32bit double word data is encoded in Endian.Little, all byte data is in Endian.Big
      if '32' in data_type:
          message = BinaryPayloadDecoder.fromRegisters(received.registers, byteorder=Endian.Big, wordorder=Endian.Little)
      else:
          message = BinaryPayloadDecoder.fromRegisters(received.registers, byteorder=Endian.Big, wordorder=Endian.Big)
      #decode correctly depending on the defined datatype in the modbus map
      if data_type == 'S32':
        interpreted = message.decode_32bit_int()
      elif data_type == 'U32':
        interpreted = message.decode_32bit_uint()
      elif data_type == 'U64':
        interpreted = message.decode_64bit_uint()
      elif data_type == 'STR16':
        interpreted = message.decode_string(16).rstrip(b'\x00')
      elif data_type == 'STR32':
        interpreted = message.decode_string(32).rstrip(b'\x00')
      elif data_type == 'S16':
        interpreted = message.decode_16bit_int()
      elif data_type == 'U16':
        interpreted = message.decode_16bit_uint()
      else: #if no data type is defined do raw interpretation of the delivered data
        interpreted = message.decode_16bit_uint()
      
      #check for "None" data before doing anything else
      if ((interpreted == MIN_SIGNED) or (interpreted == MAX_UNSIGNED)):
        displaydata = None
      else:
        #put the data with correct formatting into the data table
        if format == 'FIX3':
          displaydata = float(interpreted) / 1000
        elif format == 'FIX2':
          displaydata = float(interpreted) / 100
        elif format == 'FIX1':
          displaydata = float(interpreted) / 10
        else:
          displaydata = interpreted
      
      self.inverter[name] = displaydata
