#!/usr/bin/env python3

# 作者：赖伟文
# 邮箱：lwwens@gmail.com ; lai_wei_wen@qq.com ;
# 时间：2019-01-03 week4 08:04:30

import os
import codecs
import jieba.analyse
import matplotlib.pyplot as plt
import matplotlib as mpl
from wordcloud import WordCloud
from os import path

cur_dir = path.dirname(__file__)
data_filename = './classify/YunNan_weibo_2017-08-08.txt'
fenci_filename = './fenci/2017-08-08.txt'
stopword_file = './fenci/stopword.txt'
wcfont_path = './fonts/SimFang.ttf'
mplfont_path = './fonts/SimHei.ttf'
wc_image_path = './fenci/2017-08-08.jpg'

with codecs.open(path.join(cur_dir, data_filename), 'r', encoding='UTF-8') as data_file:
    data = []
    # 添加停用词
    jieba.analyse.set_stop_words(path.join(cur_dir, stopword_file))

    # 通过词频获取关键字
    for text in data_file.readlines(100000):
        data.extend(jieba.analyse.extract_tags(text, topK=40))
    data = ' '.join(data)
    with codecs.open(path.join(cur_dir, fenci_filename), 'w', encoding='UTF-8') as fenci_file:
        fenci_file.write(data)
    word_cloud = WordCloud(font_path=wcfont_path).generate(data)

    # 词云显示
    mplfont = mpl.font_manager.FontProperties(fname=mplfont_path)
    mpl.rcParams['axes.unicode_minus'] = False
    plt.figure()
    plt.title('微博文本词云', fontproperties=mplfont, fontsize=30)
    plt.imshow(word_cloud, interpolation="bilinear")
    plt.axis('off')
    plt.show()

    # 保存词云图片
    word_cloud.to_file(wc_image_path)
