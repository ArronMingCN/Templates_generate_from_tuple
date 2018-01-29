#! Python3
# -*- coding: utf-8 -*-
import sys
import re




# 针对表格值比较做的数值处理，初步确定表有一定的格式要求：* (*)
# 其中每个*中的值一定要用逗号分开，对于更多其他符号没有处理。
# 由两表合并比较值得需求，需要将百分数的值保留一位
# 2018/1/26
def handle_tuple_element3(ele):
    #python3的四舍五入0.5算作0
    ele=ele.strip()
    cut_blank=re.compile(" ")
    cut_comma= re.compile(",")
    cut_parentheses = re.compile(r'\(') # 通过左圆括号切分外面的值
    decimal_count = re.compile(u'\d+\.\d\d+')#判断小数位数大于等于两位的情况
    cut_inside = re.compile("\d+\.\d*")
    results = [] # return a list
    count = 0
    for nums in cut_parentheses.split(ele):
        nums=nums.strip()
        if count==0: #处理括号外
            if nums == "":
                count += 1
                continue
            for i in cut_comma.split(nums): #用逗号切分括号外的
                i = i.strip()
                if i == "":
                    continue
                if '%' in i: #当括号外出现百分数时，目前数值四舍五入为整数
                    i = i[:len(i) - 1]
                    i = str(round(float(i),1))
                    results.append(i + "%")
                elif( is_float(i) == True): #若是小数则进行四舍五入
                    results.append(int(round(float(i))))
                else:
                    results.append(i)
        elif count ==1 : #处理括号里面
            nums=nums.strip()
            nums=nums[0:(len(nums)-1)]  #获得括号中的内容
            if nums == "":
                count += 1
                continue
            insides=cut_comma.split(nums)   #逗号切分
            for i in insides:
                i = i.strip()
                if '%' in i:
                    i=i[:len(i)-1]  #去掉百分号
                    i=str(round(float(i),1))  #百分数目前确定数值部分为整数
                    results.append(i+"%")
                elif i.isalpha()==True:  #纯字母情况
                    results.append(i)
                else:#浮点数情况，判断小数位数
                    #注意，这是针对括号里的，前面括号外的皆保留整数，或字符串本身
                    r= re.match(decimal_count, str(i))
                    if r:  #若存在大于等于两位小数的，则保留一位小数
                        r = round(float(r.group()), 1)
                    else:
                        r= i #否则不四舍五入
                    results.append(str(r))
        else:
            break
        count += 1
    return results
def is_float(s):
        '''
        这个函数是用来判断传入的是否为小数,包括正小数和负小数三
        :param s :传入一个字符串
        :return: True or False
        '''
        s = str(s)
        if s.isdigit():
            return False
        else:
            if s.count('.') == 1:  # 判断小数点个数
                sl = s.split('.')  # 分割字符串
                left = sl[0]  # 小数点前面的
                right = sl[1]  # 小数点后面的
                if left.startswith('-') and left.count('-') == 1 and right.isdigit():
                    lleft = left.split('-')[1]  ##按照负号分割然后取负号后面的数
                    if lleft.isdigit():
                        return True  # 负小数
                    else:
                        return False
                elif left.isdigit() and right.isdigit():
                    return True  # 正小数

                else:
                    return False
            else:
                return False

# 当场跑程序一定要注意输入文件的格式问题，特别对于China和Overall的行值分级必须是一致的
# 比如本次处理中，因为原始表格问题，其中一表丢失了在另一表存在的第一级行值，导致无法输出正确。
def run():
    f1 = open("table_source_china.txt","r",encoding="utf-8")
    f2 = open("table_source_overall.txt","r",encoding="utf-8")
    dict_china = {}
    dict_overall = {}
    dict_china_data_used = {}
    dict_overall_data_used = {}
    cut_tuple = re.compile("\|\|")
    for tuple in f1.readlines():
        tuple = tuple.strip()
        data = ""
        value = 0
        count = 0
        for ele in cut_tuple.split(tuple):
            if count == 0:
                if ele == "":
                    count += 1
                    continue
                key = ele
            elif count == 1:
                if ele == "":
                    count += 1
                    continue
                #key = key + "||" + ele[:]
            elif count == 2:
                if ele == "":
                    data = ""
                    value = "0%"
                else:
                    data = ele
                    value = handle_tuple_element3(ele)
                    # 当前需求显示，第二个值是作为比较的，是百分数，带百分号，但需要去掉百分号做减法
                    if len(value) <2 :
                        value = str(value[0])[:-1]
                    else:
                        value = str(value[1])[:-1]
            else:
                print("not the standard 3_ele_tuple!")
                break
            count += 1
        dict_china[key] = data
        dict_china_data_used[key] =value
    for i in dict_china:
        print(dict_china[i])
    for j in dict_china_data_used:
        print(dict_china_data_used[j])
    for tuple in f2.readlines():
        tuple = tuple.strip()
        data = ""
        value = 0
        count = 0
        for ele in cut_tuple.split(tuple):
            if count == 0:
                if ele == "":
                    count += 1
                    continue
                key = ele
            elif count == 1:
                if ele == "":
                    count += 1
                    continue
                key = key + "||" + ele
            elif count == 2:
                if ele == "":
                    data = ""
                    value = "0%"
                else:
                    data = ele
                    value = handle_tuple_element3(ele)
                    # 当前需求显示，第二个值是作为比较的，是百分数，带百分号，但需要去掉百分号做减法
                    if len(value) < 2:
                        value = str(value[0])[:-1]
                    else:
                        value = str(value[1])[:-1]
            else:
                print("not the standard 3_ele_tuple!")
                break
            count += 1
        dict_overall[key] = data
        dict_overall_data_used[key] = value
    for i in dict_overall:
        print(dict_overall[i])
    for j in dict_overall_data_used:
        print(dict_overall_data_used[j])
    #输出单表信息，输出为一个文件或字符串，
    for key in dict_overall.keys():
        print(key+dict_overall[key])

    for key in dict_china.keys():
        print(dict_china[key])

    #输出合并的信息
    if len(dict_overall) >= len(dict_china):
        for key in dict_overall:
            print(dict_overall)



fout_emerged=open("table_emerged.txt","w",encoding="utf-8")
fout_table_china = open("table_china.txt","w",encoding="utf-8")
fout_table_overall = open("table_china.txt","w",encoding="utf-8")

if __name__ == "__main__":
    #print(handle_tuple_element3(""))
    run()