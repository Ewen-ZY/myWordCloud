#!/usr/bin/env python3

# 作者：赖伟文
# 邮箱：lwwens@gmail.com ; lai_wei_wen@qq.com ;

import re
import os
import codecs
import jieba.analyse
import matplotlib.pyplot as plt
import matplotlib as mpl
from wordcloud import WordCloud
from os import path

# 系统信息
cur_dir = path.dirname(__file__)

def multi_wordcloud():
    # 分类目录、分词目录、词云目录
    classify_dir = './classify'
    fenci_dir = './fenci'
    wc_image_dir = './wcimage'

    # 遍历分类后的数据集
    for root_dir, alldirs, allfiles in os.walk(path.join(cur_dir, classify_dir)):
        for afile in allfiles:
            match = re.search(r'\d{4}-\d{2}-\d{2}', afile)
            # 分类子目录-数据集文件名
            data_filename = root_dir + os.sep + afile
            # 分词子目录-分词文件名
            fenci_filename = fenci_dir + os.sep + match.group(0) + '.txt'
            # 词云子目录-词云图文件名
            wc_image_filename = wc_image_dir + os.sep + match.group(0) + '.jpg'
            
            # 分词、生成词云图
            generate_wordcloud(data_filename, fenci_filename, wc_image_filename)


def generate_wordcloud(data_filename, fenci_filename, wc_image_filename):
    # 字体路径
    wcfont_path = './fonts/SimFang.ttf'
    mplfont_path = './fonts/SimHei.ttf'
    # 停用词路径
    stopword_path = './fenci/stopword.txt'

    with codecs.open(path.join(cur_dir, data_filename), 'r', encoding='UTF-8') as data_file:
        data = []
        # 添加停用词
        jieba.analyse.set_stop_words(path.join(cur_dir, stopword_path))

        # 通过词频获取关键字
        for text in data_file.readlines(100000):
            data.extend(jieba.cut(text, cut_all=False, HMM=True))
        data = ' '.join(data)
        # 将分词后的数据存入相应文件
        with codecs.open(path.join(cur_dir, fenci_filename), 'w', encoding='UTF-8') as fenci_file:
            fenci_file.write(data)

        # 生成词云
        word_cloud = WordCloud(font_path=wcfont_path).generate(data)

        print(wc_image_filename)
        # 词云显示
        #mplfont = mpl.font_manager.FontProperties(fname=mplfont_path)
        #mpl.rcParams['axes.unicode_minus'] = False
        #plt.figure()
        #plt.title('微博文本词云', fontproperties=mplfont, fontsize=30)
        #plt.imshow(word_cloud, interpolation="bilinear")
        #plt.axis('off')
        #plt.show()

        # 保存词云图片
        word_cloud.to_file(wc_image_filename)


if __name__ == '__main__':
    multi_wordcloud()
