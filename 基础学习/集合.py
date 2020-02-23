#集合元素不可重复,  不同集合之间可以进行 并集/差集/等等

set1 = {1, 2, 3, 4}
set2 = {1, 2, 7, 8}
print(set1 - set2)   #set1有,set2没有的
print(set2 - set1)  #set2有,set1没有的
print(set1 | set2)  #并集
print(set1 & set2)  #交集
print(set1 ^ set2)  #set1,set2并集-交集

mylist = [1, 2, 3, 3]
new = list(set(mylist))
print(new)
