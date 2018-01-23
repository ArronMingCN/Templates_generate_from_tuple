#! python3

import re
import  sys

f_out=open("new_form_data.txt","w")
def change(old_file):
    f_old=open(old_file)
    cut_Ele=re.compile(r';')
    for line in f_old.readlines():
        cut_off = line.find("----")
        tuple_line = line[:cut_off]
        sentence_line = line[cut_off + 4:]
        tuple_line = tuple_line.strip()
        sentence_line = sentence_line.strip()
        new_line=""
        count=1
        for ele in cut_Ele.split(tuple_line):
            if count==1:
                count+=1
                continue
            elif count==2:
                if ele=="":
                    count+=1
                    continue
                new_line+=(ele+"|")
            elif count==3:
                if ele=="":
                    count += 1
                    continue
                new_line+=(ele+"||")
            elif count==4:
                if ele=="":
                    count += 1
                    continue
                new_line+=(ele+"|")
            elif count == 5:
                if ele == "":
                    count += 1
                    continue
                new_line+=(ele + "||")
            elif count == 6:
                if ele == "":
                    count += 1
                    continue
                new_line+=(ele)
            else:
                break
            count += 1
        f_out.write(new_line+"----"+sentence_line+"\n")
    f_out.close()
if  __name__ == "__main__":
    change("table_content.txt")
