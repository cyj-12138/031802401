# -*- coding: utf-8 -*-
# 分词包
import jieba
import jieba.analyse
from sklearn.metrics.pairwise import cosine_similarity
import sys


class CosineSimilarity(object):
    def __init__(self, file1, file2):
        self.s1 = file1
        self.s2 = file2

    @staticmethod
    def get_keyword(content):  # 提取关键词
        seg = [i for i in jieba.cut(content, cut_all=True) if i != '']  # 分词
        keywords = jieba.analyse.extract_tags("|".join(seg), topK=1000, withWeight=False)
        return keywords

    @staticmethod
    def one_hot(keyword_dict, keywords):
        cut_code = [0] * len(keyword_dict)
        for word in keywords:
            cut_code[keyword_dict[word]] += 1
        return cut_code

    def calculate(self):
        keywords1 = self.get_keyword(self.s1)
        keywords2 = self.get_keyword(self.s2)
        union = set(keywords1).union(set(keywords2))
        keyword_dict = {}
        i = 0
        for word in union:
            keyword_dict[word] = i
            i += 1

        vector1 = self.one_hot(keyword_dict, keywords1)
        vector2 = self.one_hot(keyword_dict, keywords2)
        sample = [vector1, vector2]
        try:
            simRate = cosine_similarity(sample)
            return simRate[1][0]
        except Exception as e:
            print(e)
            return 0.0


# 测试
if __name__ == '__main__':
    root_Path = sys.argv[1]
    copy_Path = sys.argv[2]
    ans_Path = sys.argv[3]
    try:
        with open(root_Path, encoding='UTF-8') as fp:
            root = fp.read()
            seg = [i for i in jieba.cut(root, cut_all=True) if i != '']
        K = int(len(seg) / 8)
    except:
        K = 0
    try:
        with open(root_Path, encoding='UTF-8') as fp:
            ori = fp.read()
        with open(copy_Path, encoding='UTF-8') as fp:
            copy = fp.read()
    except Exception as e:
        print(e)
    model = CosineSimilarity(ori, copy)
    similarity = round(model.calculate(), 2)
    try:
        with open(ans_Path, "w+", encoding='UTF-8') as fp:
            fp.write(str(similarity))
    except Exception as e:
        print(e)
