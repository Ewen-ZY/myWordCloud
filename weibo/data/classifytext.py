#!/usr/bin/env python3

import os
import re
import codecs

pathDir = os.path.dirname(__file__)

# 数据集路径
datafile_path = './YunNan_weibo_08-10.UTF-8.csv'

datafile = open(os.path.join(pathDir, datafile_path))

# 若分类目录不存在则创建
if not os.path.exists(os.path.join(pathDir, 'classify')):
    os.mkdir(os.path.join(pathDir, 'classify'))
    print('创建目录classify...')

# 将文本按日期分类
while True:
    lines = datafile.readlines(100000)
    if not lines:
        break
    for line in lines:
        match = re.search(r'^\d{4}-\d{2}-\d{2}', line)
        if match:
            filename = 'classify/YunNan_weibo_' + match.group(0) + '.txt'
            if not os.path.exists(os.path.join(pathDir, filename)):
                newfile = open(os.path.join(pathDir, filename), 'w')
                newfile.close()
            afile = codecs.open(os.path.join(pathDir, filename), 'a', 'UTF-8')
            afile.write(line.split(',')[3] + '\n')
            afile.close()
            print('分类未完成...')
