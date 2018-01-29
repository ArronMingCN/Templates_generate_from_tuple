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
    ele=str(ele).strip()
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
def emerged_table_out(long_table,short_table,whereIsChina):
    # 这里是为了控制输出固定为先中国，后全球，有一个前后对比关系。
    global table_emerged_contents, table_emerged_compare_contents
    if whereIsChina == 1:
        for key in long_table.keys():
            if key in short_table.keys():
                value_1_china = ""
                value_2_china = ""
                value_1_overall = ""
                value_2_overall = ""
                son_key=""
                for son_key in long_table[key].keys():
                    if 'Drug A' in son_key:
                        value_1_china = long_table[key][son_key]
                for son_key in short_table[key].keys():
                    if 'Drug A' in son_key:
                        value_1_overall = short_table[key][son_key]
                for son_key in long_table[key].keys():
                    if 'Placebo' in son_key:
                        value_2_china= long_table[key][son_key]
                for son_key in short_table[key].keys():
                    if 'Placebo' in son_key:
                        value_2_overall = short_table[key][son_key]
                if value_1_china == "":
                    value_1_china = "nothing"
                if value_1_overall == "":
                    value_1_overall = "nothing"
                if value_2_china == "":
                    value_2_china = "nothing"
                if value_2_overall == "":
                    value_2_overall = "nothing"

                row_value=get_last_row_ele(key)
                sub_1 = handle_ele3_sub(value_1_china,value_1_overall)
                sub_2 = handle_ele3_sub(value_2_china,value_2_overall)
                #fout_emerged.write(row_value+"||"+value_1_china+"||"+value_1_overall+"||"+str(sub_1)+"||"+value_2_china+"||"+value_2_overall+"||"+str(sub_2)+"|||")
                table_emerged_contents += (row_value+"||"+value_1_china+"||"+value_1_overall+"||"+value_2_china+"||"+value_2_overall+"|||")
                table_emerged_compare_contents += (row_value+"||"+value_1_china+"||"+value_1_overall+"||"+str(sub_1)+"||"+value_2_china+"||"+value_2_overall+"||"+str(sub_2)+"|||")
            else: # 当较短的表没有该key时，则只输出长表的值，其余为nothing
                value_1_china = ""
                value_2_china = ""
                son_key=""
                for son_key in long_table[key].keys():
                    if 'Drug A' in son_key:
                        value_1_china = long_table[key][son_key]
                for son_key in long_table[key].keys():
                    if 'Placebo' in son_key:
                        value_2_china= long_table[key][son_key]
                if value_1_china == "":
                    value_1_china = "nothing"
                if value_2_china == "":
                    value_2_china = "nothing"

                row_value = get_last_row_ele(key)
                #当该项在短表中没有时，先不做减法
                #fout_emerged.write(row_value + "||" + value_1_china + "||nothing" + "||nothing||" + value_2_china + "||nothing||nothing" +"|||")
                table_emerged_contents += (row_value + "||" + value_1_china + "||nothing||"  + value_2_china + "||nothing" +"|||")
                table_emerged_compare_contents += (row_value + "||" + value_1_china + "||nothing" + "||nothing||" + value_2_china + "||nothing||nothing" +"|||")
        #去掉多的分隔符
        table_emerged_contents = table_emerged_contents[:-3]
        table_emerged_compare_contents = table_emerged_compare_contents[:-3]
    elif whereIsChina == 2:
        for key in long_table.keys():
            if key in short_table.keys():
                value_1_china = ""
                value_2_china = ""
                value_1_overall = ""
                value_2_overall = ""
                son_key = ""
                for son_key in long_table[key].keys():
                    if 'Drug A' in son_key:
                        value_1_overall = long_table[key][son_key]
                for son_key in short_table[key].keys():
                    if 'Drug A' in son_key:
                        value_1_china = short_table[key][son_key]
                for son_key in long_table[key].keys():
                    if 'Placebo' in son_key:
                        value_2_overall = long_table[key][son_key]
                for son_key in short_table[key].keys():
                    if 'Placebo' in son_key:
                        value_2_china = short_table[key][son_key]
                if value_1_china == "":
                    value_1_china = "nothing"
                if value_1_overall == "":
                    value_1_overall = "nothing"
                if value_2_china == "":
                    value_2_china = "nothing"
                if value_2_overall == "":
                    value_2_overall = "nothing"

                sub_1 = handle_ele3_sub(value_1_china, value_1_overall)
                sub_2 = handle_ele3_sub(value_2_china, value_2_overall)
                row_value = get_last_row_ele(key)
                # fout_emerged.write(row_value + "||" + value_1_china + "||" + value_1_overall + "||" + str(sub_1) + "||" + value_2_china + "||" + value_2_overall + "||" + str(sub_2)+"|||")
                table_emerged_contents +=(row_value + "||" + value_1_china + "||" + value_1_overall + "||" + value_2_china + "||" + value_2_overall +"|||")
                table_emerged_compare_contents += (row_value + "||" + value_1_china + "||" + value_1_overall + "||" + str(sub_1) + "||" + value_2_china + "||" + value_2_overall + "||" + str(sub_2)+"|||")

            else: # 当较短的表没有该key时，则只输出长表的值，其余为nothing
                value_1_overall = ""
                value_2_overall = ""
                son_key = ""
                for son_key in long_table[key].keys():
                    if 'Drug A' in son_key:
                        value_1_overall = long_table[key][son_key]
                for son_key in long_table[key].keys():
                    if 'Placebo' in son_key:
                        value_2_overall = long_table[key][son_key]
                if value_1_overall == "":
                    value_1_overall = "nothing"
                if value_2_overall == "":
                    value_2_overall = "nothing"
                # 当该项在短表中没有时，先不做减法
                row_value = get_last_row_ele(key)
                #fout_emerged.write(row_value + "||nothing||" + value_1_overall + "||nothing||nothing||" + value_2_overall+"||nothing"+"|||")
                table_emerged_contents += (row_value + "||nothing||" + value_1_overall + "||nothing||" + value_2_overall+"|||")
                table_emerged_compare_contents += (row_value + "||nothing||" + value_1_overall + "||nothing||nothing||" + value_2_overall+"||nothing"+"|||")

        #去掉多余分隔符
        table_emerged_compare_contents = table_emerged_compare_contents[:-3]
        table_emerged_contents = table_emerged_contents[:-3]
    else:
        print("there won't be another option here")

# 获取第三个元素data的需要相减的值，做减法，返回结果，当前需求为第二个百分数做减法， 得到浮点数，不要百分号
# 有一个待解决的问题，若是真是百分比相同，我这里也会返回0,后面会处理为nothing，不显示东西。

def handle_ele3_sub(ele1,ele2):
    if ele1 == "nothing":
        return "nothing"
    if ele2 == "nothing":
        return "nothing"
    nums1 = handle_tuple_element3(ele1)
    nums2 = handle_tuple_element3(ele2)
    if len(nums1)<2:
        num1 = 0
    else:
        if is_float(str(nums1[1]).strip()[:-1]):
            num1 = float(str(nums1[1]).strip()[:-1])
        else:
            num1 = 0
    if len(nums2) < 2:
        num2 = 0
    else:
        if is_float(str(nums2[1]).strip()[:-1]):
            num2 = float(str(nums2[1]).strip()[:-1])
        else:
            num2 = 0

    return round(num1 - num2,1)

#处理多级问题，只返回最后一级，同时加上对应缩进,只处理到有4级的情况
def get_last_row_ele(row):
    cut_ele=re.compile(r'\|')
    lst = cut_ele.split(row)
    length = len(lst)
    if length == 0:
        return "nothing"
    elif length == 1:
        return lst[0]
    elif length == 2:
        return "    "+lst[-1]
    elif length == 3:
        return "        "+lst[-1]
    else:
        return "            "+lst[-1]

# 以词典形式返回，key是'val_1' 和 'val_2'，对应两个列drug a和placebo得到的差值，  value是相应的值
def get_two_value(tuple):
    cut_ele=re.compile(r'\|\|')
    lst = cut_ele.split(tuple)
    val_1 = 0
    val_2 = 0
    if len(lst)==7:
        val_1 = lst[3]
        val_2 = lst[6]
    dict={'val_1':val_1,'val_2':val_2}
    return dict
#通过threshold输出符合范围值的项
def out_by_range(dicts,threshold):
    global graph_data
    lst = []
    for key in dicts.keys():
        if float(dicts[key]['val_1']) <= threshold and float(dicts[key]['val_2']) <= threshold:
            lst.append(key)

    # 输出横坐标项
    for i in range(len(lst)-1):
        graph_data += (lst[i]+"||")
    graph_data +=(lst[-1]+"|||")
    l1 = [dicts[x]['val_1'] for x in lst]
    l2 = [dicts[x]['val_2'] for x in lst]
    temp1 = "||".join(l1)
    temp2 = "||".join(l2)
    graph_data += (temp1 +"|||"+temp2)
    # 输出纵坐标值，顺序对应前面的横坐标数据，每个横坐标对应两个值，用|隔开，每两个值用||隔开
    # for i in range(len(lst)-1):
    #     graph_data += (str(dicts[lst[i]]['val_1'])+"|"+str(dicts[lst[i]]['val_2'])+"||")
    # graph_data += (str(dicts[lst[-1]]['val_1']) + "|" + str(dicts[lst[-1]]['val_2']))

# 当场跑程序一定要注意输入文件的格式问题，特别对于China和Overall的行值分级必须是一致的
# 比如本次处理中，因为原始表格问题，其中一表丢失了在另一表存在的第一级行值，导致无法输出正确。
def run_table():
    global table_contents
    f1 = open("table_source_china.txt","r",encoding="utf-8")
    f2 = open("table_source_overall.txt","r",encoding="utf-8")
    dict_china = {}
    dict_overall = {}
    cut_tuple = re.compile("\|\|")
    for tuple in f1.readlines():
        tuple = tuple.strip()
        count = 0
        key = ""
        value_dict = {}
        temp_value_key = ""
        for ele in cut_tuple.split(tuple):
            if count == 0:
                if ele == "":
                    count += 1
                    continue
                key = ele
                if key in dict_china.keys():
                    pass
                else:
                    dict_china[key]={}
            elif count == 1:
                if ele == "":
                    count += 1
                    continue
                temp_value_key = ele
                value_dict[temp_value_key]=""
            elif count == 2:
                if ele == "":
                    pass
                else:
                    value_dict[temp_value_key]=ele
            else:
                print("not the standard 3_ele_tuple!")
                break
            count += 1
        dict_china[key].update(value_dict)
    for tuple in f2.readlines():
        tuple = tuple.strip()
        count = 0
        key = ""
        value_dict = {}
        temp_value_key = ""
        for ele in cut_tuple.split(tuple):
            if count == 0:
                if ele == "":
                    count += 1
                    continue
                key = ele
                if key in dict_overall.keys():
                    pass
                else:
                    dict_overall[key] = {}
            elif count == 1:
                if ele == "":
                    count += 1
                    continue
                temp_value_key = ele
                value_dict[temp_value_key] = ""
            elif count == 2:
                if ele == "":
                    pass
                else:
                    value_dict[temp_value_key] = ele
            else:
                print("not the standard 3_ele_tuple!")
                break
            count += 1
        dict_overall[key].update(value_dict)
    # # 按'Drug A'、'PlaceBo'的顺序单独打印输出两个表的内容
    #print("table_china")
    for key in dict_china.keys():
        value1 = ""
        value2 = ""
        # 只要列值（比如Dtug A这种）不存在，即使三元组有第三个数据也舍弃
        for son_key in dict_china[key].keys():
            if 'Drug A' in son_key:
                value1 = dict_china[key][son_key]
        for son_key in dict_china[key].keys():
            if 'Placebo' in son_key:
                value2 = dict_china[key][son_key]
        if value1 == "":
            value1 = "nothing"
        if value2 == "":
            value2 = "nothing"
        row_value = get_last_row_ele(key)
        table_contents += (row_value + "||" + value1 + "||" + value2 + "|||")
    table_contents = table_contents[:-3]
    table_contents += "||||"
    #print("table_overall")
    for key in dict_overall.keys():
        value1 = ""
        value2 = ""
        son_key = ""
        for son_key in dict_overall[key].keys():
            if 'Drug A' in son_key:
                value1 = dict_overall[key][son_key]
        for son_key in dict_overall[key].keys():
            if 'Placebo' in son_key:
                value2 = dict_overall[key][son_key]
        if value1 == "":
            value1="nothing"
        if value2 == "":
            value2 = "nothing"
        row_value = get_last_row_ele(key)
        table_contents += (row_value+"||"+value1+"||"+value2+"|||")
    table_contents = table_contents[:-3]

    # 输出合并的信息
    if len(dict_china) >= len(dict_overall):
        emerged_table_out(dict_china,dict_overall,1)
    else:
        emerged_table_out(dict_overall,dict_china,2)
    #print( table_contents)

# 通过输入七元组，输出图表需要信息
def run_graph(table_emerged_compare_contents):
    content = table_emerged_compare_contents
    # 将所有位置的nothing换做0 以便后面对第四个和第七个值进行计算
    content= content.replace("nothing",'0')
    cut_tuple=re.compile(r'\|\|\|')
    cut_ele=re.compile(r'\|\|')
    dicts={}
    for tuple in cut_tuple.split(content):
        lst = cut_ele.split(tuple)
        if len(lst) == 7:
            key = lst[0].strip()
            dicts[key]=get_two_value(tuple)
    out_by_range(dicts,-1)


# 全局变量，单表内容信息,表间用||||隔开
table_contents=""
# 全局变量，合并后的内容
table_emerged_contents = ""
# 全局变量，合并后做过减法的内容
table_emerged_compare_contents= ""

#全局变量，需要的图表数据
graph_data = ""

if __name__ == "__main__":
    run_table()
    #print(table_contents+"\n")
    print(table_emerged_contents)
    print(table_emerged_compare_contents)
    run_graph(table_emerged_compare_contents)
    print(graph_data)

