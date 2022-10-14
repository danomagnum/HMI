from .drivers import BaseDriver
import pylogix
import datetime
from collections import deque
import string

class CIP(BaseDriver):
  def __init__(self, cfg):
    self.tags = {}
    self.client = pylogix.PLC()
    self.client.IPAddress = cfg['IP']
    self.tags = {}
    self.comm_active = False
    self.read_queue = deque()
    self.write_queue = deque()
  def read(self, tag):
    result = None
    #print tag
    if tag in self.tags:
      result = self.tags[tag].Value
    
    if tag not in self.read_queue:
      self.read_queue.append(tag)
    
    
    return {tag: result}
  
  def write(self, tag, value):
    self.write_queue.append([tag, value])
    #self.client.Write(tag, value)

  def single_read(self, read_list=None):
    if read_list is None:
      read_list = list(self.read_queue)
      self.read_queue.clear()
    for tag in read_list:
      try:
        value = self.client.Read(tag)
        self.tags[tag] = value
      except:
        print('error with tag{}'.format(tag))
        self.tags[tag] = None

  def retry_connection(self):
    print('connection resetting')
    self.client = pylogix.PLC()
    self.client.IPAddress = cfg['IP']
  
  def bulk_read(self, read_list=None):
    if read_list is None:
      read_list = list(self.read_queue)
      self.read_queue.clear()
    
    if len(read_list) > 1:
      print("reading multiple")
      try:
        values = self.client.Read(read_list)
      except:
        self.retry_connection()
      for x in range(len(read_list)):
        self.tags[read_list[x]] = values[x]
    else:
      print("reading single")
      self.single_read(read_list)
      
  
  def tick(self, driverlist):
    if self.read_queue:
        self.bulk_read()
    
    write_list = list(self.write_queue)
    self.write_queue.clear()
    for tag, value in write_list:
      print('{} = {}'.format(tag, value))
      self.client.Write(tag, value)
