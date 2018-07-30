#coding=utf-8

import sys

if __name__ == '__main__':
    arglen = len(sys.argv)

    print('使用方法:', sys.argv[0], 'filename [ start_1/end_1 ... start_N/end_N ]', file=sys.stderr)
    print('参数说明:', 'start_x(x=1...N) 表示待提取部分的起始偏移，end_x(x=1...N) 表示结束偏移', file=sys.stderr)
    print('         ', '注意：[start_x, end_x) 是前闭后开区间', file=sys.stderr)
    print('示    例:', sys.argv[0], 'a.txt 100/120 0x200/0x240', file=sys.stderr)
    print(file=sys.stderr)

    if arglen == 1:
        print('无命令行参数，退出', file=sys.stderr)
        exit()

    input_file = open(sys.argv[1], "rb")
    input_bytes = input_file.read()
    input_file.close()

    output_bytes = bytearray()
    for i in range(2, arglen):
        off_len = sys.argv[i]
        bytes_off_str, bytes_len_str = off_len.split('/')
        if bytes_off_str.startswith('0x') or bytes_off_str.startswith('0X'):
            bytes_offset = int(bytes_off_str,16)
        else:
            bytes_offset = int(bytes_off_str)
        if bytes_len_str.startswith('0x') or bytes_len_str.startswith('0X'):
            bytes_len = int(bytes_len_str,16)
        else:
            bytes_len = int(bytes_len_str)
        #output_bytes += input_bytes[bytes_offset:bytes_offset+bytes_len]
        output_bytes += input_bytes[bytes_offset:bytes_len]

    output_file = open(sys.argv[1]+".bak", "wb")
    output_file.write(output_bytes)
    output_file.close()
    print("writing %d bytes" % len(output_bytes), file=sys.stderr)
    sys.stdout.buffer.write(output_bytes)
