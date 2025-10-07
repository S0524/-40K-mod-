#!/usr/bin/env python3

from collections import namedtuple
import os
import struct
import sys

# 定义一个名为File的namedtuple，包含文件名和数据
File = namedtuple('File', ['name', 'data'])

class N2PK():
    def __init__(self, filename=None):
        self._body = b''
        self._files = []
        if filename:
            self._import_from(filename)

    def _import_from(self, filename):
        # 从文件读取字节数据
        data = self._get_bytes(filename)

        # 解析n2pk头部
        header_format = '<i32sQ'
        header_length = struct.calcsize(header_format)
        (_pad, _neocore, body_length) = struct.unpack_from(header_format, data)

        # 隔离主体数据
        self._body = data[header_length:header_length + body_length]

        # 构建目录表
        toc = data[header_length + body_length:]
        toc_format = '<i'
        (num_files,) = struct.unpack_from(toc_format, toc)

        toc_offset = struct.calcsize(toc_format)
        # 获取每个文件的元数据和数据
        self._files = []
        for f in range(num_files):
            meta_len_format = '<ii'
            (_unknown, name_length) = struct.unpack_from(meta_len_format, toc[toc_offset:])
            toc_offset += struct.calcsize(meta_len_format)

            name_format = '<' + str(name_length * 2) + 'sxxqq'
            (raw_filename, file_offset, file_size) = struct.unpack_from(name_format, toc[toc_offset:])
            filename = raw_filename.decode('utf-16')
            toc_offset += struct.calcsize(name_format)

            self._files.append(File(filename, self._body[file_offset:file_offset + file_size]))

    def _get_bytes(self, filename):
        # 从文件中读取字节数据
        with open(filename, 'rb') as file:
            b = file.read()
            return b

    def add_file(self, filename, data):
        # 添加文件到N2PK对象
        self._files.append(File(filename, data))
        self._body += data

    def pack_files(self, output_filename):
        # 构建文件体
        body = b''.join([f.data for f in self._files])

        # 构建目录表
        toc = struct.pack('<i', len(self._files))
        for f in self._files:
            name_length = len(f.name.encode('utf-16')) // 2
            toc += struct.pack('<ii', 0, name_length)
            toc += struct.pack('<' + str(name_length * 2) + 'sxxqq', f.name.encode('utf-16'), 0, len(f.data))

        # 构建文件头
        header = struct.pack('<i32sQ', 0, b'NEOCORE', len(body))

        # 写入文件
        with open(output_filename, 'wb') as output:
            output.write(header)
            output.write(body)
            output.write(toc)

def main(argv):
    if len(sys.argv) < 3:
        print(f'Usage: {sys.argv[0]} <input_directory> <output_filename>')
        sys.exit(-1)
    
    input_directory = argv[1]
    output_filename = argv[2]

    # 创建N2PK对象
    package = N2PK()

    # 读取目录中的所有文件
    for dirpath, _, filenames in os.walk(input_directory):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            with open(file_path, 'rb') as file:
                data = file.read()
            package.add_file(os.path.relpath(file_path, input_directory), data)

    # 打包文件
    package.pack_files(output_filename)
    print(f'Packed files from {input_directory} into {output_filename}')

if __name__ == "__main__":
    main(sys.argv)