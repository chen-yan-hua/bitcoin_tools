# https://pypi.python.org/pypi/ecc/0.0.1
from ecc.elliptic import mul,add

import os, sys, getopt, hashlib, binascii as B

def Usage():
    print('使用方法:', sys.argv[0], '[-m sha1/sha256/...] (-f tobeSign | -s tobeSign | -h tobeSign) 曲线名 公钥X(HEX) 公钥Y(HEX) 签名r(HEX) 签名s(HEX)')
    print('参数说明: -m 表示签名前使用指定的算法计算摘要 e=Hash(tobeSign)，否则 tobeSign 已经是摘要(作为e直接进行签名)')
    print('          -f 表示 tobeSign 为文件')
    print('          -s 表示 tobeSign 为可显示的 ASCII 字符串，例如 "123"')
    print('          -h 表示 tobeSign 字符串的 16 进制表示，例如 313233，即字符串"123"')
    print('          曲线名可使用: prime256v1(即secp256r1) secp256k1 secp384r1 secp521r1 sm2p256v1(国密SM2曲线)')
    print('示    例:', sys.argv[0], '-m sha256 -f tobeHash prime256v1 公钥X 公钥Y 签名r 签名s -- 计算文件摘要e，然后验证签名')
    print('         ', sys.argv[0], '          -f file.bin prime256v1 公钥X 公钥Y 签名r 签名s -- 文件内容就是摘要e，直接验证签名')
    print('         ', sys.argv[0], '-m sha256 -s HelloYou prime256v1 公钥X 公钥Y 签名r 签名s -- 计算 "HelloYou" 的摘要e，然后验证签名')
    print('         ', sys.argv[0], '-m sha256 -h 01020304 prime256v1 公钥X 公钥Y 签名r 签名s -- 计算 0x01020304 的摘要e，然后验证签名')
    print('         ', sys.argv[0], '          -h D2....4B prime256v1 公钥X 公钥Y 签名r 签名s -- 0xD2...4B 就是摘要e，直接验证签名')

try:
    opts, args = getopt.getopt(sys.argv[1:], 'm:f:s:h:')
except getopt.GetoptError as err:
    print (str(err))
    Usage()
    exit()

if len(opts) == 0 or len(args) == 0:
    Usage()
    exit()

print()

for o, a in opts:
    if o in ('-m', '--help'):
        dgst = a
    elif o in ('-f', '--version'):
        filename = a
    elif o in ('-s', '--output'):
        ascii_str = a
        print('string',a)
    elif o in ('-h', '--output'):
        hex_str = a
        print('hex',a)
    else:
        print ('unhandled option')
        exit()

CurveName,Ax,Ay,r,s = args

if CurveName == "prime256v1" or CurveName == "secp256r1":
    p=0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFF
    a=0xFFFFFFFF00000001000000000000000000000000FFFFFFFFFFFFFFFFFFFFFFFC
    b=0x5AC635D8AA3A93E7B3EBBD55769886BC651D06B0CC53B0F63BCE3C3E27D2604B
    Gx=0x6B17D1F2E12C4247F8BCE6E563A440F277037D812DEB33A0F4A13945D898C296
    Gy=0x4FE342E2FE1A7F9B8EE7EB4A7C0F9E162BCE33576B315ECECBB6406837BF51F5
    order=0xFFFFFFFF00000000FFFFFFFFFFFFFFFFBCE6FAADA7179E84F3B9CAC2FC632551
elif CurveName == "secp256k1":
    p=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
    a=0x0000000000000000000000000000000000000000000000000000000000000000
    b=0x0000000000000000000000000000000000000000000000000000000000000007
    Gx=0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
    Gy=0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
    order=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
elif CurveName == "secp384r1":
    p=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFFFF0000000000000000FFFFFFFF
    a=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFFFF0000000000000000FFFFFFFC
    b=0xB3312FA7E23EE7E4988E056BE3F82D19181D9C6EFE8141120314088F5013875AC656398D8A2ED19D2A85C8EDD3EC2AEF
    Gx=0xAA87CA22BE8B05378EB1C71EF320AD746E1D3B628BA79B9859F741E082542A385502F25DBF55296C3A545E3872760AB7
    Gy=0x3617DE4A96262C6F5D9E98BF9292DC29F8F41DBD289A147CE9DA3113B5F0B8C00A60B1CE1D7E819D7A431D7C90EA0E5F
    order=0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFC7634D81F4372DDF581A0DB248B0A77AECEC196ACCC52973
elif CurveName == "secp521r1":
    p=0x01FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
    a=0x01FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFC
    b=0x0051953EB9618E1C9A1F929A21A0B68540EEA2DA725B99B315F3B8B489918EF109E156193951EC7E937B1652C0BD3BB1BF073573DF883D2C34F1EF451FD46B503F00
    Gx=0x00C6858E06B70404E9CD9E3ECB662395B4429C648139053FB521F828AF606B4D3DBAA14B5E77EFE75928FE1DC127A2FFA8DE3348B3C1856A429BF97E7E31C2E5BD66
    Gy=0x011839296A789A3BC0045C8A5FB42C7D1BD998F54449579B446817AFBD17273E662C97EE72995EF42640C550B9013FAD0761353C7086A272C24088BE94769FD16650
    order=0x01FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFA51868783BF2F966B7FCC0148F709A5D03BB5C9B8899C47AEBB6FB71E91386409
elif CurveName == "sm2p256v1":
    p=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
    a=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
    b=0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
    Gx=0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7
    Gy=0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0
    order=0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
else:
    print ('未知名的曲线: ' + CurveName)
    exit()

# 公钥
Ax = int(Ax,16)
Ay = int(Ay,16)
print('Ax: '+hex(Ax))
print('Ay: '+hex(Ay))

if 'dgst' in dir() :
    h = hashlib.new(dgst)
    if 'filename' in dir():
        f = open(filename, 'rb');
        tmp = f.read();
        f.close();
        h.update(tmp)
        print('文件 %s 摘要:'%filename, h.hexdigest())
    elif 'ascii_str' in dir():
        h.update(str.encode(ascii_str)) # <class 'str'> --> <class 'bytes'>
        print('字符串 %s 摘要:'%ascii_str, h.hexdigest())
    elif 'hex_str' in dir():
        h.update(B.a2b_hex(hex_str)) # hex-str --> <class 'bytes'>
        print('HEX字串 0x%s 摘要:'%hex_str, h.hexdigest())
    else:
        print('参数错误: -m 存在，-f -s -h 必须有其一')
        exit()
    e = h.digest()
else:
    if 'filename' in dir():
        f = open(filename, 'rb');
        e = f.read();
        f.close();
        print('文件 %s 内容即摘要:'%filename, str(e))
    elif 'hex_str' in dir():
        e = B.a2b_hex(hex_str) # hex-str --> <class 'bytes'>
        print('HEX字串 0x%s 即摘要'%hex_str)
    else:
        print('参数错误: -m 不存在，-f -h 必须有其一')
        exit()

e = int.from_bytes(e, byteorder='big') # 转换成 int

# 签名内容
r = int(r,16)
s = int(s,16)
print('r: '+hex(r))
print('s: '+hex(s))

# inverse of s
w = pow(s, order-2, order)

u1 = (e*w)%order
u2 = (r*w)%order

n = p
p = n-a
q = n-b
g = (Gx,Gy)
P = (Ax,Ay)

P1 = mul(p, q, n, g, u1)
P2 = mul(p, q, n, P, u2)
x,y = add(p, q, n, P1, P2)
print('result r: ' + hex(x%order))
print('origin r: ' + hex(r))
if x%order == r:
    print('\nsignature is valid')
else:
    print('\nsignature is NOT valid')
