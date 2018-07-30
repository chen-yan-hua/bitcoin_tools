#coding=utf-8

import sys

if __name__ == '__main__':
    arglen = len(sys.argv)

    print('使用方法:', sys.argv[0], 'input_1 input_2 [ input_3 ... input_N ]', file=sys.stderr)
    print('参数说明:', 'input_x (x=1...n) 是文件名 或 Hex 表示的字节串', file=sys.stderr)
    print('          如果参数名以 0x/0X 开头，则表示是字节串，否则是文件', file=sys.stderr)
    print('示    例:', sys.argv[0], 'a.txt 0x00 b.txt 0x1234 c.txt', file=sys.stderr)
    print(file=sys.stderr)

    if arglen == 1:
        print('无命令行参数，退出', file=sys.stderr)
        exit()

    output_bytes = bytearray()
    for i in range(1, arglen):
        file_name = sys.argv[i]
        if file_name.startswith('0x') or file_name.startswith('0X'): # 字节的 Hex 表示字串
            input_bytes = bytes.fromhex(file_name[2:])
        else:
            input_file = open(file_name, "rb")
            input_bytes = input_file.read()
            input_file.close()
        output_bytes += input_bytes

    output_file = open(sys.argv[1]+".bak", "wb")
    output_file.write(output_bytes)
    output_file.close()
    print("writing %d bytes" % len(output_bytes), file=sys.stderr)
    sys.stdout.buffer.write(output_bytes)