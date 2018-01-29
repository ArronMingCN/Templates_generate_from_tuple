#! Python3
# -*- coding: utf-8 -*-
import sys
import re




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


def run_graph():
    f=open("table_emerged.txt","r",encoding="utf-8")
    content=f.read()
    content= content.replace("nothing",'0')
    cut_tuple=re.compile(r'\|\|\|')
    cut_ele=re.compile(r'\|\|')
    dicts={}
    print(content)
    for tuple in cut_tuple.split(content):
        lst = cut_ele.split(tuple)
        if len(lst) == 7:
            key = lst[0].strip()
            dicts[key]=get_two_value(tuple)
    for i in dicts.keys():
        print(i+"||"+str(dicts[i]['val_1'])+"||"+str(dicts[i]['val_2']))
    out_by_range(dicts,-1)

#通过threshold输出符合范围值的项
def out_by_range(dicts,threshold):
    f_out = open("graph_data.txt","w",encoding="utf-8")
    emerged_contents = ""
    lst = []
    for key in dicts.keys():
        if float(dicts[key]['val_1']) <= threshold and float(dicts[key]['val_2']) <= threshold:
            lst.append(key)

    # 输出横坐标项
    for i in range(len(lst)-1):
        f_out.write(lst[i]+"||")
    f_out.write(lst[-1]+"|||")
    # 输出纵坐标值，顺序对应前面的横坐标数据，每个横坐标对应两个值，用|隔开，每两个值用||隔开
    for i in range(len(lst)-1):
        f_out.write(str(dicts[lst[i]]['val_1'])+"|"+str(dicts[lst[i]]['val_2'])+"||")
    f_out.write(str(dicts[lst[-1]]['val_1']) + "|" + str(dicts[lst[-1]]['val_2']))

    f_out.close()
    print("Done")

if __name__ == "__main__":
    run_graph()