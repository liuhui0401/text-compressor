# -*- coding:utf-8 -*-

import argparse
import math
import jieba
import numpy as npy
from utils import *

import os
import sys

os.chdir(sys.path[0])


class CompressorExample:
    """
    Simply compresses nothing.
    """

    def compress(self, input_file, output_file):
        with open(input_file, "r") as f:
            text = f.read()

        with open(output_file, "w") as f:
            f.write(text)

    def decompress(self, input_file, output_file):
        with open(input_file, "r") as f:
            text = f.read()

        with open(output_file, "w") as f:
            f.write(text)


class Compressor:
    def __init__(self):
        """
        Your code here (if necessary)
        """
        pass

    def compress(self, input_file, output_file):
        """Compress Chinese documents.

        Perform word segmentation on the document, 
        convert the segmented words into 0/1 strings, 
        and then into bytes, for compression.
        """

        # Load the Huffman dictionary
        huffman_dict = npy.load("./static/huffman_dict.npy").item()
        tmp_dict = {}
        out_dict = {}
        tmp_list = []
        with open(input_file, "r") as f:
            novel = f.read()
        word_list = jieba.lcut(novel)

        # Count unrecorded characters
        ans = 0
        for word in word_list:
            if word in huffman_dict:
                ans += 1
                continue
            for char in word:
                if char in huffman_dict:
                    continue
                if char not in tmp_list:
                    tmp_list.append(char)

        # Single character length
        if len(tmp_list) == 0:
            per_len = 0
        else:
            per_len = int(math.log(len(tmp_list), 2))
            if int(math.pow(2, per_len)) < len(tmp_list):
                per_len += 1

        # Write this article dictionary
        head_str = huffman_dict["qaz666"]
        tlen = len(tmp_list)
        for i in range(tlen):
            word = tmp_list[i]
            tmp_dict[word] = head_str + int2binary(i, per_len)
            out_dict[head_str + int2binary(i, per_len)] = word

        # Compress data
        buff = []
        for word in word_list:
            if word in huffman_dict:
                buff.append(huffman_dict[word])
            else:
                for char in word:
                    if char in huffman_dict:
                        buff.append(huffman_dict[char])
                    else:
                        buff.append(tmp_dict[char])
        str_buff = "".join(buff)

        # Add dictionary
        # The first 24 bits are the dictionary length,
        # then 8 bits are pre_len, the next is the dictionary,
        # and then the Huffman code
        str_dict = str(out_dict)
        byt_dict = bytes(str_dict, encoding="UTF-8")
        output = (
            binary2bytes(int2binary(len(byt_dict), 24))
            + binary2bytes(int2binary(per_len, 8))
            + byt_dict
            + binary2bytes(str_buff, True)
        )

        with open(output_file, "wb") as f:
            f.write(output)

    def decompress(self, input_file, output_file):
        """Decompress Chinese documents.

        Convert the stored bytes into 0/1 strings, 
        find the corresponding strings in the dictionary, and output
        """

        # Load the Huffman dictionary
        huffman_dict = npy.load("./static/bit_to_huff.npy").item()

        # Read compressed files
        with open(input_file, "rb") as f:
            tmp = f.read()
        tlen = int.from_bytes(tmp[:3], byteorder="big", signed=False)
        pre_len = int.from_bytes(tmp[3:4], byteorder="big", signed=False)
        if pre_len != 0:
            str_dict = str(tmp[4: tlen + 4], encoding="utf-8")
            my_dict = eval(str_dict)
        else:
            str_dict = ""
        str_buff = bytes2binary(tmp[tlen + 4:])

        # Unzip the data
        output = ""
        tmp_str = ""
        my_read = False
        tcnt = 0
        for char in str_buff:
            tmp_str += char
            if my_read == True:
                tcnt = tcnt - 1
                if tcnt == 0:
                    my_read = False
                    output += my_dict[tmp_str]
                    tmp_str = ""
                continue
            if tmp_str not in huffman_dict:
                continue
            if huffman_dict[tmp_str] == "qaz666":
                my_read = True
                tcnt = pre_len
            else:
                output += huffman_dict[tmp_str]
                tmp_str = ""

        with open(output_file, "w") as f:
            f.write(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", type=str, nargs=2, help="Compress a file")
    parser.add_argument("-x", type=str, nargs=2, help="Decompress a file")
    parser.add_argument(
        "--method", type=str, default="Compressor", help="Compressor to use"
    )

    args = parser.parse_args()
    exec("compresser = {}()".format(args.method))

    try:
        input_file = args.c[0]
        output_file = args.c[1]
        compresser.compress(input_file, output_file)
    except TypeError:
        pass

    try:
        input_file = args.x[0]
        output_file = args.x[1]
        compresser.decompress(input_file, output_file)
    except TypeError:
        pass
