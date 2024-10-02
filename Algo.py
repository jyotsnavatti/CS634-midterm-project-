import sys
from itertools import combinations
from itertools import permutations
from typing import Dict
#How to run
#python Algo.py datasetname {minimum support(in percentage)} {minimum confidence(in percentage)}
def print_item_set(frequent_set,n):
    print("########################################")
    print("Selected itemsets after ",n," iteration")
    print("__Itemset__", "__Support__")
    print("########################################")
    print()
    for i in frequent_set:
        print(i,round(frequent_set[i]*100/total_no_tx,2),)
    print()


def find_freq_set(list1, notconsider, item_set_list, n):
    comb = combinations(list1, n)
    item_support_count = {}
    for i in comb:
        set_i = set(i)
        i=tuple(sorted(i))
        for j in item_set_list:
            if set_i.issubset(j):
                if notconsider:
                    count = 0
                    for k in notconsider:
                        if k.issubset(set_i):
                            count = 1
                            break
                    if not count:
                        if i in item_support_count:
                            item_support_count[i] += 1
                        else:
                            item_support_count[i] = 1
                else:
                    if i in item_support_count:
                        item_support_count[i] += 1
                    else:
                        item_support_count[i] = 1
    frequent_set_to_return = {}
    rejected_set_to_return = []
    # print(item_support_count)
    if item_support_count:
        print("************************")
        print("Itemsets for ", n, "Iteration")
        print("************************")
        print()
        for i in item_support_count:
            print(i,round(item_support_count[i]*100/total_no_tx,2))
            if (item_support_count[i]/total_no_tx)*100 >= min_supp:
                frequent_set_to_return[i] = item_support_count[i]
            else:
                rejected_set_to_return.append(set(list(i)))
        print()
        if frequent_set_to_return:
            print_item_set(frequent_set_to_return,n)
            support_of_all_item_set.update(item_support_count)
            generate_association_rule(frequent_set_to_return)
            return frequent_set_to_return, rejected_set_to_return
    return None,None

def generate_association_rule(frequent_set):
    for items_set_tuple in frequent_set.keys():
        print("Association Rule for itemset - ",items_set_tuple)
        print("__Rules__","__Confidence__")
        size_of_item_set=len(items_set_tuple)
        itemset=set(items_set_tuple)
        while size_of_item_set-1>0:
            comb = combinations(items_set_tuple, size_of_item_set-1)
            for i in comb:
                left_side_items=i
                right_side_items=tuple(itemset-set(i))
                item_conf=round(support_of_all_item_set[items_set_tuple]*100/support_of_all_item_set[left_side_items],2)
                if item_conf>=min_conf:
                    print(left_side_items,"=>",right_side_items,item_conf,"Rule Selected")
                else:
                    print(left_side_items,"=>",right_side_items,item_conf,"Rule Rejected")

            size_of_item_set -=1
        print()


###Program Start from here###
file_name = sys.argv[1]
file_object = open(file_name, "r")
lines = file_object.readlines()
all_tx = []
total_no_tx=0
support_of_all_item_set={}
min_supp = int(sys.argv[2])
min_conf = int(sys.argv[3])
c1 = {}  # type: Dict[str, int]
item_set_list = []
print("********************")
print("Input Transactions")
print("********************")
print()

for line in lines:
    line = line.replace("\n", "")
    print(line)
    all_tx.append("".join(line.split(" ")[1].split(",")))
    seen = set()
    for i in "".join(line.split(" ")[1:]).split(","):

        if (i,) in c1:
            c1[(i,)] += 1
        else:
            # print((i,),line)
            c1[(i,)] = 1
        seen.add(i)
    item_set_list.append(seen)
    total_no_tx+=1
    # print(seen)
frequent_set = {}
# print(c1)
rejected_set = []
print()
print("************************")
print("Item Sets", 1, "Iteration")
print("************************")
print()
for i in c1:
    print(i,round(c1[i]*100/total_no_tx))
    if (c1[i]/20)*100 >= min_supp:
        frequent_set[i] = c1[i]
    else:
        rejected_set.append(set(i))
support_of_all_item_set.update(c1)
list1 =[item[0] for item in frequent_set.keys()]

print()
print_item_set(frequent_set,1)
item_set_size = 1
while len(list1) > item_set_size:
    frequent_set1, rejected_set1 = find_freq_set(list1, rejected_set, item_set_list, item_set_size + 1)
    if not frequent_set1:
        break
    item_list = [items for item_tuples in list(frequent_set1.keys()) for items in item_tuples]
    list1 = list(set(item_list))
    rejected_set = rejected_set1
    frequent_set=frequent_set1
    item_set_size += 1

