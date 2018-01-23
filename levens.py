#! python3
import Levenshtein

str_report = "A summary of subject disposition for all treated subjects is provided in Table 1. In the 16 mg/kg group, 90 of 106 subjects (85%) discontinued treatment; the majority of treatment discontinuations (82 subjects; 77%) were due to progressive disease. Five subjects (5%) discontinued from treatment due to a TEAE. "

list_key = ["16 mg/kg",
"106",
"90 (85%)",
"82 (77%)",
"5 (5%)"
]

str_test1 = "A summary of subject disposition for all treated subjects is provided in Table 1"
str_test2 = "Table 1:	Subject Disposition Treatment All Treated Analysis Set"
str_test3 = "asdasd di2scontinued treatment22"
list_a = str_test1.split(" ")
list_b = str_test2.split()
for i in range(len(list_a)):
    for j in range( len(list_b)):
        print(list_a[i] + "  " + list_b[j] + "  " + str(Levenshtein.distance(list_a[i], list_b[j])) + "  "+  str(Levenshtein.ratio(list_a[i], list_b[j])))
        if Levenshtein.distance(list_a[i], list_b[j]) < 4 and Levenshtein.ratio(list_a[i], list_b[j]) >= 0.5 :
            list_a[i] = "&title;"

print(str(Levenshtein.ratio("A" , "Disposition")))
for i in range(len(list_a)):
    if i > 0:
        if list_a[i] == list_a[i-1] == "&title;":
            continue
    print(list_a[i]  , end=' ')