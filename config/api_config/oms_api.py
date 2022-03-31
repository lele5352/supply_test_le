oms_api_config = {
    "get_warehouses_list": {
        "uri_path": "/api/ec-oms-api/base/getWarehouseList",
        "method": "get",
        "data": {
            "t": "",
        }
    },
    "list_product": {
        "uri_path": "/api/ec-oms-api/salesorder/listProduct?current=1&size=99",
        "method": "get",
        "data": {
            "type": 1,
            "skuCode": "",
            "t": "",
        }
    },
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
            "remark": "自动化创建需求自动化创建需求自动化创建需求",
            "details": []
        }
    },

}
