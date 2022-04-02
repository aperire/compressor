from mecha import cucha

bn_str = "000001100110111000010010101010010101010"

compressor = cucha()

key_dict, enc_list = compressor.generate_key_enc(bn_str, 10)
key_list = compressor.generate_key_file(bn_str, 10)
print(key_list)
