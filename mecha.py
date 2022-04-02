from PIL import Image
import os
import sys
import math
import matplotlib.pyplot as plt
from ast import literal_eval


class cucha:
    def __init__(self):
        pass

    def file_to_bn(self, file_path: str) -> str:
        with open(file_path, "rb") as target_file:
            f = target_file.read()
            bn = bytearray(f)
            bn_str = "".join(format(ord(i), "08b") for i in str(bn))
        return bn_str

    def generate_key_enc(self, bn_str: str, group_constant: int) -> str:
        group_list = list()
        group_temp = str()
        enc_list = list()
        leftover = str()
        group_repeatance = dict()

        for i in range(len(bn_str)):
            group_temp += bn_str[i]
            if i % group_constant == group_constant - 1:
                group_list.append(group_temp)
                group_temp = str()
        if len(bn_str) % group_constant != 0:
            for i in range(len(bn_str) % group_constant):
                leftover = bn_str[-i] + leftover

        for i in group_list:
            if i not in group_repeatance.keys():
                group_repeatance[i] = 1
            else:
                group_repeatance[i] += 1

        key_dict = dict(
            sorted(group_repeatance.items(), key=lambda group: group[1], reverse=True)
        )
        n = 0
        for i in list(key_dict.keys()):
            temp = str(bin(n))[2:]
            compress_code = str()
            for j in temp:
                compress_code += j
            key_dict.update({i: str(compress_code)})
            n += 1
        key_dict[leftover] = str(bin(n))[2:]

        digits = math.ceil(math.log(len(list(key_dict.values()))) / math.log(2))

        for i in group_list:
            val = key_dict.get(i)
            while len(val) < digits:
                val = "0" + val
            enc_list.append(val)
        enc_list.append(key_dict[leftover])

        for i, j in zip(key_dict.keys(), enc_list):
            key_dict[i] = j

        return key_dict, enc_list

    def generate_key_file(self, bn_str: str, group_constant: int):
        group_constant_bin = str(bin(group_constant))[2:]
        key_list = [group_constant_bin]
        key_dict, enc_list = self.generate_key_enc(bn_str, group_constant)

        for key, val in key_dict.items():
            key_list.append(f"{key}{val}")
        
        
        return key_list
    
    def generate_enc_file(self, bn_str: str, group_constant: int) -> 
