wms_api_config = {
    "get_warehouses_list": {
        "uri_path": "/api/ec-wms-api/data/permission/user/list?t=1645604117257",
        "method": "get",
        "data": {
            "t": 1645604117257,
        }
    },

    "switch_warehouse": {
        "uri_path": "/api/ec-wms-api/data/permission/switchdefault",
        "method": "put",
        "data": {"dataPermId": 1}
    },

    "other_add_skuinfo_page": {
        "uri_path": "/api/ec-wms-api/entryorder/addSkuInfoPage",
        "method": "post",
        "data": {
            "skuCode": None,
            "skuCodeLike": "53586714577",
            "skuName": None,
            "saleSkuCode": None,
            "saleSkuCodeLike": None,
            "size": 10,
            "current": 1
        },
    },

    "entryorder": {
        "uri_path": "/api/ec-wms-api/entryorder",
        "method": "post",
        "data": {
            "entryOrderId":None,
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

    "get_sku_info_by_entryCode": {
        "uri_path": "/api/ec-wms-api/entryorder/getSkuInfoByEntryCode",
        "method": "post",
        "data": {
          "entryOrderCode": "RK2202280011",
          "entryOrderId": 1837,
          "size": 100
        },
    },

    "get_entry_order_by_id": {
        "uri_path": "/api/ec-wms-api/entryorder/getEntryOrderById/",
        "method": "get",
        "data": {
            "t": 1645604117257,
        },
    },

    "put_on_the_shelf": {
        "uri_path": "/api/ec-wms-api/entryorder/putOnTheShelf",
        "method": "post",
        "data": {
            "entryOrderId": 1234,
            "skuList": []
        },
    },
}