# coding=utf-8

import os, struct, sys, binascii as B, re
from hashlib import sha256

def computer_merkle_root(double_sha256_list, list_len):
    if list_len == 1:
        print("[%d] 2-SHA256 %s" % (0, str(B.b2a_hex(double_sha256_list[0]))[2:-1]))
        return double_sha256_list[0];

    for i in range(list_len):
        print("[%d] 2-SHA256 %s" % (i, str(B.b2a_hex(double_sha256_list[i]))[2:-1]))
    if list_len %2 == 1:
        double_sha256_list.append(double_sha256_list[-1])
        list_len += 1

    # 两两配对
    # X-X X-X
    #  / /
    # X X
    list_len = list_len // 2
    for i in range(list_len):
        double_sha256_list[i] = sha256(sha256(double_sha256_list[2*i]+double_sha256_list[2*i+1]).digest()).digest()
    del double_sha256_list[list_len:]
    return computer_merkle_root(double_sha256_list, list_len)

if __name__ == '__main__':
    arglen = len(sys.argv)

    print('使用方法:', sys.argv[0], '[ input_1 input_2 ... input_n ]', file=sys.stderr)
    print('参数说明: input_x (x=1...n) 是 Hexdump 形式的 2-SHA256 值', file=sys.stderr)
    print('          如果没有命令行参数，则从终端读入，读入的字符串为 Hexdump 形式的 2-SHA256 值', file=sys.stderr)
    print('示    例:', sys.argv[0], '3b...a3 ed...fd 7a...7b', file=sys.stderr)
    print('         ', sys.argv[0], file=sys.stderr)
    print(file=sys.stderr)

    double_sha256_list = []

    if arglen == 1:
        while True:
            try:
                a = input()
                input_bytes = B.a2b_hex(a)
                double_sha256_list.append(input_bytes)
            except EOFError:
                #print('end of input')
                break
        merkle_root = computer_merkle_root(double_sha256_list, len(double_sha256_list))
        merkle_root_rev = merkle_root[::-1]
        ret = str(B.b2a_hex(merkle_root))[2:-1]
        ret_rev = str(B.b2a_hex(merkle_root_rev))[2:-1]
        print()
        print('Merkle Root =', ret)
        print('             ', ret_rev, '-- little Endian')
        exit()

    for i in range(1, arglen):
        input_bytes = B.a2b_hex(sys.argv[i])
        double_sha256_list.append(input_bytes)

    merkle_root = computer_merkle_root(double_sha256_list, len(double_sha256_list))
    merkle_root_rev = merkle_root[::-1]
    ret = str(B.b2a_hex(merkle_root))[2:-1]
    ret_rev = str(B.b2a_hex(merkle_root_rev))[2:-1]
    print('Merkle Root =', ret)
    print('             ', ret_rev, '-- little Endian')
