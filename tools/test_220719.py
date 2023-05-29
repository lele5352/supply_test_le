import time
# arr = list(map(int, input().split()))
# print('Input List:', arr)

"""
#两个字典合并
basic_information = {"name":['karl','Lary'],"mobile":["0134567894","0123456789"]}
academic_information = {"grade":["A","B"]}
details = dict() ## Combines Dict
## Dictionary Comprehension Method
details = {key: value for data in (basic_information, academic_information) for key,value in data.items()}
print(details)
## Dictionary unpacking
details = {**basic_information, **academic_information}
print(details)
## Copy and Update Method
details = basic_information.copy()
details.update(academic_information)
print(details)
"""


#列表合并成为字典
list1 = ['a', 'b', 'c']
list2 = [1, 2, 3]


# Method 1: zip()
# dictt0 = dict(zip(list1, list2))
dictt0 = zip(list1, list2)
for i in dictt0:
    print(i)

# Method 2: dictionary comprehension
# dictt1 = {key: value for key, value in zip(list1, list2)}


"""
#计算时间
import datetime
start = datetime.datetime.now()
time.sleep(2)
print(datetime.datetime.now()-start)
"""