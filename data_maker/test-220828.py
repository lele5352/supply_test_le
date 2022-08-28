import json
import random
picking_detail_info = '{"code":200,"message":"操作成功","data":{"id":4766,"pickOrderNo":"DJH2208280001","receiveWarehouseCode":"LELE-BH","receiveWarehouseName":"乐乐备货","receiveTargetWarehouseCode":null,"receiveTargetWarehouseName":null,"deliveryWarehouseCode":null,"deliveryWarehouseName":null,"deliveryTargetWarehouseCode":null,"deliveryTargetWarehouseName":null,"createUsername":"黄乐乐","createTime":1661673310000,"state":3,"goodsType":2,"pickType":1,"pickOrderType":1,"pickUserId":null,"pickUsername":"黄乐乐","pickTime":1661673333000,"trayCount":4,"trayQty":0,"exceptionQty":0,"waitTrayQty":4,"details":[{"pickOrderNo":null,"id":12013,"storageLocationCode":null,"storageLocationId":null,"goodsSkuCode":"71230293819","goodsSkuName":"岩板电视柜-白色","waresSkuCode":"71230293819","waresSkuName":"岩板电视柜-淡灰色","shouldPickQty":2,"realPickQty":2,"goodsSkuImg":"https://img1.popicorns.com/fit-in/200x200/mall/file/2021/12/02/709b2a91c7b148fc9cd7c7a6407a767c.jpg","trayQty":0,"errorQty":0,"divertState":0,"demandDetails":null},{"pickOrderNo":null,"id":12012,"storageLocationCode":null,"storageLocationId":null,"goodsSkuCode":"70076739388","goodsSkuName":"白色岩板组合茶几","waresSkuCode":"70076739388","waresSkuName":"白色岩板组合茶几","shouldPickQty":2,"realPickQty":2,"goodsSkuImg":"https://img1.popicorns.com/fit-in/200x200/mall/file/2021/08/02/74d94f24f1704f6fb9bacb1099df77d9.jpg","trayQty":0,"errorQty":0,"divertState":0,"demandDetails":null}],"stateName":"装托中","goodsTypeName":null,"pickTypeName":"纸质单","pickOrderTypeName":"调拨拣货","distributeStatusName":"已分配","expectTrayDetails":[{"waresSkuCode":"71230293819","expectQty":2},{"waresSkuCode":"70076739388","expectQty":2}]}}'
picking_detail_info = json.loads(picking_detail_info)
picking_detail_info = picking_detail_info.get("data")
pick_order_no = picking_detail_info.get("pickOrderNo")

tray_infos = []  # 装托的sku信息
data = []  # 接口内参数信息
# 通过获取拣货单内已拣货sku信息列表数据，拼接按需装托相关参数
for i in picking_detail_info.get("details"):
    for j in range(i["realPickQty"]):
        sku_info = {
            "id": i["id"],
            "waresSkuCode": i["waresSkuCode"],
            "waresSkuName": i["waresSkuName"],
            "goodsSkuCode": i["goodsSkuCode"],
            "goodsSkuName": i["goodsSkuName"],
            "skuQty": 1
        }
        tray_infos.append(sku_info)
random.shuffle(tray_infos)
print(tray_infos)
