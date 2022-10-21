stock_opeartion_config = {
    "get_wares_skuname_by_code": {
        "uri_path": "/api/ec-wms-api/adjustReceipt/getWaresSkuNameByCode?",
        "method": "get",
        "data": {
            "waresSkuCode": "53586714577B01",
            "t": 1645604117257
        }
    },
    "get_storage_location_info": {
        "uri_path": "/api/ec-wms-api/adjustReceipt/getStorageLocationInfo?",
        "method": "get",
        "data": {
            "waresSkuCode": "53586714577B01",
            "storageLocationCode": "KW-SJQ-01",
            "t": 1645604117257
        }
    },
    "adjust_receipt": {
        "uri_path": "/api/ec-wms-api/adjustReceipt",
        "method": "post",
        "data": [
            {
                "waresSkuCode": "53586714577B01",
                "storageLocationCode": "KW-SJQ-01",
                "adjustReason": 2,
                "changeCount": "1",
                "changeType": 2,
                "remark": "",
                "waresSkuName": "部件1 1/2 X1"
            }
        ]
    },
    "adjust_receipt_page": {
        "uri_path": "/api/ec-wms-api/adjustReceipt/page",
        "method": "post",
        "data": {
            "waresSkuCode": "",
            "storageLocationCode": "",
            "adjustReceiptCode": "",
            "status": 1,  # 状态：null-全部，1-待审核，2-已审核，3-已驳回
            "changeType": 0,  # 变动类型 0-全部，1-盘亏，2-盘盈
            "source": 1,  # 来源：0-全部，1-人工创建，2-短拣异常
            "adjustReason": "",
            "sortField": [
                {
                    "field": "create_time",
                    "type": "DESC"
                }
            ],
            "size": 10,
            "current": 1
        }
    },
    "adjust_receipt_batch_audit": {
        "uri_path": "/api/ec-wms-api/adjustReceipt/batchAudit",
        "method": "post",
        "data": {
            "auditResult": 2, #调整结果：1-通过，2-驳回
            "ids": [

            ],
            "rejectReason": "自动操作自动操作自动操作"
        }
    },
}
