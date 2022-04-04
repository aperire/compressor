from mecha import cucha
from PIL import Image
import base64
import os

# 3.51
# 2.82
# 2.89
title = "yujin.bmp"
with open(title, "rb") as image:
    data = image.read()
    bn_str = "".join(format(i, "08b") for i in data)
print(len(bn_str) / 8)

gc = 10
"""compressor = cucha()
k_size = compressor.generate_key_file(bn_str, gc)
e_size = compressor.generate_enc_file(bn_str, gc)
print(k_size + e_size)"""


size_lst = list()
for gc in range(10, 50):
    compressor = cucha()

    k_size = compressor.generate_key_file(bn_str, gc)
    e_size = compressor.generate_enc_file(bn_str, gc)
    size_lst.append(int(k_size) + int(e_size))
    print(k_size + e_size)
1787994.0
