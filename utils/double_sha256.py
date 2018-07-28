#coding=utf-8

import sys, hashlib
from hashlib import sha256
import binascii as B

def dbl_sha256(input_bytes):
    temp = hashlib.new('sha256', input_bytes).digest()
    return hashlib.new('sha256', temp).digest()

if __name__ == '__main__':
    arglen = len(sys.argv)

    if arglen == 1:
        print('使用方法:', sys.argv[0], '[ input_1 input_2 ... input_n ]', file=sys.stderr)
        print('参数说明:', 'input_x (x=1...n) 是文件名 或 Hexdump 形式的字符串 -- 优先当作文件处理', file=sys.stderr)
        print('          如果没有命令行参数，则从终端读入，读入的字符串为 Hexdump 形式', file=sys.stderr)
        print('示    例:', sys.argv[0], 'e8...e5 0a...89 c2...7c', file=sys.stderr)
        print('         ', sys.argv[0], 'a.txt b.txt', file=sys.stderr)
        print('         ', sys.argv[0], 'e8...e5 0a...89 a.txt', file=sys.stderr)
        print('         ', sys.argv[0], file=sys.stderr)
        print(file=sys.stderr)
        print('无命令行参数，从终端读入', file=sys.stderr)
        while True:
            try:
                a = input()
                input_bytes = B.a2b_hex(a)
                ret = dbl_sha256(input_bytes)
                hex_asc_str = B.b2a_hex(ret)
                print(str(hex_asc_str)[2:-1])
            except EOFError:
                #print('end of input')
                break
        exit()

    for i in range(1, arglen):
        # print(sys.argv[i])
        try: # 先以文件方式打开
            input_file = open(sys.argv[i], "rb")
            input_bytes = input_file.read()
            input_file.close()
        except FileNotFoundError:
            # print("打开文件失败，当字符串读入")
            input_bytes = B.a2b_hex(sys.argv[i])
        ret = dbl_sha256(input_bytes)
        hex_asc_str = B.b2a_hex(ret)
        print(str(hex_asc_str)[2:-1])
