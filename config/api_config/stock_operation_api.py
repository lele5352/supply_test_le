stock_opeartion_config = {
    # 通过sku的code获取sku名称
    "get_wares_skuname_by_code": {
        "uri_path": "/api/ec-wms-api/adjustReceipt/getWaresSkuNameByCode?",
        "method": "get",
        "data": {
            "waresSkuCode": "53586714577B01",
            "t": 1645604117257
        }
    },
    # 获取库位库存信息
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
            "auditResult": 2,  # 调整结果：1-通过，2-驳回
            "ids": [],
            "rejectReason": "自动操作自动操作自动操作"
        }
    },
    # 新增盘点单
    "inventory_process_order_create": {
        "uri_path": "/api/ec-wms-api/inventoryProcessOrder/create",
        "method": "post",
        "data": {
            "inventoryProcessLatitude": 0,
            "inventoryProcessRange": 0,
            "inventoryProcessType": 0,
            "locDetails": [
                {
                    "locCode": "KW-SJQ-3150"
                }
            ]
        }
    },
    # 获取盘点单列表数据信息
    "inventory_process_order_page": {
        "uri_path": "/api/ec-wms-api/inventoryProcessOrder/page",
        "method": "post",
        "data":
            {
                "inventoryProcessOrderNoLike": "",
                "states": [
                    0
                ],  # 状态 (0-新建;10-待盘点;20-盘点中;30-已盘点;40-待处理;50-已完成;60-已取消;70-已关闭)
                "inventoryProcessType": "",  # 盘点类型 (0-常规盘点;1-短拣盘点;2-抽盘)
                "stocktakingOrderDimension": "",  # 盘点维度(0-库位;1-SKU)
                "locCodes": [],
                "saleSkuCodes": [],
                "skuCodes": [],
                "skuNameLike": "",
                "createUsername": "",
                "updateUsername": "",
                "createTimeStart": None,
                "createTimeEnd": None,
                "updateTimeStart": None,
                "updateTimeEnd": None,
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
    # 获取盘点任务列表数据信息
    "inventory_process_task_page": {
        "uri_path": "/api/ec-wms-api/inventoryProcessTask/page",
        "method": "post",
        "data":
            {
                "inventoryProcessOrderNoLike": "",  # 盘点单号
                "states": [],  # 盘点状态  0-待盘点，10-盘点中，20-已完成，30-已取消
                "inventoryProcessType": "",
                "inventoryProcessTaskNoLike": "",  # 盘点任务
                "locCodes": [],
                "saleSkuCodes": [],
                "skuCodes": [],
                "skuNameLike": "",
                "createUsername": "",
                "updateUsername": "",
                "createTimeStart": None,
                "createTimeEnd": None,
                "updateTimeStart": None,
                "updateTimeEnd": None,
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
    # 生成盘点任务
    "inventory_process_order_generate_task": {
        "uri_path": "/api/ec-wms-api/inventoryProcessOrder/generateTask",
        "method": "post",
        "data":
            {
                "inventoryProcessOrderNo": "PD2301310012",
                "operationMode": 1,
                "maxQty": 1
            }
    },
    # 分配人员
    "inventory_process_assign": {
        "uri_path": "/api/ec-wms-api/inventoryProcessTask/assign",
        "method": "post",
        "data":
            {
                "inventoryProcessTaskNo": [
                    "PD2301310003_T1-1"
                ],
                "inventoryProcessUserId": 308,
                "inventoryProcessUsername": "黄乐乐",
                "source": 1
            }
    },

    # 打印
    "inventory_process_print": {
        "uri_path": "/api/ec-wms-api/inventoryProcessTask/print?",
        "method": "get",
        "data":
            {
                "inventoryProcessTaskNo": "PD2301310003_T1",
                "t": 1675135653934
            }
    },
    # 打印次数
    "inventory_process_printTimes": {
        "uri_path": "/api/ec-wms-api/inventoryProcessTask/printTimes?",
        "method": "get",
        "data":
            {
                "inventoryProcessTaskNo": "PD2301310003_T1",
                "t": 1675135653934
            }
    },
    # 获取盘点任务单详情页
    "inventory_process_task_detailPage": {
        "uri_path": "/api/ec-wms-api/inventoryProcessTask/detailPage",
        "method": "post",
        "data": {
            "inventoryProcessTaskId": "1905",
            "size": 10000,
            "current": 1
        }
    },
    # 盘点任务录入--提交
    "inventory_process_commit": {
        "uri_path": "/api/ec-wms-api/inventoryProcess/commit",
        "method": "post",
        "data": {
            "inventoryProcessTaskNo": "PD2301160033_T1-1",
            "commitDetails": [{
                "skuCode": "28265130025A01",
                "locCode": "KW-SJQ-3000",
                "inventoryProcessTaskNo": "PD2301160033_T1-1",
                "inventoryProcessTaskDetailId": 4609,
                "inventoryProcessQty": 3,
                "inventoryStartQty": 3
            }, {
                "skuCode": "J020053-11A01",
                "locCode": "KW-SJQ-3000",
                "inventoryProcessTaskNo": "PD2301160033_T1-1",
                "inventoryProcessTaskDetailId": 4610,
                "inventoryProcessQty": 7,
                "inventoryStartQty": 7
            }]
        }
    }

}
