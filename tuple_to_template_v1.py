#! Python3
# -*- coding: utf-8 -*-
import sys
import re
class arithmetic():

    def __init__(self):
        pass

    ''''' 【编辑距离算法】 【levenshtein distance】 【字符串相似度算法】 '''

    def levenshtein(self, first, second):
        if len(first) > len(second):
            first, second = second, first
        if len(first) == 0:
            return len(second)
        if len(second) == 0:
            return len(first)
        first_length = len(first) + 1
        second_length = len(second) + 1
        distance_matrix = [range(second_length) for x in range(first_length)]
        # print distance_matrix
        for i in range(1, first_length):
            for j in range(1, second_length):
                deletion = distance_matrix[i - 1][j] + 1
                insertion = distance_matrix[i][j - 1] + 1
                substitution = distance_matrix[i - 1][j - 1]
                if first[i - 1] != second[j - 1]:
                    substitution += 1
                distance_matrix[i][j] = min(insertion, deletion, substitution)
                # print distance_matrix
        return distance_matrix[first_length - 1][second_length - 1]


def open_text(tuple_sentence):
    f_ts = open(tuple_sentence)
    cutTuple=re.compile(r';')
    cutBlank=re.compile(r' ')#用空格切六元组
    for line in f_ts.readlines():

        cut_off = line.find("----")
        tuple_line=line[:cut_off]
        sentence_line=line[cut_off+4:]
        count=1
        for tuple_element in cutTuple.split(tuple_line):
            tuple_element=tuple_element.strip()
            if count == 1:#六元组标题
                if tuple_element ==  "":
                    count += 1
                    continue
                sentence_line=sentence_line.lower().replace(tuple_element.lower(),"&data1!")
            elif count == 2:
                if tuple_element == "":
                    count += 1
                    continue
                sentence_line = sentence_line.lower().replace(tuple_element.lower(), "&data2!")
            elif count == 3:
                if tuple_element == "":
                    count += 1
                    continue
                #for word in cutBlank.split(tuple_element):
                sentence_line = sentence_line.lower().replace(tuple_element.lower(), "&data3!")
            elif count == 4:
                if tuple_element == "":
                    count += 1
                    continue
                sentence_line = sentence_line.lower().replace(tuple_element.lower(), "&data4!")
            elif count ==5:
                if tuple_element == "":
                    count += 1
                    continue
                sentence_line = sentence_line.lower().replace(tuple_element.lower(), "&data5!")
            elif count ==6:
                if tuple_element == "":
                    count += 1
                    continue
                two_nums=handle_tuple_element6(tuple_element)#返回两个值（初步规律）
                for nums in two_nums:
                    if nums:
                        nums=str(nums)
                        sentence_line = sentence_line.lower().replace(nums, "&data6!")
                #去掉百分号
                sentence_line=sentence_line.replace("%","")

            else:
                break
            count += 1
        print(sentence_line)

def template_generize(tuple_line,sentence_line):
    cutTuple = re.compile(r'\|\|')#切分元组元素
    cutBlank = re.compile(r' ')  # 用空格切六元组

def handle_tuple_element6(str):
    #初步发现元组第六个元素具有类似 80 (74.2%)的特征，将其分离
    str=str.strip()
    cut_blank=re.compile(" ")
    cut_inside = re.compile("\d+\.\d*")
    results = []#返回两个整形
    count = 0
    for nums in cut_blank.split(str):
        nums=nums.strip()
        if count==0:
            results.append(int(round(float(nums))))

        elif count ==1 :
            a=re.search(u'\d+\.\d*',nums)
            if a:
                a=a.group()
                results.append(int(round(float(a))))
        else:
            break
        count += 1
    return results



def cutEleIntoList(ele):
    ele=ele.strip()
    cut_Ele=re.compile(r'\|')
    list=[]
    for t in cut_Ele.split(ele):
        t=t.strip()
        list.append(t)
    return list


if __name__ == "__main__":
    arith = arithmetic()
    t_s = "table_content.txt"
    print(cutEleIntoList("helo||abc"))
    #open_text(t_s)
    #print handle_tuple_element6("80 (77.4%)")

