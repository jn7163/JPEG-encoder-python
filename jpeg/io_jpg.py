#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: < io_jpg.py 2016-05-14 21:03:38 >
"""
JPEG读写二进制实现
""" 

import numpy as np
import struct

# JPEG固定文件头数据
# HEADER_MARKER = {}
HEADER_SOI = '\xff\xd8'
HEADER_APP0 = '\xff\xe0'
HEADER_DQT = '\xff\xdb'
HEADER_SOF0 = '\xff\xc0'
HEADER_DHT = '\xff\xc4'
HEADER_SOS = '\xff\xda'
HEADER_EOC ='\xff\xd9'


class JPG(object):
	def __init__(self, filelocation, input_matrix=None):
		self.filelocation = filelocation
		self.matrix = input_matrix
		if self.matrix is not None:
			self.height = self.matrix.shape[0]
			self.width = self.matrix.shape[1]
		else:
			self.height = 0
			self.width = 0

		# 偏移量字典
		self.offset_dict = {
			'APP0': None,
			'DQT': [], 
			'SOF0': None,
			'DHT': [],
			'SOS': None,
			'EOC': None
		}
		self.buffer = None

		
	# ------------------------------
	def read_offset(self, f):
		index = 2
		# 从APP0开始扫描
		f.seek(2)
		print "reading offset"
		while True:
			buffer = f.read(1)
			# 到达EOF
			if not buffer:
				break
			if buffer == '\xff':
				buffer += f.read(1)
				if buffer == HEADER_APP0:
					self.offset_dict['APP0'] = index
					index += 1
				elif buffer == HEADER_DQT:
					self.offset_dict['DQT'].append(index)
					index += 1
				elif buffer == HEADER_SOF0:
					self.offset_dict['SOF0'] = index
					index += 1
				elif buffer == HEADER_DHT:
					self.offset_dict['DHT'].append(index)
					index += 1
				elif buffer == HEADER_SOS:
					self.offset_dict['SOS'] = index
					index += 1
				elif buffer == HEADER_EOC:
					self.offset_dict['EOC'] = index
					break
				else:
					# 向后移动指针
					f.seek(-1, 1)
			index += 1
		for i in self.offset_dict:
			print i, "->", self.offset_dict[i]

	def read_APP0(self):
		pass

	def read_DQT(self):
		pass

	def read_SOF0(self):
		pass

	def read_DHT(self):
		pass

	def read_SOS(self):
		pass

	def read_compressed_bin(self):
		pass

	def read_data(self):
		with open(self.filelocation, 'rb') as f:
			self.read_offset(f)
			
		pass

	def get_data(self):
		pass
	
	# ------------------------------

	def write(self):
		pass

	def write_APP0(self):
		pass

	def write_DQT(self):
		pass

	def write_SOF0(self):
		pass

	def write_DHT(self):
		pass

	def write_SOS(self):
		pass

	def write_compressed_bin(self):
		pass

	def write_data(self):
		pass

def test():
	my_pic1 = JPG('/tmp/wbt.jpg')
	my_pic1.read_data()
	

if __name__ == '__main__':
	test()
