import requests
import json
from tools import read_db, read_ever
import time
from produce import login


class GetWarehouse():

    def switch_warehouse(self, warehouse_code):
        login.Login().get_authorization("url.json", "config.json")
        warehouse_info = login.Login().switch_warehouse("url.json", "config.json", "warehouse.json", warehouse_code)
        return warehouse_info


class Transfer:
    def __init__(self, authorization):
        self.headers = {'Content-Type': 'application/json', 'charset': 'UTF-8', 'Authorization': authorization}
        self.pick_order_no = ''
        self.entryorderid = ''
        self.box_info = ''
        self.transfer_out_no = ''

    # 其他入库-新增
    def other_add(self):
        url_other_add = 'https://test-scms.popicorns.com/api/ec-wms-api/entryorder'
        data_add = {
            "entryOrderType": 3,
            # "eta": 1642403631000,
            # "supplierCode": null,
            # "fromOrderCode": null,
            # "remark": null,
            "qualityType": 0,
            # "timestamp": 1642403631000,
            "logisticsInfoList": [],
            "skuInfoList": [
                {
                    "warehouseSkuCode": "53586714577B02",
                    "planSkuQty": 20,
                    "warehouseSkuName": "部件2 2/2 X2",
                    "warehouseSkuWeight": "5",
                    "saleSkuCode": "53586714577",
                    "saleSkuName": "决明子",
                    "bomVersion": "B",
                    "saleSkuImg": "https://img.popicorns.com/dev/file/2021/11/08/8cbba5e1160a48e9bd9b43e54450ab7c.jpg",
                    "warehouseSkuHeight": "10",
                    "warehouseSkuLength": "10",
                    "warehouseSkuWidth": "10"
                },
                {
                    "warehouseSkuCode": "53586714577B01",
                    "planSkuQty": 5,
                    "warehouseSkuName": "部件1 1/2 X1",
                    "warehouseSkuWeight": "5",
                    "saleSkuCode": "53586714577",
                    "saleSkuName": "决明子",
                    "bomVersion": "B",
                    "saleSkuImg": "https://img.popicorns.com/dev/file/2021/11/08/8cbba5e1160a48e9bd9b43e54450ab7c.jpg",
                    "warehouseSkuHeight": "10",
                    "warehouseSkuLength": "10",
                    "warehouseSkuWidth": "10"
                },
                {
                    "warehouseSkuCode": "53586714577D01",
                    "planSkuQty": 10,
                    "warehouseSkuName": "单品2个组成1个销售sku 1/1 X2",
                    "warehouseSkuWeight": "50",
                    "saleSkuCode": "53586714577",
                    "saleSkuName": "决明子",
                    "bomVersion": "D",
                    "saleSkuImg": "https://img.popicorns.com/dev/file/2021/11/08/8cbba5e1160a48e9bd9b43e54450ab7c.jpg",
                    "warehouseSkuHeight": "50",
                    "warehouseSkuLength": "50",
                    "warehouseSkuWidth": "50"
                }
            ],
            "operationFlag": 0
        }
        res = requests.post(url_other_add, headers=self.headers, data=json.dumps(data_add))
        self.entryorderid = res.json().get('data')['entryOrderId']
        print('新增入库单' + res.json().get('message'))

    # 其他入库-提交
    def other_submit(self):

        url_other_submit = 'https://test-scms.popicorns.com/api/ec-wms-api/entryorder'
        data_submit = {
            "entryOrderId": self.entryorderid,
            "entryOrderType": 3,
            "eta": 1642348800000,
            # "supplierCode": null,
            # "fromOrderCode": null,
            "qualityType": 0,
            # "remark": null,
            "logisticsInfoList": [],
            "skuInfoList": [
                {
                    "warehouseSkuCode": "53586714577B02",
                    "planSkuQty": 20,
                    "warehouseSkuName": "部件2",
                    "warehouseSkuWeight": "5",
                    "saleSkuCode": "53586714577",
                    "saleSkuName": "决明子",
                    "bomVersion": "B",
                    "saleSkuImg": "https://img1.popicorns.com/fit-in/200x200/dev/file/2021/11/08/8cbba5e1160a48e9bd9b43e54450ab7c.jpg",
                    "warehouseSkuHeight": "10",
                    "warehouseSkuLength": "10",
                    "warehouseSkuWidth": "10"
                },
                {
                    "warehouseSkuCode": "53586714577B01",
                    "planSkuQty": 5,
                    "warehouseSkuName": "部件1",
                    "warehouseSkuWeight": "5",
                    "saleSkuCode": "53586714577",
                    "saleSkuName": "决明子",
                    "bomVersion": "B",
                    "saleSkuImg": "https://img1.popicorns.com/fit-in/200x200/dev/file/2021/11/08/8cbba5e1160a48e9bd9b43e54450ab7c.jpg",
                    "warehouseSkuHeight": "10",
                    "warehouseSkuLength": "10",
                    "warehouseSkuWidth": "10"
                },
                {
                    "warehouseSkuCode": "53586714577D01",
                    "planSkuQty": 10,
                    "warehouseSkuName": "单品2个组成1个销售sku",
                    "warehouseSkuWeight": "50",
                    "saleSkuCode": "53586714577",
                    "saleSkuName": "决明子",
                    "bomVersion": "D",
                    "saleSkuImg": "https://img1.popicorns.com/fit-in/200x200/dev/file/2021/11/08/8cbba5e1160a48e9bd9b43e54450ab7c.jpg",
                    "warehouseSkuHeight": "50",
                    "warehouseSkuLength": "50",
                    "warehouseSkuWidth": "50"
                }
            ],
            "operationFlag": 1
        }
        res = requests.post(url_other_submit, headers=self.headers, data=json.dumps(data_submit))
        print(res.json().get('message'))

    # 其他入库-上架
    def other_upper(self, location_code):
        url_other_upper = 'https://test-scms.popicorns.com/api/ec-wms-api/entryorder/putOnTheShelf'
        data_upper = {
            "entryOrderId": self.entryorderid,
            "skuList": [
                {
                    "skuCode": "53586714577B02",
                    "shelvesLocationCode": location_code,
                    "skuQty": "20",
                    "abnormalQty": 0
                },
                {
                    "skuCode": "53586714577B01",
                    "shelvesLocationCode": location_code,
                    "skuQty": "5",
                    "abnormalQty": 0
                },
                {
                    "skuCode": "53586714577D01",
                    "shelvesLocationCode": location_code,
                    "skuQty": "10",
                    "abnormalQty": 0
                }
            ]
        }
        res = requests.post(url_other_upper, headers=self.headers, data=json.dumps(data_upper))
        print('上架' + res.json().get('message'))

    # 删除库存
    def del_wares(self):
        sql_ims_list = [
            "DELETE FROM wares_inventory WHERE ware_sku_code LIKE '53586714577%';",
            "DELETE FROM goods_inventory WHERE goods_sku_code = '53586714577' ;",
            "DELETE FROM central_inventory WHERE goods_sku_code = '53586714577';",
        ]

        # sql_wms_list = [
        #     "DELETE FROM trf_transfer_out_order WHERE warehouse_id =536;",
        #     "DELETE FROM trf_transfer_out_order_detail WHERE warehouse_id =536;",
        #     "DELETE FROM trf_transfer_in_order WHERE warehouse_id =517;",
        #     "DELETE FROM trf_transfer_in_order_detail WHERE warehouse_id =536;",
        #     "DELETE FROM trf_box_order WHERE warehouse_id =536;",
        #     "DELETE FROM trf_box_order_detail WHERE warehouse_id =536;",
        #     "DELETE FROM trf_box_order_in WHERE warehouse_id =517;",
        #     "DELETE FROM trf_box_order_detail_in WHERE warehouse_id =536;",
        #     "DELETE FROM trf_handover_order WHERE warehouse_id =536;",
        #     "DELETE FROM trf_transfer_demand WHERE warehouse_id =536;",
        #     "DELETE FROM trf_transfer_pick_order WHERE warehouse_id =536;",
        #     "DELETE FROM trf_transfer_pick_order_detail WHERE warehouse_id = 536;"
        # ]

        for i in sql_ims_list:
            read_db.ReadDB('ims').execute(i)

        # for i in sql_wms_list:
        #     read_db.ReadDB('wms').execute(i)

    # 添加库存
    def add_wares(self, location_code):
        self.other_add()
        self.other_upper(location_code)

    # 获取仓库信息
    def get_warehouse_info(self, wareshouse_code):
        warehouse_info = read_ever.GetData().get_wareshouse_info(wareshouse_code)
        return warehouse_info

    # 创建调拨需求-备货
    def add_demand(self, delivery_warehouse_code, delivery_target_warehouse_code, receive_warehouse_code,
                   receive_target_warehouse_code, sku_info):
        url_add_demand = 'https://test-scms.popicorns.com/api/ec-oms-api/demand/create'

        delivery_warehouse_info = self.get_warehouse_info(delivery_warehouse_code)
        receive_warehouse_info = self.get_warehouse_info(receive_warehouse_code)
        delivery_target_warehouse_info = self.get_warehouse_info(delivery_target_warehouse_code)
        receive_target_warehouse_info = self.get_warehouse_info(receive_target_warehouse_code)

        if delivery_target_warehouse_info:
            delivery_target_warehouse_id = delivery_target_warehouse_info.get("warehouseId")
            delivery_target_warehouse_code = delivery_target_warehouse_info.get("warehouseCode")
            delivery_target_warehouse_name = delivery_target_warehouse_info.get("warehouseName")
        else:
            delivery_target_warehouse_id = None
            delivery_target_warehouse_code = None
            delivery_target_warehouse_name = None

        if receive_target_warehouse_info:
            receive_target_warehouse_id = receive_target_warehouse_info.get("warehouseId")
            receive_target_warehouse_code = receive_target_warehouse_info.get("warehouseCode")
            receive_target_warehouse_name = receive_target_warehouse_info.get("warehouseName")
        else:
            receive_target_warehouse_id = None
            receive_target_warehouse_code = None
            receive_target_warehouse_name = None

        for item in sku_info:
            data_demand = {
                "deliveryWarehouseId": delivery_warehouse_info.get("warehouseId"),
                "deliveryWarehouseName": delivery_warehouse_info.get("warehouseName"),
                "deliveryWarehouseCode": delivery_warehouse_info.get("warehouseCode"),
                "deliveryTargetWarehouseId": delivery_target_warehouse_id,
                "deliveryTargetWarehouseName": delivery_target_warehouse_name,
                "deliveryTargetWarehouseCode": delivery_target_warehouse_code,
                "receiveWarehouseId": receive_warehouse_info.get("warehouseId"),
                "receiveWarehouseName": receive_warehouse_info.get("warehouseName"),
                "receiveWarehouseCode": receive_warehouse_info.get("warehouseCode"),
                "receiveTargetWarehouseName": receive_target_warehouse_name,
                "receiveTargetWarehouseCode": receive_target_warehouse_code,
                "receiveTargetWarehouseId": receive_target_warehouse_id,
                "remark": "",
                "details": [
                    {
                        "itemSkuCode": item.get("sale_sku_code"),
                        "itemSkuType": 1,
                        "quantity": item.get("num"),
                        "itemPicture": "https://img.popicorns.com/dev/file/2021/11/08/8cbba5e1160a48e9bd9b43e54450ab7c.jpg"
                    }
                ]
            }
            time.sleep(1)
            res = requests.post(url_add_demand, headers=self.headers, data=json.dumps(data_demand))
            print('备货需求新增:' + res.json().get('message'))

    # 查询调拨需求
    """
    num：查询的需求单数量
    """

    def search_demand(self, num):
        url_search_demand = "https://test-scms.popicorns.com/api/ec-wms-api/transferOut/demand/list"
        data_search_demand = {
            "current": 1,
            "size": num,
            "states": [

            ],
            "receiveWarehouseCode": "",
            "demandCodeList": None,
            "goodsSkuCodeList": None,
            "startCreateTime": "",
            "endCreateTime": "",
            "sourceCodeList": None,
            "customerType": "",
            "createUserId": 10,
            "demandType": "",
            "cancelFlag": "",
            "sortField": [
                {
                    "field": "create_time",
                    "type": "DESC"
                }
            ],
            "saleOrderCodes": None
        }
        res = requests.post(url_search_demand, headers=self.headers, data=json.dumps(data_search_demand))
        demands = res.json().get("data").get("records")
        demands_list = []
        for i in demands:
            demands_list.append({
                "id": i.get("id"),
                "demandCode": i.get("demandCode")
            })
        print(demands_list)
        return demands_list

    # 取消调拨需求
    def cancel_demand(self):
        url_cancel_demand = 'https://test-scms.popicorns.com/api/ec-oms-api/demand/cancel'
        data_cancle_demand = {"id": 541}
        res = requests.post(url_cancel_demand, headers=self.headers, data=json.dumps(data_cancle_demand))
        print('取消调拨需求:' + res.json().get('message'))

    # 创建拣货单
    def create_pick(self):
        info = self.search_demand(3)
        demand_codes_list = []
        for item in info:
            demand_codes_list.append(str(item.get("demandCode")))
        url_create_pick = 'https://test-scms.popicorns.com/api/ec-wms-api/transferOut/picking/create'
        data_create_demand = {"demandCodes": demand_codes_list, "pickType": 1}
        res = requests.post(url_create_pick, headers=self.headers, data=json.dumps(data_create_demand))
        self.pick_order_no = res.json().get("data")
        print("创建拣货单:{0},拣货单号为：{1}".format(res.json().get("message"), self.pick_order_no))

    # 查询拣货单
    def search_pick_order(self):
        url_search_pick_order = 'https://test-scms.popicorns.com/api/ec-wms-api/transferOut/picking/list'
        data_search_pick_order = {
            "current": 1,
            "size": 10,
            "pickOrderNo": "",
            "createUsername": "",
            "pickingUser": "",
            "state": "",
            "pickType": "",
            "distributeStatus": "",
            "type": "",
            "payTime": [],
            "startPickTime": "",
            "endPickTime": "",
            "sortField": [
                {
                    "field": "create_time",
                    "type": "DESC"
                }
            ],
            "saleSkuCodes": [],
            "skuCodes": []
        }
        res = requests.post(url_search_pick_order, headers=self.headers, data=json.dumps(data_search_pick_order))
        pick_orders = res.json().get("data").get("records")
        pick_orders_list = []
        for i in pick_orders:
            pick_orders_list.append({
                "id": i.get("id"),
                "pickOrderNo": i.get("pickOrderNo")
            })
        return pick_orders_list

    # 分配拣货人
    def assign_picker(self):

        pick_orders = self.search_pick_order()
        pick_order_no = pick_orders[0].get("pickOrderNo")

        url_assign_picker = 'https://test-scms.popicorns.com/api/ec-wms-api/transferOut/picking/assignPickUser'
        data_assign_picker = {"pickOrderNos": [self.pick_order_no], "pickUsername": "黄乐乐", "pickUserId": "10"}
        res = requests.post(url_assign_picker, headers=self.headers, data=json.dumps(data_assign_picker))
        print("分配拣货人：", res.json().get("message"))

    # 查询拣货单详情
    def picking_detail(self):
        pick_orders = self.search_pick_order()
        pick_order_no = pick_orders[0].get("pickOrderNo")
        url_pciking_detail = "https://test-scms.popicorns.com/api/ec-wms-api/transferOut/picking/detail/{0}?t=1642684741035)".format(
            pick_order_no)
        res = requests.get(url_pciking_detail, headers=self.headers)
        picking_detail = res.json().get("data")
        return picking_detail

    # 确认拣货
    def do_picking(self, type):
        picking_detail = self.picking_detail()
        url_do_picking = "https://test-scms.popicorns.com/api/ec-wms-api/transferOut/picking/doPicking"
        pick_orders = self.search_pick_order()
        pick_order_no = pick_orders[0].get("pickOrderNo")
        data_pickung = {
            "pickOrderNo": pick_order_no,
            "details": picking_detail.get("details")
        }
        if type:
            # 全部拣货
            x = 0
            for item in data_pickung["details"]:
                item.update(realPickQty=data_pickung["details"][x]["shouldPickQty"])
                x += 1
        else:
            # 部分拣货
            x = 0
            y = [5, 8, 5, 10]
            for item in data_pickung["details"]:
                item.update(realPickQty=y[x])
                x += 1
        print(json.dumps(data_pickung))
        res = requests.post(url_do_picking, headers=self.headers, data=json.dumps(data_pickung))
        print("确认拣货：", res.json().get("message"))

    # PDA-拉取拣货单详情页
    def pda_picking_detail(self):
        pick_orders = self.search_pick_order()
        pick_order_no = pick_orders[0].get("pickOrderNo")
        url_pda_picking_detail = "https://test160.popicorns.com/api/ec-wms-api/transferOut/picking/demand/detail?pickOrderNo={0}".format(
            pick_order_no)
        res = requests.get(url_pda_picking_detail, headers=self.headers)
        picking_detail = res.json().get("data")
        return picking_detail

    # PDA-按需装托
    def submit_tray_info(self, type, location_code_tp):

        info = self.pda_picking_detail()
        url_submit_tray_info = "https://test160.popicorns.com/api/ec-wms-api/transferOut/pda/submitTrayInfo"
        if type:
            datas_submit_tray = [{
                "storageLocationCode": location_code_tp,
                "pickOrderNo": info["pickOrderNo"],
                "trayInfos": [{
                    "id": info["details"][0]["id"],
                    "waresSkuCode": "53586714577D01",
                    "waresSkuName": "单品2个组成1个销售sku 1/1 X2",
                    "goodsSkuCode": "53586714577",
                    "goodsSkuName": "决明子",
                    "skuQty": 10
                }, {
                    "id": info["details"][1]["id"],
                    "waresSkuCode": "53586714577B01",
                    "waresSkuName": "部件1 1/2 X1",
                    "goodsSkuCode": "53586714577",
                    "goodsSkuName": "决明子",
                    "skuQty": 5
                }, {
                    "id": info["details"][2]["id"],
                    "waresSkuCode": "53586714577B02",
                    "waresSkuName": "部件2 2/2 X2",
                    "goodsSkuCode": "53586714577",
                    "goodsSkuName": "决明子",
                    "skuQty": 20
                }]
            }]
        else:
            datas_submit_tray = [{
                "storageLocationCode": location_code_tp,
                "pickOrderNo": info["pickOrderNo"],
                "trayInfos": [{
                    "id": info["details"][0]["id"],
                    "waresSkuCode": "53586714577D01",
                    "waresSkuName": "单品2个组成1个销售sku 1/1 X2",
                    "goodsSkuCode": "53586714577",
                    "goodsSkuName": "决明子",
                    "skuQty": 10
                }, {
                    "id": info["details"][1]["id"],
                    "waresSkuCode": "53586714577B01",
                    "waresSkuName": "部件1 1/2 X1",
                    "goodsSkuCode": "53586714577",
                    "goodsSkuName": "决明子",
                    "skuQty": 5
                }, {
                    "id": info["details"][2]["id"],
                    "waresSkuCode": "53586714577B02",
                    "waresSkuName": "部件2 2/2 X2",
                    "goodsSkuCode": "53586714577",
                    "goodsSkuName": "决明子",
                    "skuQty": 13
                }]
            }]
        res = requests.post(url_submit_tray_info, headers=self.headers, data=json.dumps(datas_submit_tray))
        print("按需装托:", res.json().get("message"))

    # PDA-不成套移出
    def move_storage(self):
        pick_orders = self.search_pick_order()
        pick_order_no = pick_orders[0].get("pickOrderNo")
        url_move_storage = 'https://test160.popicorns.com/api/ec-wms-api/transferOut/pda/moveStorage'
        datas_move_storage = {
            "fromStorageLocationCode": "KW-RQ-TP-01",
            "waresSkuCode": "53586714577B01",
            "toStorageLocationCode": "KW-RQ-YK-01",
            "pickOrderNo": pick_order_no
        }
        print(datas_move_storage)
        for i in range(1):
            res = requests.post(url_move_storage, headers=self.headers, data=json.dumps(datas_move_storage))
        print("不成套移出:", res.json().get("message"))

    # PDA-创建出库单
    def finish_picking(self, location_code_tp):
        pick_orders = self.search_pick_order()
        pick_order_no = pick_orders[0].get("pickOrderNo")
        url_finish_picking = "https://test160.popicorns.com/api/ec-wms-api/transferOut/pda/finishPacking"
        datas_finish_picking = {
            "pickOrderNo": pick_order_no,
            "storageLocationCodes": [location_code_tp]
        }
        res = requests.post(url_finish_picking, headers=self.headers, data=json.dumps(datas_finish_picking))
        self.transfer_out_no = res.json().get("data")
        print("创建出库单:", res.json().get("message"))

    # 查询出库箱单
    def search_box_out_list(self):
        url_search_box_out_list = "https://test-scms.popicorns.com/api/ec-wms-api/transferOut/box/list"
        datas_search_box_out_list = {
            "current": 1,
            "size": 1,
            "boxNos": [],
            "storageLocationCodes": [],
            "transferOutNos": [],
            "state": "",
            "receiveWarehouseCode": "",
            "createUsername": "",
            "startCreateTime": "",
            "endCreateTime": "",
            "startUpdateTime": "",
            "endUpdateTime": "",
            "sortField": [
                {
                    "field": "create_time",
                    "type": "DESC"
                }
            ],
            "saleSkuCodes": [],
            "waresSkuCodes": []
        }
        res = requests.post(url_search_box_out_list, headers=self.headers, data=json.dumps(datas_search_box_out_list))
        return res.json().get("data").get("records")

    # PDA-调拨复核
    def review_submit(self):
        self.box_info = self.search_box_out_list()
        url_review_submit = "https://test160.popicorns.com/api/ec-wms-api/transferOut/box/review/submit"
        datas_review_submit = {
            "boxNo": self.box_info[0].get("boxNo"),
            "storageLocationCode": self.box_info[0].get("storageLocationCode")
        }
        res = requests.post(url_review_submit, headers=self.headers, data=json.dumps(datas_review_submit))
        print("调拨复核:", res.json().get("message"))

    # PDA-调拨出库--改单
    def change_order(self):
        # box_info = self.search_box_out_list()

        url_change_order = 'https://test160.popicorns.com/api/ec-wms-api/transferOut/modify/changeOrder'
        datas_change_order = {
            "transferOutNo": self.box_info[0].get("transferOutNo"),
            "changeSkuDetailList": [{
                "skuCode": "53586714577B02",
                "fromLocCode": "KW-RQ-TP-01",
                "toLocCode": "KW-RQ-YK-01",
                "skuQty": 2
            }, {
                "skuCode": "53586714577B01",
                "fromLocCode": "KW-RQ-TP-01",
                "toLocCode": "KW-RQ-YK-01",
                "skuQty": 1
            }, {
                "skuCode": "53586714577D01",
                "fromLocCode": "KW-RQ-TP-01",
                "toLocCode": "KW-RQ-YK-01",
                "skuQty": 4
            }]
        }
        res = requests.post(url_change_order, headers=self.headers, data=json.dumps(datas_change_order))
        print("调拨出库-改单:", res.json().get("message"))

    # PDA-调拨发货-扫描箱单
    def handover_bind(self):
        url_handover_bind = "https://test160.popicorns.com/api/ec-wms-api/transferOut/handover/bind"
        datas_handover_bind = {
            "boxNo": "DC2204090001-1",  # self.box_info[0].get("boxNo"),
            "handoverNo": None,
            "receiveWarehouseCode": None
        }
        res = requests.post(url_handover_bind, headers=self.headers, data=json.dumps(datas_handover_bind))
        return res.json().get("data")

    # PDA-调拨发货-发货
    def delivery_confirm(self):
        handover_no = self.handover_bind().get("handoverNo")
        url_delivery_confirm = "https://test160.popicorns.com/api/ec-wms-api/transferOut/handover/delivery/confirm"
        data_delivery_confirm = {
            "handoverNo": handover_no
        }
        print(data_delivery_confirm)
        res = requests.post(url_delivery_confirm, headers=self.headers, data=json.dumps(data_delivery_confirm))
        print("调拨发货:", res.json().get("message"))

    """-------------------------------调拨入库-------------------------------"""

    # 查询入库箱单
    def search_box_in(self, handover_no):

        url_search_box_in = "https://test-scms.popicorns.com/api/ec-wms-api/transferIn/input/box/page"
        datas_search_box_in = {
            "current": 1,
            "size": 10,
            "handoverNo": handover_no,
            "transferInNo": "",
            "inState": "",
            "deliveryWarehouseCode": "",
            "boxNos": [],
            "waresSkuCodes": [],
            "startEta": "",
            "endEta": "",
            "startCreateTime": "",
            "endCreateTime": ""
        }
        res = requests.post(url_search_box_in, headers=self.headers, data=json.dumps(datas_search_box_in))
        print(res.json().get("data"))
        return res.json().get("data").get("records")[0]

    # PDA-调拨入库-确认拣货
    def transfer_in_confirm(self, handover_no):
        url_transfer_in_confirm = "https://test160.popicorns.com/api/ec-wms-api/transferIn/handover/received/confirm"
        data_transfer_in_confirm = {
            "handoverNo": handover_no
        }
        res = requests.post(url_transfer_in_confirm, headers=self.headers, data=json.dumps(data_transfer_in_confirm))
        print("调拨收货:", res.json().get("message"))

    # PDA-调拨入库-整箱上架
    def transfer_in_receive_all(self, box_no, location_code):
        url_search_box = "https://test160.popicorns.com/api/ec-wms-api/transferIn/input/box/detail/pda?boxNo={0}".format(
            box_no)
        res = requests.get(url_search_box, headers=self.headers)
        transfer_in_box_no_info = res.json().get("data")
        url_receive_all = "https://test160.popicorns.com/api/ec-wms-api/transferIn/input/box/shelf"
        data_transfer_in_receive_all = {
            "boxNo": transfer_in_box_no_info["boxNo"],
            "storageLocationCode": location_code,
            "transferInNo": transfer_in_box_no_info["transferInNo"]
        }
        res = requests.post(url_receive_all, headers=self.headers, data=json.dumps(data_transfer_in_receive_all))
        print("整箱上架：", res.json().get("message"))

    # PDA-调拨入库-逐渐上架
    def transfer_in_receive_one(self, box_no):
        url_search_box = "https://test160.popicorns.com/api/ec-wms-api/transferIn/input/box/scan/pda"
        data_search_box = {
            "boxNo": box_no,
            "type": 2,
            "hideError": False
        }
        res = requests.post(url_search_box, headers=self.headers, data=json.dumps(data_search_box))
        box_info = res.json().get("data")
        url_transfer_in_receive_one = "https://test160.popicorns.com/api/ec-wms-api/transferIn/input/sku/shelf"
        data_transfer_in_recevie_one = [
            {
                "boxNo": box_no,
                "storageLocationCode": "KW-SJQ-01",
                "transferInNo": box_info.get("transferInNo"),
                "details": [{
                    "waresSkuCode": "53586714577D01",
                    "quantity": 5
                }, {
                    "waresSkuCode": "53586714577B02",
                    "quantity": 5
                }]
            },
            {
                "boxNo": box_no,
                "storageLocationCode": "KW-SJQ-02",
                "transferInNo": box_info.get("transferInNo"),
                "details": [{
                    "waresSkuCode": "53586714577D01",
                    "quantity": 3
                }, {
                    "waresSkuCode": "53586714577B01",
                    "quantity": 5
                }]
            },
            {
                "boxNo": box_no,
                "storageLocationCode": "KW-SJQ-03",
                "transferInNo": box_info.get("transferInNo"),
                "details": [{
                    "waresSkuCode": "53586714577D01",
                    "quantity": 2
                }, {
                    "waresSkuCode": "53586714577B02",
                    "quantity": 5
                }]
            }
        ]
        for item in data_transfer_in_recevie_one:
            res = requests.post(url_transfer_in_receive_one, headers=self.headers, data=json.dumps(item))
            print("逐件上架：", res.json().get("message"))


if __name__ == '__main__':
    """
    测试使用仓库：
    533	佛山1号备货仓	CNFS02-BH   KW-SJQ-05   KW-RQ-TP-05
    534	佛山2号备货仓	CNFS03-BH   KW-SJQ-06   KW-RQ-TP-06

    537	佛山1号中转仓	CNFS02-ZZ
    535	佛山2号中转仓	CNFS03-ZZ
    516 佛山中转      FSZZ

    539	英国1号仓	UKBH01      KW-SJQ-01   KW-RQ-TP-01
    540	法国1号仓	ZY-FOR      KW-SJQ-03   KW-RQ-TP-03

    532	英国2号仓	UKBH02      KW-SJQ-02   KW-RQ-TP-02
    530	休斯顿1号仓	USTX01      KW-SJQ-04   KW-RQ-TP-04
    """

    warehouse_info = GetWarehouse().switch_warehouse("UKBH01")  # 切换到预期仓库
    authorization = read_ever.GetData().get_authorization("config.json")  # 获取token
    player = Transfer(authorization)

    """--------调拨出库--------"""
    """
    # player.del_wares()  # 删除库存
    location_code = "KW-SJQ-01"
    player.add_wares(location_code)     #添加库存

    player.add_demand("UKBH01", "", "UKBH02", "", [{"sale_sku_code": "53586714577", "num": 5}, {"sale_sku_code": "53586714577", "num": 5}, {"sale_sku_code": "BP53586714577B02", "num": 10}])     #新增调拨-备货需求
    # player.add_demand("CNFS02-ZZ", "UKBH01", "UKBH01", "UKBH01", [{"sale_sku_code": "53586714577", "num": 5}, {"sale_sku_code": "53586714577", "num": 5}, {"sale_sku_code": "BP53586714577B02", "num": 10}])     #中转仓需求使用
    # player.cancel_demand()      #取消调拨需求

    player.create_pick()      #创建拣货单

    player.assign_picker()      #分配拣货人

    player.do_picking(1)     #确认拣货  1：全部拣货   0 部分拣货

    location_code_tp = "KW-RQ-TP-01"
    player.submit_tray_info(1, location_code_tp)     #按需装托 1：全部拣货   0 部分拣货
    # player.move_storage()       #不成套移出

    player.finish_picking(location_code_tp)     #创建出库单

    # player.change_order()       #调拨出库-改单

    player.review_submit()      #调拨复核

    player.delivery_confirm()       #调拨发货
    """

    """--------调拨入库--------"""

    # """
    box_in_info = player.search_box_in("DBJJ2204090001")  # 获取箱号相关信息
    player.transfer_in_confirm(box_in_info.get("handoverNo"))  # 调拨收货
    player.transfer_in_receive_all(box_in_info.get("boxNo"), "KW-SJQ-01")  # 整箱上架
    player.transfer_in_receive_one(self.box_info.get("boxNo"))  # 逐渐上架
    # """
