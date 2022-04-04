from PIL import Image
import os
import sys
import math
import matplotlib.pyplot as plt
from ast import literal_eval
import binascii


class Spring:
    def __init__(self):
        pass

    def file_to_bn(self, file_path: str) -> str:
        with open(file_path, "rb") as target_file:
            data = target_file.read()
            bn_str = "".join(format(i, "08b") for i in data)
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

        key_char = str()
        key_char_list = list()
        for i in key_list:
            if key_list.index(i) != 0:
                key_char += i
        temp = str()
        for i in key_char:
            temp += i
            if len(temp) == 8:
                key_char_list.append(chr(int(temp, 2)))
                temp = ""
        leftover_length = len(key_char) % 8
        if leftover_length != 0:
            leftover = key_char[(-1) * leftover_length :]
            while len(leftover) < 8:
                leftover = "0" + leftover
            key_char_list.append(chr(int(leftover, 2)))

        title = f"test/{group_constant}_{leftover_length}.txt"
        enc_key = str()
        for i in key_char_list:
            enc_key += i

        with open(title, "w") as f:
            f.write(enc_key)

        size = os.stat(title).st_size
        return size

    def generate_enc_file(self, bn_str: str, group_constant: int):
        key_dict, enc_list = self.generate_key_enc(bn_str, group_constant)
        enc_char = str()
        for i in enc_list:
            enc_char += i

        enc_char_list = list()
        temp = str()
        for i in enc_char:
            temp += i
            if len(temp) == 8:

                enc_char_list.append(chr(int(temp, 2)))
                temp = ""
        leftover_length = len(enc_char) % 8

        if leftover_length != 0:
            leftover = enc_char[(-1) * leftover_length :]

            while len(leftover) < 8:
                leftover = "0" + leftover

            enc_char_list.append(chr(int(leftover, 2)))

        title = f"test/{leftover_length}.txt"
        content = str()
        for i in enc_char_list:
            content += i
        with open(title, "w") as f:
            f.write(content)

        size = os.stat(title).st_size
        return size
