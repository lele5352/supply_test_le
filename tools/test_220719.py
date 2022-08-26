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

"""
#列表合并成为字典
list1 = ['karl','lary','keera']
list2 = [28934,28935,28936]
# Method 1: zip()
dictt0 = dict(zip(list1, list2))
# Method 2: dictionary comprehension
dictt1 = {key:value for key,value in zip(list1,list2)}
"""

"""
#计算时间
import datetime
start = datetime.datetime.now()
time.sleep(2)
print(datetime.datetime.now()-start)
"""
import random
import requests
from tools.request_operator import RequestOperator
pre = "KW-SJQ-1"
url = "https://test189.popicorns.com/api/ec-wms-api/adjustReceipt"
authorization = "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1SWQiOjMwOCwidXNlcl9uYW1lIjoiaHVhbmdsZWxlQHBvcGljb3Jucy5jb20iLCJ2Ijo2Niwic2NvcGUiOlsiYWxsIl0sImV4cCI6MTY2MTU1ODM5OSwianRpIjoiNmZkYTYwM2MtM2ZkNC00NWQ3LWFlOTktOGQ2ZTliYjcwNmMwIiwiY2xpZW50X2lkIjoiaG9tYXJ5LWVjIn0.XJJGiGqUEt8xodgkKiwctGPOyorUMvqJcp_0zKbe9p_GbKsHg06TMYF1owePuKj0J2hvjnJAzVjaBgS2HrX2_Z5xzdO9piG6ff-dZ72892iSHGY7kmjM1tdOo63d9hfrPlfff2xk71Ar-N9itvCoUlkp-dh1HhKRUnPLgioo9Mc"
headers = {'Content-Type': 'application/json;charset=UTF-8', "Authorization": authorization,
           "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"}

# data = [
#     {
#     "waresSkuCode": "71230293819",
#     "storageLocationCode": "KW-SJQ-01",
#     "adjustReason": 2,
#     "changeCount": "1",
#     "changeType": 2,
#     "remark": "",
#     "waresSkuName": "岩板电视柜-淡灰色"
#     },
#     {
#         "waresSkuCode": "70076739388",
#         "storageLocationCode": "KW-SJQ-02",
#         "adjustReason": 2,
#         "changeCount": "1",
#         "changeType": 2,
#         "remark": "",
#         "waresSkuName": "白色岩板组合茶几"
#     }
# ]


for i in range(1, 100):
    a = str(i).rjust(3, '0')
    kw = pre + a

    data_list = [
        {
            "waresSkuCode": "71230293819",
            "storageLocationCode": kw,
            "adjustReason": 2,
            "changeCount": str(random.randint(0, 5)),
            "changeType": 2,
            "remark": "",
            "waresSkuName": "岩板电视柜-淡灰色"
        },
        {
            "waresSkuCode": "70076739388",
            "storageLocationCode": kw,
            "adjustReason": 2,
            "changeCount": str(random.randint(0, 5)),
            "changeType": 2,
            "remark": "",
            "waresSkuName": "白色岩板组合茶几"
        }
    ]
    # data_list = [
    #     {
    #         "waresSkuCode": "13939177553A01",
    #         "storageLocationCode": kw,
    #         "adjustReason": 2,
    #         "changeCount": str(random.randint(0, 5)),
    #         "changeType": 2,
    #         "remark": "",
    #         "waresSkuName": "植物攀爬架"
    #     },
    #     {
    #         "waresSkuCode": "20330092784",
    #         "storageLocationCode": kw,
    #         "adjustReason": 2,
    #         "changeCount": str(random.randint(0, 5)),
    #         "changeType": 2,
    #         "remark": "",
    #         "waresSkuName": "60件套刀叉套装-黑金(12)"
    #     }
    # ]
    # print(data_list)
    for x in data_list:
        if int(x["changeCount"]) == 0:
            # print(data_list.index(x))
            del data_list[data_list.index(x)]
    res = requests.post(url, headers=headers, json=data_list)
    print(i, res.json())

