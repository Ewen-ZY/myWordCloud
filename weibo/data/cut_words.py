#!/usr/bin/env python3

# 作者：赖伟文
# 邮箱：lwwens@gmail.com ; lai_wei_wen@qq.com ;

import codecs
import json
import jieba
import numpy
import os
import re
import time
import matplotlib as mpl
import matplotlib.pyplot as plt
from collections import Counter
from os import path
from PIL import Image
from wordcloud import WordCloud


# 打印时间信息
def print_info(info):
    # 时间格式：2019-01-02 21:07:09
    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    print('[%s] %s' % (now, info))


# 将数据写入文件
def write_data(filepath, text):
    with codecs.open(filepath, 'w', encoding='UTF-8') as afile:
        afile.write(text)


# 加载停用词
def load_stopwords(filepath):
    print_info('Loading stopwords...')
    stopwords = [line.strip() for line in codecs.open(filepath, 'r', encoding='UTF-8').readlines()]
    return stopwords


# 分词
def cut_words(data_filepath, stopwords):
    print_info('Cutting words...')
    outstr = ''

    # 读入要分词的文件
    with codecs.open(data_filepath, 'r', encoding='UTF-8') as data_file:
        text = data_file.read()

        # 分词
        seg_list = jieba.cut(text, cut_all=False)

        # 去除停用词，并用一个空格分隔词
        for word in seg_list:
            if word not in stopwords and word != '\n':
                outstr += word
                outstr += ' '

    return outstr


# 统计词频
def wordcount(cut_words_filepath):
    print_info('Counting words...')
    with codecs.open(cut_words_filepath, 'r', encoding='UTF-8') as cuted_file:
        text = cuted_file.read()
        seg_list = jieba.cut(text, cut_all=False)
        word_dict = dict(Counter(seg_list))
        word_dict.pop(' ')
    return word_dict if word_dict is not None else {}


# 生成词云
def generate_wordcloud(word_dict, wcfont_path, mask_filepath):
    print_info('Generating wordcloud...')

    # 生成mask
    mask = numpy.array(Image.open(mask_filepath, 'r'))
    # mask = plt.imread(mask_filepath)

    # 生成词云
    word_cloud = WordCloud(font_path=wcfont_path, background_color='white', max_font_size=2000,
                           mask=mask, contour_color='steelblue', contour_width=2)
    word_cloud.generate_from_frequencies(word_dict)
    return word_cloud


# 显示词云
def display_wordcloud(word_cloud, mpl_font_path):
    print_info('Displaying wordcloud...')
    mpl_font = mpl.font_manager.FontProperties(fname=mpl_font_path)

    # 显示Unicode符号
    mpl.rcParams['axes.unicode_minus'] = False

    # 显示词云
    # plt.title('微博文本词云', fontproperties=mpl_font, fontsize=30)
    plt.imshow(word_cloud, interpolation="bilinear")
    # 是否显示x、y轴
    plt.axis('off')
    plt.figure()
    plt.show()


# 分词、词云
def cut_word_and_wordcloud(data_filepath, cut_words_filepath, word_dict_filepath, wc_image_filepath, mask_filepath):
    # 字体路径
    mpl_font_path = './fonts/SimHei.ttf'
    wcfont_path = './fonts/SimFang.ttf'
    # 停用词路径
    stopwords_filepath = './stopword.txt'

    # 加载停用词
    stopwords = load_stopwords(stopwords_filepath)
    # 分词
    text = cut_words(data_filepath, stopwords)
    # 去除标点符号
    write_data(cut_words_filepath, text)
    # 统计词频
    word_dict = wordcount(cut_words_filepath)
    # 将词频写入文件
    write_data(word_dict_filepath, json.dumps(word_dict, ensure_ascii=False))
    # 生成词云
    word_cloud = generate_wordcloud(word_dict, wcfont_path, mask_filepath)
    # 保存词云
    word_cloud.to_file(wc_image_filepath)
    # 显示词云
    display_wordcloud(word_cloud, mpl_font_path)


# 多文件生成词云
def multi_wordcloud():
    # 分类目录、分词目录、词云目录
    classify_dir = './classify'
    cut_words_dir = './cut_words'
    wc_image_dir = './wcimage'
    mask_filepath = './alice_mask.png'
    
    # 遍历分类后的数据集
    for root_dir, alldirs, allfiles in os.walk(classify_dir):
        for afile in allfiles:
            print_info('处理' + afile + '中...')
            match = re.search(r'\d{4}-\d{2}-\d{2}', afile)
            # 分类子目录-数据集文件名
            data_filepath = root_dir + os.sep + afile
            # 分词子目录-分词文件名
            cut_words_filepath = cut_words_dir + os.sep + match.group(0) + '.txt'
            # 词频
            word_dict_filepath = cut_words_dir + os.sep + match.group(0) + '.json'
            # 词云子目录-词云图文件名
            wc_image_filepath = wc_image_dir + os.sep + match.group(0) + '.jpg'

            # 分词、生成词云图
            cut_word_and_wordcloud(data_filepath, cut_words_filepath, word_dict_filepath, wc_image_filepath, mask_filepath)


# 主程序
if __name__ == '__main__':
    print_info('Main process...')
    multi_wordcloud()

