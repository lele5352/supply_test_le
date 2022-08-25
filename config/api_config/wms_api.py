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
    #获取sku相关信息
    "get_by_wareSkuCode": {
        "uri_path": "/api/ec-wms-api/sku-search/getByWareSkuCode",
        "method": "get",
        "data": {
            "warehouseSkuCode": None
        },
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
            "size": 99,
            "states": [],
            "receiveWarehouseCode": "",
            "demandCodeList": None,
            "goodsSkuCodeList": None,
            "startCreateTime": "",
            "endCreateTime": "",
            "sourceCodeList": [],
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
        "data": {
            "pickOrderNo": "",
            "details": "",
        }
    },

    # PDA-按需装托时，获取拣货单详情
    "pda_picking_detail": {
        "uri_path": "/api/ec-wms-api/transferOut/picking/demand/detail",
        "method": "get",
        "data": {
            "pickOrderNo": "",
        }
    },

    # PDA-按需装托
    "pda_submit_tray_info": {
        "uri_path": "/api/ec-wms-api/transferOut/pda/submitTrayInfo",
        "method": "post",
        "data": [{
            "storageLocationCode": "",
            "pickOrderNo": "",
            "trayInfos": []
        }]
    },

    # PDA-不成套移出
    "pda_move_storage": {
        "uri_path": "/api/ec-wms-api/transferOut/pda/moveStorage",
        "method": "post",
        "data": {
            "fromStorageLocationCode": "KW-RQ-TP-01",
            "waresSkuCode": "53586714577B01",
            "toStorageLocationCode": "KW-RQ-YK-01",
            "pickOrderNo": ""
        }
    },

    # PDA-创建出库单
    "pda_finish_picking": {
        "uri_path": "/api/ec-wms-api/transferOut/pda/finishPacking",
        "method": "post",
        "data": {
            "pickOrderNo": "",
            "storageLocationCodes": ""
        }
    },

    # 查询调拨出库-箱单
    "search_box_out_list": {
        "uri_path": "/api/ec-wms-api/transferOut/box/list",
        "method": "post",
        "data": {
            "current": 1,
            "size": 99,
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
        },
    },

    # PDA-调拨复核
    "pda_review_submit": {
        "uri_path": "/api/ec-wms-api/transferOut/box/review/submit",
        "method": "post",
        "data": {
            "boxNo": "",
            "storageLocationCode": ""
        }
    },

    # PDA-调拨出库-改单
    "pda_change_order": {
        "uri_path": "/api/ec-wms-api/transferOut/modify/changeOrder",
        "method": "post",
        "data": {
            "transferOutNo": "",
            "changeSkuDetailList": []
        }
    },

    # PDA-调拨发货-扫描箱单
    "pda_handover_bind": {
        "uri_path": "/api/ec-wms-api/transferOut/handover/bind",
        "method": "post",
        "data": {
            "boxNo": "DC2204090001-1",
            "handoverNo": None,
            "receiveWarehouseCode": None
        }
    },

    # PDA-调拨发货-发货
    "pda_delivery_confirm": {
        "uri_path": "/api/ec-wms-api/transferOut/handover/delivery/confirm",
        "method": "post",
        "data": {
            "handoverNo": "",
        }
    },

    # 查询调拨入库-箱单
    "search_box_in_list": {
        "uri_path": "/api/ec-wms-api/transferIn/input/box/page",
        "method": "post",
        "data": {
            "current": 1,
            "size": 99,
            "handoverNo": "",
            "transferInNo": "",
            "inState": "",
            "deliveryWarehouseCode": "",
            "boxNos": [],
            "waresSkuCodes": [],
            "startEta": "",
            "endEta": "",
            "startCreateTime": "",
            "endCreateTime": "",
            "category": None
        },
    },

    # PDA-调拨入库-确认收货
    "pda_transfer_in_confirm": {
        "uri_path": "/api/ec-wms-api/transferIn/handover/received/confirm",
        "method": "post",
        "data": {
            "handoverNo": ""
        }
    },

    # PDA-调拨入库-整箱上架
    "pda_transfer_in_receive_all": {
        "uri_path": "/api/ec-wms-api/transferIn/input/box/shelf",
        "method": "post",
        "data": {
            "boxNo": "",
            "storageLocationCode": "",
            "transferInNo": ""
        }
    },

    # PDA-调拨入库-逐渐上架
    "pda_transfer_in_receive_one": {
        "uri_path": "/api/ec-wms-api/transferIn/input/sku/shelf",
        "method": "post",
        "data": ""
    },

    # 仓间调拨-查询sku信息
    "cj_sku_info_page": {
        "uri_path": "/api/ec-wms-api/otherStockOutOrder/skuInfoPage",
        "method": "post",
        "data": {
            "saleSkuCodes": [],
            "skuName": "",
            "size": 10,
            "current": 1,
            "warehouseLocationCode": "",
            "productState": 1,
            "skuCodes": []
        }
    },

    # 仓间调拨-新增仓间调拨单
    # 返回值：{'code': 200, 'message': '操作成功', 'data': {'instructOrderId': 480, 'instructOrderNo': 'CJDC2204180001', 'pickOrderNo': 'CJJH2204180001'}}
    "cj_create_inner": {
        "uri_path": "/api/ec-wms-api/mutualTransferOut/create/inner",
        "method": "post",
        "data": {
            "t": 1649929488448,
            "receiveWarehouseCode": "",
            "remark": "测试测试",
            "skuItems": []
        }
    },

    # 仓间调拨-调拨出库单分页查询
    "cj_platform_transferout_page": {
        "uri_path": "/api/ec-wms-api/platformTransferOut/page/2",
        "method": "post",
        "data": {
            "platformTransferOutCodeList": [],
            "skuCodeList": [],
            "saleSkuCodeList": [],
            "inState": None, #接收列表类型数据 [0,1,2,3]
            "receiveWarehouseId": None,
            "boxOrderNos": [],
            "pickOrderNos": [],
            "wmsStates": [],
            "deliveryUserId": "",
            "createUserId": None,
            "size": 10,
            "current": 1
        }
    },

    # 仓间调拨-调拨出库单详情页（确认拣货时也用此接口）
    "cj_detail_page": {
        "uri_path": "/api/ec-wms-api/mutualTransferOut/detailPage/{0}",
        "method": "get",
        "data": {
            "t": 1649929488448
        }
    },

    # 仓间调拨-确认拣货
    "cj_confirmPick": {
        "uri_path": "/api/ec-wms-api/mutualTransferOut/confirmPick",
        "method": "post",
        "data": {
            "pickOrderId": None,
            "pickOrderNo": "",
            "pickItems": []
        }
    },

    # 仓间调拨-确认拣货
    "cj_deliver_inner": {
        "uri_path": "/api/ec-wms-api/mutualTransferOut/deliver/inner",
        "method": "post",
        "data": {
            "instructOrderId": 1,
        }
    },
}
