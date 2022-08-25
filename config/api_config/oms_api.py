oms_api_config = {
    # 获取仓库列表
    "get_warehouses_list": {
        "uri_path": "/api/ec-oms-api/base/actual/getWarehouseList",
        "method": "get",
        "data": {
            "t": "",
        }
    },

    # 新增调拨需求时，查询sku相关信息
    "list_product": {
        "uri_path": "/api/ec-oms-api/salesorder/listProduct?current=1&size=99",
        "method": "get",
        "data": {
            "type": 1,
            "skuCode": "",
            "t": "",
        }
    },
    # 新增调拨需求
    "demand_create": {
        "uri_path": "/api/ec-oms-api/demand/create",
        "method": "post",
        "data": {
            "deliveryWarehouseId": " ",
            "deliveryWarehouseName": " ",
            "deliveryWarehouseCode": " ",
            "deliveryTargetWarehouseId": " ",
            "deliveryTargetWarehouseName": " ",
            "deliveryTargetWarehouseCode": " ",
            "receiveWarehouseId": " ",
            "receiveWarehouseName": " ",
            "receiveWarehouseCode": " ",
            "receiveTargetWarehouseName": " ",
            "receiveTargetWarehouseCode": " ",
            "receiveTargetWarehouseId": " ",
            "remark": "",
            "details": []
        }
    },

    # 查询新增的调拨需求
    "demand_page": {
        "uri_path": "/api/ec-oms-api/demand/page",
        "method": "post",
        "data": {
          "current": 1,
          "size": 10,
          "demandStatus": [],
          "deliveryWarehouseCodes": [],
          "receiveWarehouseCodes": [],
          "demandType": [],
          "transferStatus": [],
          "purchaseStatus": [],
          "externDemandNos": [],
          "linkNos": [],
          "itemSkuCodes": [],
          "remark": "",
          "createTimeStart": "",
          "createTimeEnd": "",
          "cancelTimeStart": "",
          "cancelTimeEnd": ""
        }
    },

    # 取消调拨需求
    "cancel_demand": {
        "uri_path": "/api/ec-oms-api/demand/cancel",
        "method": "post",
        "data": {
            "id": ""
        }
    },

}
