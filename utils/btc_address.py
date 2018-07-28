#coding=utf-8
#print('''
#            +----------+
# +-----+    |          |RIPEMD160(SHA256(.))结果记为 HASH
# |公钥P|    |          V
# +-----+    |  +----+------+
#    |       ^  |0x00| HASH | --> SHA256
#    V       |  +----+------+        |
#  SHA256    |   \           \       V
#    |       |    \           \   SHA256
#    V       |     \记为P_HASH \     |取前4字节记为Check
# RIPEMD160  |      \           \    V
#    |       |       +----+------+-----+
#    +--->---+       |0x00| HASH |Check| --> BASE58 编码 --> 比特币地址
#                    +----+------+-----+                     记为 OUT
#                            记为 IN
# 比特币地址(钱包地址)生成
# (1)私钥 --> 公钥P=(X,Y)
#    为后续计算方便, 公钥P保存为下列两种16进制格式
#            压缩格式 P = 04    X Y
#          非压缩格式 P = 02/03 X   -- 02:Y为偶数 03:Y为奇数
# (2) HASH   = RIPEMD160(SHA256(P))
# (3) P_HASH = 0x00 | HASH
# (4) Check  = SHA256(SHA256(P_HASH))
# (5) IN     = P_HASH | Check
# (6) OUT    = BASE58(IN)
#''')

import sys, hashlib
from hashlib import sha256
import binascii as B

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('使用方法:', sys.argv[0], 'pub   公钥信息(P=04|X|Y 或 02|X 或 03|X)')           # condition 1
        print('         ', sys.argv[0], 'pri   私钥信息(P=K)')                                # condition 3
        print('         ', sys.argv[0], 'pri-c 私钥信息(P=K)')                                # condition 2
        print()
        print('         ', sys.argv[0], 'hash  XXXX -- 由公钥中间值XXXX生成公钥的比特币地址') # condition 4
        print('         ', ' '*len(sys.argv[0]), '              其中, XXXX=RIPEMD160(SHA256(P))')
        print()
        print('示    例:', sys.argv[0],         'pub 046639E8E50A89C27CB21EA2B3D8E6E39541B92BACBB6CEC1A32E6A0B91D008E7F035AFA91410C69A0309E423027C6FB631F498E07A996FA177DC575F49F251924')
        print('         ', ' '*len(sys.argv[0]),'      | ---------------------------- X ----------------------------- || ---------------------------- Y ----------------------------- |')
        print()
        print('         ', sys.argv[0],         'pub 0202a406624211f2abbdc68da3df929f938c3399dd79fac1b51b0e4ad1d26a47aa  # 公钥：压缩格式')
        print('         ', ' '*len(sys.argv[0]),'      | ---------------------------- X ----------------------------- |')
        print()
        print('         ', sys.argv[0],         'pri   B5A948BD1650CB7FA30E5E820B54265E4963CF6591AE7CCE5F4EE8D1BA62132C  # 私钥：WIF 未压缩格式')
        print('         ', ' '*len(sys.argv[0]),'      | ---------------------------- K ----------------------------- |')
        print()
        print('         ', sys.argv[0],         'pri-c B5A948BD1650CB7FA30E5E820B54265E4963CF6591AE7CCE5F4EE8D1BA62132C  # 私钥：WIF 压缩格式')
        print('         ', ' '*len(sys.argv[0]),'      | ---------------------------- K ----------------------------- |')
        exit()

    if sys.argv[1].startswith('pub') :
        key_flag = 1
    elif sys.argv[1].startswith('pri-c') :
        key_flag = 2
    elif sys.argv[1].startswith('hash') :
        key_flag = 4
    else :
        key_flag = 3

    if key_flag != 4 :
        Key = B.a2b_hex(sys.argv[2])
        temp = hashlib.new('sha256', Key).digest()
        HASH = hashlib.new('ripemd160', temp).digest()
        bytes = B.b2a_hex(temp)
        print('Sha256(Key) :', str(bytes)[2:-1])
        bytes = B.b2a_hex(HASH)
        print('HASH:        ', str(bytes)[2:-1], "        -- HASH = Ripemd160(Sha256(Key))")
    else :
        HASH = B.a2b_hex(sys.argv[2])
        bytes = B.b2a_hex(HASH)
        print('HASH:        ', str(bytes)[2:-1], "        -- HASH = Ripemd160(Sha256(Key))")

    if key_flag == 1 or key_flag == 4 :
        P_HASH = b'\x00' + HASH
        bytes = B.b2a_hex(P_HASH)
        print('P_HASH:    ', str(bytes)[2:-1], '        -- P_HASH = 0x00 | HASH')
    elif key_flag == 3 :
        P_HASH = b'\x80' + Key
        # Add a 0x80 byte in front of it for mainnet addresses
        bytes = B.b2a_hex(P_HASH)
        print('P_HASH:', str(bytes)[2:-1], '-- P_HASH = 0x80 | Prikey')
    elif key_flag == 2:
        P_HASH = b'\x80' + Key + b'\x01'
        # Add a 0x80 byte in front of it for mainnet addresses
        # Also add a 0x01 byte at the end if the private key will correspond to a compressed public key
        bytes = B.b2a_hex(P_HASH)
        print('P_HASH:', str(bytes)[2:-1], '-- P_HASH = 0x80 | Prikey | 0x01')

    temp = hashlib.new('sha256', P_HASH).digest()
    Check = hashlib.new('sha256', temp).digest()
    bytes = B.b2a_hex(Check)
    print('Check:                                               ', str(bytes)[2:10], '-- Check = SHA256(SHA256(P_HASH))[0:4]')

    temp = P_HASH + Check[0:4]
    bytes = B.b2a_hex(temp)
    print('BASE58_IN: ', str(bytes)[2:-1])

    # base58 encode
    # code_string = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    # x = convert_bytes_to_big_integer(BASE58_IN)
    # output_string = ""
    # while(x > 0)
    # {
    #   (x, remainder) = divide(x, 58)
    #   output_string.append(code_string[remainder])
    # }
    # repeat(number_of_leading_zero_bytes_in_hash)
    # {
    #   output_string.append(code_string[0]);
    # }
    # output_string.reverse();
    # 核心：将 BASE58_IN 看作一个大整数，表示成以58为基数的数
    code_string = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    x = int(str(bytes)[2:-1], 16)
    output_string = ''
    while(x > 0) :
        (x, remainder) = divmod(x, 58)
        output_string = output_string + code_string[remainder]
    if key_flag == 1 :
        print('BASE58_OUT:', '1'+output_string[::-1])
    elif key_flag == 2 :
    		print('BASE58_OUT:', output_string[::-1], '-- WIF-compressed')
    else :
        print('BASE58_OUT:', output_string[::-1], '-- WIF')