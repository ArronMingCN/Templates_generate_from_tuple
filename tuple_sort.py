import os
import re




def tuple_sort_by_data(tuple_file):
    f = open(tuple_file, "r", encoding="utf-8")
    cut_tuple = re.compile("\|\|")
    dicts = {}
    for tuple in f.readlines():
        tuple = tuple.strip()
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
                    value = 0
                else:
                    datas=handle_tuple_element_data(ele)
                    if len(datas)<2 : #没有第二个值，即为0
                        value = 0
                    else:
                        value=datas[1]
                    # 得到的为第二个值
            else:
                print("not the standard 3_ele_tuple!")
                break
            count += 1
        dicts[key] = float(value)
    get_list = sorted(dicts.items(), key=lambda d: d[1], reverse=True)  # 返回list
    back_to_dict = dict(get_list)  # 转换为dict
    '''
    for i in back_to_dict.keys():
        print(i)
        print(back_to_dict[i])
    '''
    return back_to_dict


# 初步发现元组第三个元素data具有类似 80 (74.2)的特征，摘出其第二个值，以备排序
def handle_tuple_element_data(ele):
    ele = ele.strip()
    cut_blank = re.compile(" ")
    cut_comma = re.compile(",")
    decimal_count = re.compile(u'\d+\.\d\d')  # 判断小数位数大于等于两位的情况
    cut_inside = re.compile("\d+\.\d*")
    results = []  # 返回两个整形
    count = 0
    for nums in cut_blank.split(ele):
        nums = nums.strip()
        if count == 0:  # 处理括号外
            if (nums.isdecimal() == True):
                results.append(int(round(float(nums))))
            else:
                results.append(nums)

        elif count == 1:  # 处理括号里面
            nums = nums.strip()
            nums = nums[1:(len(nums) - 1)]  # 获得括号中的内容
            insides = cut_comma.split(nums)  # 逗号切分
            for i in insides:
                i = i.strip()
                if '%' in i:
                    i = i[:len(i) - 1]  # 去掉百分号
                    i = str(int(round(float(i))))
                    results.append(i + "%")
                elif i.isalpha() == True:  # 纯字母情况
                    results.append(i)
                else:  # 纯数字情况，判断小数位数
                    r = re.match(decimal_count, str(i))
                    if r:  # 若存在，则保留一位小数
                        r = round(float(r.group()), 1)
                    else:
                        r = i
                    results.append(str(r))
        else:
            break
        count += 1
    return results

#通过value选取词典中符合的键值对，返回符合选取范围的list
def get_sorted_tuples_by_value(dicts, value):
    list=[]  #将需要的三元组存入list
    for i in dicts.keys():
        if dicts[i] >= float(value):
            list.append(i+"||"+str(dicts[i])+"%")
        else:
            #如果已经排序好，到这里就说明已经结束！可以节省资源
            break
    return list

#通过list和模板1   in the med group 生成句子
def generize_sentence_bytemp1(tuple_list,value):
    #列名
    column=""
    #and之前的语法句子
    eles_before_and=""
    #最后一个元素
    last_word=""
    cut_tuple=re.compile(r"\|\|")
    #template2="The most frequently reported TEAEs"+column2+"in the control group were neutrophil count decreased (38.5%), platelet count decreased (26.9%), pyrexia (26.9%), and neutropenia (21.2%)."
    lenth=len(tuple_list)
    if lenth < 1:
        print("There is no such data in the med A group!")
        return

    for i in range(lenth-1):
        eles=cut_tuple.split(tuple_list[i])
        eles_before_and+=eles[0].lower()+" ("+eles[2]+"),"
    last_tuple=tuple_list[-1]
    ele_list=cut_tuple.split(last_tuple)
    last_word=ele_list[0].lower()+" ("+ele_list[2]+")"
    column="of "+ele_list[1].lower()
    if lenth==1:
        template1 = "The most frequently reported TEAEs (≥" + str(
            value)+"%"+ " of subjects) " + column + " in the med A group were " +last_word + "."
    else:
        template1 = "The most frequently reported TEAEs (≥" + str(value)+"%" + " of subjects) " + column + " in the med A group were "+eles_before_and+"and "+last_word+"."

    print(template1)
    return template1

#通过list和模板2 in the control group生成句子
def generize_sentence_bytemp2(tuple_list,value):
    #列名
    column=""
    #and之前的语法句子
    eles_before_and=""
    #最后一个元素
    last_word=""
    cut_tuple=re.compile(r"\|\|")
    lenth=len(tuple_list)
    if lenth < 1:
        print("There is no such data in the med A group!")
        return

    for i in range(lenth-1):
        eles=cut_tuple.split(tuple_list[i])
        eles_before_and+=eles[0].lower()+" ("+eles[2]+"),"
    last_tuple=tuple_list[-1]
    ele_list=cut_tuple.split(last_tuple)
    last_word=ele_list[0].lower()+" ("+ele_list[2]+")"
    column="of "+ele_list[1].lower()
    if lenth==1:
        template2 = "The most frequently reported TEAEs (≥" + str(
            value)+"%"+ " of subjects) " + column + " in the control group were " +last_word + "."
    else:
        template2 = "The most frequently reported TEAEs (≥" + str(value)+"%" + " of subjects) " + column + " in control group were "+eles_before_and+"and "+last_word+"."
    print(template2)
    return template2




if __name__ == "__main__":
    value=input("Please input the range:")
    tuple_list=get_sorted_tuples_by_value(tuple_sort_by_data("test.txt"), value)
    generize_sentence_bytemp2(tuple_list,value)