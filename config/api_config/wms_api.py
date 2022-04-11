wms_api_config = {
    # 获取全部仓库信息列表
    "get_warehouses_list": {
        "uri_path": "/api/ec-wms-api/data/permission/user/list?t=1645604117257",
        "method": "get",
        "data": {
            "t": 1645604117257,
        }
    },

    # 切换仓库
    "switch_warehouse": {
        "uri_path": "/api/ec-wms-api/data/permission/switchdefault",
        "method": "put",
        "data": {"dataPermId": 1}
    },
    # 其他入添加商品时，查询接口
    "other_add_skuinfo_page": {
        "uri_path": "/api/ec-wms-api/entryorder/addSkuInfoPage",
        "method": "post",
        "data": {
            "skuCode": None,
            "skuCodeLike": "53586714577",
            "skuName": None,
            "saleSkuCode": None,
            "saleSkuCodeLike": None,
            "size": 50,
            "current": 1
        },
    },
    # 其他入库单
    "entryorder": {
        "uri_path": "/api/ec-wms-api/entryorder",
        "method": "post",
        "data": {
            "entryOrderId": None,
            "entryOrderType": 3,
            "eta": 1642403631000,
            "supplierCode": None,
            "fromOrderCode": None,
            "remark": None,
            "qualityType": 0,
            "timestamp": 1642403631000,
            "logisticsInfoList": [],
            "skuInfoList": [],
            "operationFlag": 1
        },
    },
    # 获取其他入库单内sku信息
    "get_sku_info_by_entryCode": {
        "uri_path": "/api/ec-wms-api/entryorder/getSkuInfoByEntryCode",
        "method": "post",
        "data": {
            "entryOrderCode": "RK2202280011",
            "entryOrderId": 1837,
            "size": 100
        },
    },
    # 获取入库单信息
    "get_entry_order_by_id": {
        "uri_path": "/api/ec-wms-api/entryorder/getEntryOrderById/",
        "method": "get",
        "data": {
            "t": 1645604117257,
        },
    },
    # 其他入库-上架
    "put_on_the_shelf": {
        "uri_path": "/api/ec-wms-api/entryorder/putOnTheShelf",
        "method": "post",
        "data": {
            "entryOrderId": 1234,
            "skuList": []
        },
    },
    # 调拨需求列表查询
    "demand_list": {
        "uri_path": "/api/ec-wms-api/transferOut/demand/list",
        "method": "post",
        "data": {
            "current": 1,
            "size": 9999,
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
        },
    },

    # 创建拣货单
    "picking_create": {
        "uri_path": "/api/ec-wms-api/transferOut/picking/create",
        "method": "post",
        "data": {"demandCodes": ["XQ2204080002"], "pickType": 1},
    },

    # 分配拣货人
    "assign_pick_user": {
        "uri_path": "/api/ec-wms-api/transferOut/picking/assignPickUser",
        "method": "post",
        "data": {"pickOrderNos": ["DJH2204080002"], "pickUsername": "黄乐乐", "pickUserId": "10"},
    },

    # 查询拣货单详情
    "picking_detail": {
        "uri_path": "/api/ec-wms-api/transferOut/picking/detail/DJH2204080002",
        "method": "get",
        "data": {"t": "1642684741035"},
    },

    # 确认拣货
    "do_picking": {
        "uri_path": "/api/ec-wms-api/transferOut/picking/doPicking",
        "method": "post",
        "data": {"pickOrderNo": "",
                 "details": "",
                }
    },
}
