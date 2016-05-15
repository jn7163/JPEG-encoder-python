#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Time-stamp: < jpeg_code.py 2016-05-15 16:15:10 >
"""
JPEG编码
"""

import block_split
import dct
import quantize
import zig_zag_scan
import dc_ac_encode
import entropy_encode
import numpy as np
import struct
import io_jpg
import io_bmp

from quantize import FORWARD
from quantize import LUMINANCE


def jpeg_encode(input_matrix):
	output_hex = ''
	each_block_encoded = []
	# 填充block长宽为8的整数
	temp_matrix = block_split.padding_dummy_edge(input_matrix)
	# 分割MCU
	blocks_spilted = block_split.split_to_blocks(temp_matrix)[0]
	del temp_matrix
	last_DC_value = 0
	block_num = 1
	# 对每一个block处理
	for block in blocks_spilted:
		print "----------------\nBLOCK #%d encoding:" % block_num
		block_num += 1
		# 计算DCT变换
		DCT_table = dct.forward_dct(block - 128)
		# 量化
		table_quantized = quantize.get_quantisation(DCT_table)
		# zig-zag顺序读取数据
		result_zig_zag = zig_zag_scan.get_seq_1x64(table_quantized)
		# 直流、交流编码
		encoded_1 = dc_ac_encode.DC_AC_encode(result_zig_zag, last_DC_value)
		print encoded_1
		# 熵编码（哈夫曼）
		encoded_2 = entropy_encode.get_entropy_encode(encoded_1)
		each_block_encoded.append(encoded_2)
		# print encoded_2

		# 记下当前块的DC值供下一个编号
		last_DC_value = table_quantized[0, 0]


	# 二进制编码
	output_hex = entropy_encode.get_encoded_to_hex(each_block_encoded)
	return output_hex

def jpeg_decode(input_hex, quantize_table, width, height):
	decoded_blocks = []
	previous_DC_value = 0
	# 熵解码
	entropy_decoded_bin = entropy_encode.get_decoded_from_hex(input_hex, is_debug = True)
	entropy_decoded_blocks = entropy_encode.get_entropy_decode(entropy_decoded_bin, is_debug=False)

	# 对每一个MCU块进行解码
	for block in entropy_decoded_blocks:
		# DC AC解码
		decoded_dc_ac = dc_ac_encode.DC_AC_decode(block, previous_DC_value)
		# zig-zag还原成8x8矩阵
		result_zig_zag = zig_zag_scan.restore_matrix_from_1x64(decoded_dc_ac)

		# 反量化
		table_unquantized = quantize.get_quantisation(result_zig_zag, quantize_table, False)

		# 逆DCT变换
		IDCT_table = dct.inverse_dct(table_unquantized)
		# 限幅
		for i, j in [(i, j) for i in xrange(8) for j in xrange(8)]:
			if IDCT_table[i, j] >= (-128) and IDCT_table[i, j] < 128:
				continue
			elif IDCT_table[i, j] > 127:
				IDCT_table[i, j] = 127
			else:
				IDCT_table[i, j] = -128
		decoded_blocks.append(IDCT_table + 128)
		# 更新DC值
		previous_DC_value = result_zig_zag[0, 0]


	# 合并前计算padded尺寸
	width_padded, height_padded = block_split.calc_new_size(width, height)
	# 计算MCU的行列数
	columns, rows = width_padded / 8, height_padded / 8
	# 合并
	merged_matrix = block_split.merge_blocks(decoded_blocks, rows, columns)
	# 移除多余的边缘像素
	final_matrix = block_split.remove_dummy_edge(merged_matrix, width, height)
	return final_matrix



def test():
	my_pic = io_jpg.JPG('/tmp/43.jpg')
	my_pic.read_data()
	(test_hex, width, height, dqt) = my_pic.get_data()

	decoded_jpg = jpeg_decode(test_hex, dqt[0], width, height)

	# with open('/tmp/from_jpg_py.txt','w') as f:
	# 	for y in xrange(height):
	# 		for x in xrange(width):
	# 			f.write(hex(int(decoded_jpg[y, x]))[2:])
	# 			f.write(' ')
	# 		f.write('\n')
			

	# exit(0)
	my_pic2 = io_bmp.BMP('/tmp/43.bmp', decoded_jpg)
	my_pic2.write_bmp()


if __name__ == "__main__":
	test()
