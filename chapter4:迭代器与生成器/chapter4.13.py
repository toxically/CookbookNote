#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import fnmatch
import gzip
import bz2
import re


def gen_find(filepat, top):
    """
        Find all filenames in a directory tree that match a shell wildcard pattern
    :param filepat: 文件名pattern
    :param top:根目录地址

    补充：
    1. os.walk 返回一个(dirpath, dirnames, filenames)元组
    2.fnmatch是匹配过滤文件名称，匹配的模式是符合Unix shell-style wildcards
        通配符如下：
        Pattern | Meaning
        *         匹配所有
        ？        匹配任意单个字符
        [seq]     匹配列表里任意字符
        [!swq]    不匹配列表里任意字符

        fnmatch.fnmatch(filename,pattern) 结果返回类型为Bool；函数用于判断文件名是否匹配
        fnamtch.filter(names,pattern) 函数用于返回符合匹配条件的文件名列表的子集

    """
    for path, dirlist, filelist in os.walk(top):
        for name in fnmatch.filter(filelist, filepat):
            yield os.path.join(path, name)


def gen_opener(filenames):
    """
        每一次打开一个文件的序列。当处理下一个迭代时，关闭当前已打开的文件
        注：
            1.t是windows平台特有的所谓text mode(文本模式）,区别在于会自动识别windows平台的换行符
            2.rt模式下，python在读取文本时会自动把\r\n转换成\n
    """
    for filename in filenames:
        if filename.endswith('.gz'):
            f = gzip.open(filename, 'rt')
        elif filename.endswith('.bz2'):
            f = bz2.open(filename, 'rt')
        else:
            f = open(filename, 'rt')
        yield f
        f.close()


def gen_concatenate(iterators):
    """
        将所有迭代器chain到一个序列中
    """
    for it in iterators:
        yield from it


def gen_grep(pattern, lines):
    """
        查找序列中符合匹配条件的行
    """
    pat = re.compile(pattern)
    for line in lines:
        if pat.search(line):
            yield line


if __name__ == '__main__':
    # 查找含有robot字符串的日志行
    log_names = gen_find('access-log*', '.')
    files = gen_opener(log_names)
    lines = gen_concatenate(files)
    robot_lines = gen_grep('robot', lines)
    for line in robot_lines:
        print(line)
