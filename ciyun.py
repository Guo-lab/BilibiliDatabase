import jieba
import  wordcloud
import pandas as pd
import csv
with open('/Users/gsq/Desktop/DatabasePractice/Final/csv/danmu.csv','r',encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    column = [row[7] for row in reader]
txt_list = jieba.cut(str(column))  #  处理  分词数据(返回数据类型列表)
string = ' '.join(txt_list)
w = wordcloud.WordCloud(width=1000,
                        height=700,
                        background_color='white',  #  背景颜色
                        font_path='Arial Unicode.ttf',   #  字体
                        scale=15, # 间隔
                        stopwords={' ','?','!',',','的','了'},  # 停用词  剔除不需要显示的字符
                        contour_width=5,                #  整个内容显示的宽度
                        contour_color='red',      #  内容显示的颜色 红色边境
)
w.generate(string)  #  传入处理好的字符窜
photo_path = '/Users/gsq/Desktop/DatabasePractice/Final/ciyun.png'
w.to_file(photo_path)  #  保存
