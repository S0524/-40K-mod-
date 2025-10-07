#!/usr/bin/env python3

from collections import namedtuple
import os
import os.path
import struct
import sys

# 定义一个名为File的namedtuple，包含文件名和数据
File = namedtuple('File', ['name', 'data'])

class N2PK():
    def __init__(self, filename):
        self._body = None
        self._files = []
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

    @property
    def filenames(self):
        # 返回所有文件的名称列表
        return [f.name for f in self._files]

    def write_files(self, output_directory='./'):
        # 将所有文件写入指定目录，如果文件已存在则覆盖
        for f in self._files:
            name = os.path.join(output_directory, f.name)
            with open(name, 'wb') as output:
                output.write(f.data)


def main():
    # 提示用户输入根目录
    root_directory = input("请输入包含.n2pk文件的根目录路径: ")

    # 可选的输出目录
    output_directory = root_directory
    use_custom_output = input("是否使用自定义输出目录？(y/n): ").strip().lower()
    if use_custom_output == 'y':
        output_directory = input("请输入输出目录路径: ")
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

    # 遍历目录并查找所有.n2pk文件
    for dirpath, _, filenames in os.walk(root_directory):
        print(f'Searching in directory: {dirpath}')  # 调试输出
        for filename in filenames:
            if filename.lower().endswith('.n2pk'):  # 大小写不敏感的文件扩展名匹配
                input_filename = os.path.join(dirpath, filename)
                output_dir = os.path.join(output_directory, os.path.relpath(dirpath, root_directory))

                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)

                package = N2PK(input_filename)
                print(f'Unpacking {input_filename} into {output_dir}')
                for file_name in package.filenames:
                    print(f'  {file_name}')
                package.write_files(output_dir)

                # 解压成功后删除原.n2pk文件
                os.remove(input_filename)


if __name__ == "__main__":
    main()