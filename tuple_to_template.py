#! Python3
# -*- coding: utf-8 -*-
import sys
import re

#more problems:模板原文大小写问题、原句加个strip()、

f_out=open("template_out.txt","w")
def run(tuple_sentence,f_out):
    f_ts = open(tuple_sentence)
    #打开文本，分行调用模板生成函数
    for line in f_ts.readlines():
        cut_off = line.find("----")
        tuple_line=line[:cut_off]
        sentence_line=line[cut_off+4:]

        tuple_line=tuple_line.strip()#new add
        sentence_line=sentence_line.strip()

        template_generize(tuple_line,sentence_line)

        f_out.write("----" + tuple_line + "----" + sentence_line + "\n")#new add

    f_out.close()#new add
    f_ts.close()#new add
    print("finish")


def template_generize(tuple_line,sentence_line):
    cutTuple = re.compile(r'\|\|')#切分元组元素
    cutBlank = re.compile(r' ')  # 用空格切六元组
    count = 1
    for tuple_element in cutTuple.split(tuple_line):
        tuple_element = tuple_element.strip()
        #处理三元组第一个元素
        if count == 1:  # 三元组列1 list
            if tuple_element == "":
                count += 1
                continue
            phaseCount=0
            for phase in cutEleIntoList(tuple_element):#形式为 abc|def|a
                sentence_line = sentence_line.lower().replace(phase.lower(), "&data"+str(phaseCount)+"!")
                phaseCount+=1 #行名标记从&data0!到&data3!

        # 处理三元组第二个元素
        elif count == 2:
            if tuple_element == "":
                count += 1
                continue
            phaseCount = 4  #限定列值标记从4开始，即从&data4!到&data7!
            for phase in cutEleIntoList(tuple_element):  # 形式为 abc|def|a
                sentence_line = sentence_line.lower().replace(phase.lower(), "&data"+str(phaseCount)+"!")
                phaseCount += 1

        # 处理三元组第三个元素
        # 元组第三个元素返回两个值或一个值（初步规律）,标记为&data8!或&data9!
        elif count == 3:
            if tuple_element == "":
                count += 1
                continue
            ele_nums = handle_tuple_element3(tuple_element)
            if len(ele_nums) == 1:
                sentence_line = sentence_line.lower().replace(str(ele_nums[0]), "&data8!")
            elif len(ele_nums) == 2:
                sentence_line = sentence_line.lower().replace( str(ele_nums[0]), "&data8!")
                ele_nums2=str(ele_nums[1])+"%"
                sentence_line = sentence_line.lower().replace(ele_nums2, "&data9!")
            else:
                print("more than 2 nums in element 3")
            # 去掉百分号
           # sentence_line = sentence_line.replace("%", "")
        else:
            break

        count += 1 #控制选择元组元素
    f_out.write(sentence_line)#new add

def handle_tuple_element3(str):
    #初步发现元组第六个元素具有类似 80 (74.2%)的特征，将其分离
    #python3的四舍五入0.5算作0
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
    t_s = "table_content_v1.txt"

    run(t_s,f_out)
    #print(handle_tuple_element3("80"))

