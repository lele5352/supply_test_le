from config.api_config import ApiConfig


class WmsService:

    class TransferDemandCreate(ApiConfig):
        uri_path = "/transferDemand/create"
        method = "post"
        data = {
            "deliveryWarehouseCode": "UKBH01",
            "deliveryTargetWarehouseCode": "",
            "receiveWarehouseCode": "UKBH02",
            "receiveTargetWarehouseCode": "",
            "userId": 10,
            "username": "黄乐乐",
            "goodsSkuCode": "53586714577",
            "demandQty": 1,
            "customerType": 2,
            "customerRemark": "客戶備注123客戶備注123客戶備注123客戶備注123客戶備注123客戶備注123客戶備注123",
            "sourceCode": "OMS4562456272",
            "saleOrderCodes": ["fdsdfdsf1", "fdsdfdsf2"],
            "demandType": 2,
            "bomVersion": "C"
        }

    class TransferDemandCancle(ApiConfig):
        uri_path = "/transferDemand/cancel"
        method = "post"
        data = {
            "demandCode": "XQ2210190026",
            "cancelUserId": 10,
            "cancelUsername": "黄乐乐"
        }


wms_service_config ={
    # 新增调拨需求
        "transferDemand_create": {
            "uri_path": "/transferDemand/create",
            "method": "post",
            "data": {
                "receiveWarehouseCode": "UKBH02",
                "deliveryWarehouseCode": "UKBH01",
                "userId": 10,
                "username": "黄乐乐",
                "goodsSkuCode": "53586714577",
                "demandQty": 1,
                "customerType": 2,
                "customerRemark": "客戶備注123客戶備注123客戶備注123客戶備注123客戶備注123客戶備注123客戶備注123",
                "sourceCode": "OMS4562456272",
                "saleOrderCodes": ["fdsdfdsf1", "fdsdfdsf2"],
                "demandType": 2,
                "bomVersion": "C"
            }
        },
    # 取消调拨需求
        "transferDemand_cancel": {
            "uri_path": "/transferDemand/cancel",
            "method": "post",
            "data": {
                "demandCode": "XQ2210190026",
                "cancelUserId": 10,
                "cancelUsername": "黄乐乐"
            }
        },
}