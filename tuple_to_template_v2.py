#! Python3
# -*- coding: utf-8 -*-
import sys
import re
import Levenshtein


f_out=open("template_out.txt","w")
def run(tuple_sentence):
    f_ts = open(tuple_sentence)
    #打开文本，分行调用模板生成函数
    for line in f_ts.readlines():
        cut_off = line.find("----")
        tuple_line=line[:cut_off]
        sentence_line=line[cut_off+4:]
        tuple_line=tuple_line.strip()
        sentence_line=sentence_line.strip()
        template_generize(tuple_line,sentence_line)
        f_out.write("----" + tuple_line + "----" + sentence_line + "\n")
    f_out.close()  # new add
    f_ts.close()  # new add
    print("finish")


def template_generize(tuple_line,sentence_line):
    cutTuple = re.compile(r'\|\|')#切分元组元素
    cutBlank = re.compile(r' ')  # 用空格切六元组
    count = 1
    for tuple_element in cutTuple.split(tuple_line):
        tuple_element = tuple_element.strip()
        #处理三元组第一个元素 行
        if count == 1:  # 三元组列1 list
            if tuple_element == "":
                count += 1
                continue
            phaseCount=0
            for phase in cutEleIntoList(tuple_element):#形式为 abc|def|a
                
                # sentence_line = sentence_line.lower().replace(phase.lower(), "&data"+str(phaseCount)+"!")
                phaseCount+=1 
                sentence_line = handle_tuple_row(phase , sentence_line , phaseCount)
                #print(sentence_line)

        # 处理三元组第二个元素 列
        elif count == 2:
            if tuple_element == "":
                count += 1
                continue
            phaseCount = 0  #限定列值标记从4开始，即从&data4!到&data7!
            for phase in cutEleIntoList(tuple_element):  # 形式为 ab c|def|a
                # print(phase)
                # sentence_line = sentence_line.lower().replace(phase.lower(), "&data"+str(phaseCount)+"!")
                phaseCount += 1
                sentence_line = handle_tuple_column(phase , sentence_line ,phaseCount)
                #print (sentence_line)

        # 处理三元组第三个元素 值
        # 元组第三个元素返回两个值或一个值（初步规律）,标记为&data8!或&data9!
        elif count == 3:
            if tuple_element == "":
                count += 1
                continue
            ele_nums = handle_tuple_element3(tuple_element)
            if len(ele_nums) == 1:
                sentence_line = sentence_line.lower().replace(str(ele_nums[0]), "&data;")
            elif len(ele_nums) == 2:
                sentence_line = sentence_line.lower().replace( str(ele_nums[0]), "&data;")
                ele_nums2=str(ele_nums[1])+"%" 
                sentence_line = sentence_line.lower().replace(ele_nums2, "&data_%;")
            else:
                print("more than 2 nums in element 3")
            # 去掉百分号
           # sentence_line = sentence_line.replace("%", "")
        else:
            print ("这不是个三元组")
            break
        count += 1 #控制选择元组元素

    #print ("最终结果")
    f_out.write(sentence_line)

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

def handle_tuple_row(key,sentence_line,level):
    list_a = sentence_line.split()#原句切分成词
    list_b = key.split(" ")#关键词
    for i in range(len(list_a)):
        for j in range( len(list_b)):
            # print(list_a[i] + "  " + list_b[j] + "  " + str(Levenshtein.distance(list_a[i], list_b[j])) + "  "+  str(Levenshtein.ratio(list_a[i], list_b[j])))

            # 纯数字要完全相等
            if list_a[i].isdigit() and list_b[j].isdigit() :
                if list_a[i] == list_b[j]:
                    list_a[i] = "&row_" + str(level) +";"

            # 编辑距离小于4 && ratio大于0.5 && 全部都不是数字 && 大于等于两个单位 &&       
            elif Levenshtein.distance(list_a[i], list_b[j]) < 4 and Levenshtein.ratio(list_a[i], list_b[j]) >= 0.5 and len(list_a[i]) > 1 and len(list_b[j]) > 1 and list_a[i].isdigit() == False and list_b[j].isdigit() == False:
                # 如果含有数字的话 如果有一个不含->不替换 如果不一样->不替换 
                if hasNumbers(list_a[i]) or hasNumbers(list_b[j]):
                    num_of_a = re.findall(r'\d+', list_a[i])
                    num_of_b = re.findall(r'\d+', list_b[j])
                    if len(num_of_a) == 0 or len(num_of_b) ==0:
                        continue
                    if num_of_a[0] != num_of_b[0]:
                        continue

                list_a[i] = "&row_" + str(level) +";"
                # print ("------------------------------------------------")
    sentence_afterrow = ""
    for i in range(len(list_a)):
        if i > 0:
            if list_a[i] == list_a[i-1] == "&row_" + str(level) +";":
                continue
        sentence_afterrow += list_a[i] 
        sentence_afterrow += ' '
    return sentence_afterrow.strip()

def handle_tuple_column(key,sentence_line,level):
    list_a = sentence_line.split()
    list_b = key.split(" ")
    for i in range(len(list_a)):
        for j in range( len(list_b)):
            # print(list_a[i] + "  " + list_b[j] + "  " + str(Levenshtein.distance(list_a[i], list_b[j])) + "  "+  str(Levenshtein.ratio(list_a[i], list_b[j])))

            # 纯数字要完全相等
            if list_a[i].isdigit() and list_b[j].isdigit() :
                if list_a[i] == list_b[j]:
                    list_a[i] = "&column_" + str(level) +";"

            # 编辑距离小于4 && ratio大于0.5 && 全部都不是数字 && 大于等于两个单位 &&       
            elif Levenshtein.distance(list_a[i], list_b[j]) < 4 and Levenshtein.ratio(list_a[i], list_b[j]) >= 0.5 and len(list_a[i]) > 1 and len(list_b[j]) > 1 and list_a[i].isdigit() == False and list_b[j].isdigit() == False:
                i # 如果含有数字的话 如果有一个不含->不替换 如果不一样->不替换 
                if hasNumbers(list_a[i]) or hasNumbers(list_b[j]):
                    num_of_a = re.findall(r'\d+', list_a[i])
                    num_of_b = re.findall(r'\d+', list_b[j])
                    if len(num_of_a) == 0 or len(num_of_b) ==0:
                        continue
                    if num_of_a[0] != num_of_b[0]:
                        continue

                list_a[i] = "&column_" + str(level) +";"
                # print ("------------------------------------------------")
    sentence_aftercolumn = ""
    for i in range(len(list_a)):
        if i > 0:
            if list_a[i] == list_a[i-1] == "&column_" + str(level) +";":
                continue
        sentence_aftercolumn += list_a[i] 
        sentence_aftercolumn += ' '
    return sentence_aftercolumn.strip()

# 判断是否包含数字
def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

def cutEleIntoList(ele):
    ele=ele.strip()
    cut_Ele=re.compile(r'\|')
    list=[]
    for t in cut_Ele.split(ele):
        t=t.strip()
        list.append(t)
    return list

if __name__ == "__main__":
    t_s = "new_form_data.txt"
    run(t_s)

