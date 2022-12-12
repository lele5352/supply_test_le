from data_maker import *


def create_demand_all():
    list_demand_code = []
    for i in range(4, 9):
        if i == 1:
            # 需求1：备货--部件--C bom
            kw = {"demandType": 2, "goodsSkuCode": "BP53586714577C01", "bomVersion": "C"}
        elif i == 2:
            # 需求2：缺货--部件--C bom
            kw = {"demandType": 1, "goodsSkuCode": "BP53586714577C01", "bomVersion": "C"}
        elif i == 3:
            # 需求2：备货--部件--B bom
            kw = {"demandType": 2, "goodsSkuCode": "BP53586714577B01", "demandQty": 1, "bomVersion": "B"}
        elif i == 4:
            # 需求2：缺货--部件--B bom
            kw = {"demandType": 1, "goodsSkuCode": "BP53586714577B02", "demandQty": 2, "bomVersion": "B"}
        elif i == 5:
            # 需求1：备货--销售--C bom
            kw = {"demandType": 1, "goodsSkuCode": "53586714577", "bomVersion": "A"}
        elif i == 6:
            # 需求2：缺货--销售--C bom
            kw = {"demandType": 1, "goodsSkuCode": "53586714577", "bomVersion": "A"}
        elif i == 7:
            # 需求2：备货--销售--B bom
            kw = {"demandType": 2, "goodsSkuCode": "53586714577", "bomVersion": "B"}
        elif i == 8:
            # 需求2：缺货--销售--B bom
            kw = {"demandType": 1, "goodsSkuCode": "53586714577", "bomVersion": "B"}
        else:
            print("不在测试数据范围内，请检查循环数量")

        res = wms_service.service_demand_create(**kw)
        list_demand_code.append(res.get("data")["demandCode"])
        print(list_demand_code)
    return list_demand_code

if __name__ == '__main__':
    create_demand_all()
