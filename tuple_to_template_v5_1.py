#! Python3
# -*- coding: utf-8 -*-
import sys
import re
import Levenshtein

# ------------------
# 2018-1-15 11:43:13
# 修改文件部分 多个三元组对应过个文件
#  tuple_position 作为元组位置参数
# 修改文件保存以及一些多元组逻辑判断
# ------------------
# 2018-1-16 10:05:36
# 接口更改 文件中每行 [list]---report
# 修改open_text 中的逻辑判断
# q取消

# 该版本修改了行 、 列 、data的泛化处理出现的一些bug


def open_text(tuple_sentence):
    f_ts = open(tuple_sentence,"r",encoding="utf-8")
    #打开文本，分行调用模板生成函数
    for line in f_ts.readlines():
        if len(line) < 5:
            continue
        cutTuples = re.compile(r'\|\|\|')  # 切分元组元素
        cut_off = line.find("----")
        tuple_all=line[:cut_off]

        sentence_line=line[cut_off+4:]
        original_sentence =sentence_line.strip()
        list_tuples = cutTuples.split(tuple_all)
        # list_tuples = tuple_all
        # print(list_tuples)
        # print(len(list_tuples))
        # for i in list_tuples:
        #     print(i)
        print("------------------------------------------")
        for index, item in enumerate(list_tuples, 1):
            sentence_line = template_generize(item,sentence_line,index)

        if len(list_tuples) == 1:
            print("1 : " + sentence_line)
            f_one.write(sentence_line+"----"+list_tuples[0]+"----"+original_sentence)
            f_one.write("\n")
        elif len(list_tuples) == 2:
            print("2 : " + sentence_line)
            f_two.write(sentence_line+"----"+list_tuples[0]+"|||"+list_tuples[1]+"----"+original_sentence)
            f_two.write("\n")
        elif len(list_tuples) == 3:
            print("3 : " + sentence_line)
            f_three.write(sentence_line+"----"+list_tuples[0]+"|||"+list_tuples[1]+"|||"+list_tuples[2]+"----"+original_sentence)
            f_three.write("\n")
        elif len(list_tuples) == 4:
            print("4 : " + sentence_line)
            f_four.write(sentence_line+"----"+list_tuples[0]+"|||"+list_tuples[1]+"|||"+list_tuples[2]+list_tuples[3]+"----"+original_sentence)
            f_four.write("\n")
        else:
            print("other : " + sentence_line)
            f_other.write(sentence_line+"----"+list_tuples[0]+"|||"+list_tuples[1]+"|||"+list_tuples[2]+list_tuples[3]+"----"+original_sentence)
            f_other.write("\n")

# 4个用于保存的文件 一元二元三元and others

# || 切元组 生成句子
def template_generize(tuple_line,sentence_line,tuple_position):
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
                sentence_line = handle_tuple_row(phase , sentence_line , phaseCount , tuple_position)
                # print(sentence_line)

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
                sentence_line = handle_tuple_column(phase , sentence_line , phaseCount , tuple_position)
                # print (sentence_line)

        # 处理三元组第三个元素 值
        # 元组第三个元素返回两个值或一个值（初步规律）,标记为&data8!或&data9!
        elif count == 3:
            if tuple_element == "":
                count += 1
                continue
            ele_nums = handle_tuple_element3(tuple_element)
            sentence_line = handle_tuple_data(ele_nums, sentence_line, phaseCount, tuple_position)
            # if len(ele_nums) == 1:
            #     sentence_line = sentence_line.lower().replace(str(ele_nums[0]), "&data;")
            # elif len(ele_nums) == 2:
            #     sentence_line = sentence_line.lower().replace( str(ele_nums[0]), "&data;")
            #     ele_nums2=str(ele_nums[1])+"%"
            #     sentence_line = sentence_line.lower().replace(ele_nums2, "&data_%;")
            # else:
            #     print("more than 2 nums in element 3")
            # 去掉百分号
           # sentence_line = sentence_line.replace("%", "")
        else:
            print ("这不是个三元组")
            break

        count += 1 #控制选择元组元素
    # print ("最终结果")
    # print(sentence_line)
    f_t_ans.write(sentence_line)
    f_t_ans.write("\n")
    return sentence_line

def handle_tuple_element3(ele):
    #初步发现元组第三个元素具有类似 80 (NE,74.2%)的特征，将其分离
    #python3的四舍五入0.5算作0
    ele=ele.strip()
    cut_blank=re.compile(" ")
    cut_comma= re.compile(",")
    decimal_count = re.compile(u'\d+\.\d\d')#判断小数位数大于等于两位的情况
    cut_inside = re.compile("\d+\.\d*")
    results = []#返回两个整形
    count = 0
    for nums in cut_blank.split(ele):
        nums=nums.strip()
        if count==0: #处理括号外
            if(nums.isdecimal() == True):
                results.append(int(round(float(nums))))
            else:
                results.append(nums)

        elif count ==1 : #处理括号里面
            nums=nums.strip()
            nums=nums[1:(len(nums)-1)]  #获得括号中的内容
            insides=cut_comma.split(nums)   #逗号切分
            for i in insides:
                i = i.strip()
                if '%' in i:
                    i=i[:len(i)-1]  #去掉百分号
                    i=str(int(round(float(i))))
                    results.append(i+"%")
                elif i.isalpha()==True:  #纯字母情况
                    results.append(i)
                else:#纯数字情况，判断小数位数
                    r= re.match(decimal_count, str(i))
                    if r:  #若存在，则保留一位小数
                        r = round(float(r.group()), 1)
                    else:
                        r= i
                    results.append(str(r))
        else:
            break
        count += 1
    return results



def handle_tuple_row(key,sentence_line,level,tuple_position):
    sentence_line = sentence_line.replace("(", " ( ").replace(")", " ) ")
    list_a = sentence_line.split()
    list_b = key.split(" ")
    for i in range(len(list_a)):
        for j in range( len(list_b)):
            # print(list_a[i] + "  " + list_b[j] + "  " + str(Levenshtein.distance(list_a[i], list_b[j])) + "  "+  str(Levenshtein.ratio(list_a[i], list_b[j])))

            # 纯数字要完全相等
            if list_a[i].isdigit() and list_b[j].isdigit() :
                if list_a[i] == list_b[j]:
                    list_a[i] = "&row_" + str(tuple_position) + "_" + str(level) +";"

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

                list_a[i] = "&row_" + str(tuple_position) + "_" + str(level) +";"
                # print ("------------------------------------------------")
    sentence_afterrow = ""
    for i in range(len(list_a)):
        if i > 0:
            if list_a[i] == list_a[i-1] == "&row_" + str(tuple_position) + "_" + str(level) +";":
                continue
        sentence_afterrow += list_a[i] 
        sentence_afterrow += ' '
        # 这里会多一个空格出来
    return sentence_afterrow

def handle_tuple_column(key,sentence_line,level,tuple_position):
    # string = re.sub("[\s+\!,$%^*()+\"\']+|[+——！，。？、~@#￥%……&*（）]+", " ", sentence_line)
    # list_a = string.split()
    sentence_line = sentence_line.replace("("," ( ").replace(")"," ) ")
    list_a = sentence_line.split()
    list_b = key.split(" ")
    for i in range(len(list_a)):
        for j in range( len(list_b)):
            # print(list_a[i] + "  " + list_b[j] + "  " + str(Levenshtein.distance(list_a[i], list_b[j])) + "  "+  str(Levenshtein.ratio(list_a[i], list_b[j])))

            # 纯数字要完全相等
            if list_a[i].isdigit() and list_b[j].isdigit() :
                if list_a[i] == list_b[j]:
                    list_a[i] = "&column_" + str(tuple_position) + "_" + str(level) +";"

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

                list_a[i] = "&column_" + str(tuple_position) + "_" + str(level) +";"
                # print ("------------------------------------------------")
    sentence_aftercolumn = ""
    for i in range(len(list_a)):
        if i > 0:
            if list_a[i] == list_a[i-1] == "&column_" + str(tuple_position) + "_" + str(level) +";":
                continue
        sentence_aftercolumn += list_a[i] 
        sentence_aftercolumn += ' '
        # 这里会多一个空格出来
    return sentence_aftercolumn


def handle_tuple_data(keylist,sentence_line,level,tuple_position):
    list_a = sentence_line.split()
    ele_nums = keylist
    for i in range(len(list_a)):
        if '&' in list_a[i]:  #含有& 说明是标记，跳过
            continue
        if hasNumbers(list_a[i]): # 当单词中含有数字时
            for j in range(len(ele_nums)):
                if "%" in list_a[i] and "%" in str(ele_nums[j]):  #当该词是一个百分数时，直接替换
                    list_a[i] = list_a[i].replace(str(ele_nums[j]), "&data_" + str(tuple_position) + "_" + "%" + ";")
                elif "." in list_a[i]:  # 当ele包含.时，暂定认为是一个浮点数，不考虑出现   x10.9x 的情况
                    if list_a[i].strip()[-1] == '.':  #如果 . 出现在最后一个位置，说明是句号，跳出
                        continue
                    try:  #若不是句号，则认为是浮点，替换
                        if float(list_a[i]) == float(ele_nums[j]):
                            list_a[i] =  "&data_" + str(tuple_position) + "_" + "Float" + ";"
                    except:  #若出现无法float错误的则 pass，因为不是纯float
                        pass
                elif list_a[i].isdigit():  #当是纯数字的时候，直接替换
                    list_a[i] =list_a[i].replace( str(ele_nums[j]),"&data_" + str(tuple_position) + "_" + "Int" + ";")
                else:
                    continue
        elif list_a[i].isalpha(): # 没有数字了，应该只能是字母字符串了
            for j in range(len(ele_nums)):
                list_a[i] = list_a[i].replace(str(ele_nums[j]), "&data_" + str(tuple_position) + "_" + "Str" + ";")
        else:
            for j in range(len(ele_nums)):
                list_a[i] = list_a[i].replace(str(ele_nums[j]), "&data_" + str(tuple_position) + "_" + "Other" + ";")

    sentence_afterData = ""
    for i in range(len(list_a)):
        sentence_afterData += list_a[i]
        sentence_afterData += ' '
        # 这里会多一个空格出来
    return sentence_afterData.strip()

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

    # t_s = "tuple-to-sentence_1/efficy-tupletosentence.txt"
    # prefix="templates_1/"
    # fdir_one = prefix+"one_element_template.txt"
    # fdir_two = prefix+"two_element_template.txt"
    # fdir_three = prefix+"three_element_template.txt"
    # fdir_four = prefix+"four_element_template.txt"
    # fdir_other = prefix+"other_element_template.txt"
    # t_ans = "new_form_data_ans.txt"
    # f_one = open(fdir_one,"a",encoding="utf-8")
    # f_two = open(fdir_two,"a",encoding="utf-8")
    # f_three = open(fdir_three,"a",encoding="utf-8")
    # f_four = open(fdir_four,"a",encoding="utf-8")
    # f_other = open(fdir_other,"a",encoding="utf-8")
    # f_t_ans = open(t_ans, "w",encoding='utf-8')
    # open_text(t_s)

    print(handle_tuple_element3("82.14"))

    print("Done")

