import random
from config.api_config.wms_api import wms_api_config
from tools.request_operator import RequestOperator
from controller.wms_controller import WmsController
from controller import *


class PdaController(RequestOperator):

    def __init__(self):
        self.prefix = app_prefix
        self.headers = app_headers
        self.wms = WmsController()
        super().__init__(self.prefix, self.headers)

    def pda_picking_detail(self, pick_order_no):
        """
        pda-获取拣货单信息
        :param pick_order_no:
        :return:
        """
        wms_api_config.get("pda_picking_detail")["data"].update({
            "pickOrderNo": pick_order_no
        })
        try:
            res = self.send_request(**wms_api_config.get("pda_picking_detail"))
            print("拣货单详情：", res)
            return res
        except Exception as e:
            raise Exception("err_info:", e)

    def pda_submit_tray_info(self, location_code_list, picking_detail_info):
        """
        按需装托
        :param location_code_list: 装托需要的托盘（当前仅支持一个托盘装托）
        :param picking_detail_info: 拣货单信息，可通过pda_picking_detail()方法获取
        :return:
        """
        if picking_detail_info:
            pick_order_no = picking_detail_info.get("pickOrderNo")
            tray_infos = []  # 装托的sku信息
            data = []  # 接口内参数信息
            # 通过获取拣货单内已拣货sku信息列表数据，拼接按需装托相关参数
            for i in picking_detail_info.get("details"):
                sku_info = {
                    "id": i["id"],
                    "waresSkuCode": i["waresSkuCode"],
                    "waresSkuName": i["waresSkuName"],
                    "goodsSkuCode": i["goodsSkuCode"],
                    "goodsSkuName": i["goodsSkuName"],
                    "skuQty": i["realPickQty"],
                    "batchInfos": [{
                        'skuQty': i["realPickQty"],
                        'batchNo': ''
                    }]
                }
                tray_infos.append(sku_info)
            item = {
                "storageLocationCode": location_code_list[0],
                "pickOrderNo": pick_order_no,
                "trayInfos": tray_infos
            }
            data.append(item)
            wms_api_config.get("pda_submit_tray_info")["data"] = data
            try:
                res = self.send_request(**wms_api_config.get("pda_submit_tray_info"))
                print("按需装托：", res)
                return res
            except Exception as e:
                raise Exception("err_info:", e)
        else:
            print("按需装托：传入的拣货单信息为空，请检查'pda_picking_detail()'函数返回参数")

    def pda_submit_tray_info_many(self, location_code_list, picking_detail_info):
        """
        按需装托
        :param location_code_list: 装托需要的托盘（支持多个托盘）
        :param picking_detail_info: 拣货单信息，可通过pda_picking_detail()方法获取
        :return:
        """
        # batch_no = ['FH01', 'FH02']
        batch_no = ['FH01']
        if picking_detail_info:
            pick_order_no = picking_detail_info.get("pickOrderNo")
            tray_infos = []  # 装托的sku信息
            # 通过获取拣货单内已拣货sku信息列表数据，拼接按需装托相关参数
            for i in picking_detail_info.get("details"):
                # 将参数按sku数量拆散
                for j in range(i["realPickQty"]):
                    sku_info = {
                        "id": i["id"],
                        "waresSkuCode": i["waresSkuCode"],
                        "waresSkuName": i["waresSkuName"],
                        "goodsSkuCode": i["goodsSkuCode"],
                        "goodsSkuName": i["goodsSkuName"],
                        "skuQty": 1,
                        'batchInfos': [{
                            'skuQty': 1,
                            'batchNo': random.choice(batch_no)
                        }]
                    }
                    # 装托的参数拆散后，追加到某个列表内
                    tray_infos.append(sku_info)
            # 打乱待装托参数的列表，实现后续随机装托
            random.shuffle(tray_infos)
            # 待装托的参数列表，按照传入的装托库位个数打散成不同的子列表，便于后续装托请求参数拼接
            for i in range(0, len(location_code_list)):
                tray_info = tray_infos[i::len(location_code_list)]
                item = {
                    "storageLocationCode": location_code_list[i],
                    "pickOrderNo": pick_order_no,
                    "trayInfos": tray_info
                }
                data = []  # 接口内参数信息
                data.append(item)
                print("按需装托时的请求参数data：", data)
                wms_api_config.get("pda_submit_tray_info")["data"] = data
                try:
                    res = self.send_request(**wms_api_config.get("pda_submit_tray_info"))
                    print("按需装托：「{0}」".format(location_code_list[i]), res)
                except Exception as e:
                    raise Exception("err_info:", e)
        else:
            print("按需装托：传入的拣货单信息为空，请检查'pda_picking_detail()'函数返回参数")

    def pda_move_storage(self):
        """
        不成套移出
        :return:
        """
        pass

    def pda_finish_picking(self, pick_order_no, location_code):
        """
        创建调拨出库单
        @param pick_order_no:
        @param location_code:
        @return:
        """
        wms_api_config.get("pda_finish_picking")["data"].update({
            "pickOrderNo": pick_order_no,
            "storageLocationCodes": location_code
        })
        try:
            res = self.send_request(**wms_api_config.get("pda_finish_picking"))
            print("创建出库单结果：", res)  # 创建出库单结果： {'code': 200, 'message': '操作成功', 'data': 'DC2204120031'}
            return res
        except Exception as e:
            raise Exception("err_info:", e)

    def pda_review_submit(self, box_no, location_code):
        """
        调拨复核
        @param box_no:
        @param location_code_list:
        @return:
        """
        wms_api_config.get("pda_review_submit")["data"].update({
            "boxNo": box_no,
            "storageLocationCode": location_code
        })
        try:
            res = self.send_request(**wms_api_config.get("pda_review_submit"))
            print("调拨复核结果：「{0}」".format(location_code), res)
            return res
        except Exception as e:
            raise Exception("err_info:", e)

    def pda_split_order(self):
        pass

    def pda_change_order(self):
        pass

    def pda_delete_order(self):
        pass

    def pda_handover_bind(self, box_no):
        """
        调拨发货-扫码箱单，生成交接单
        @param box_no:
        @return:
        """
        wms_api_config.get("pda_handover_bind")["data"].update({
            "boxNo": box_no,
        })
        try:
            res = self.send_request(**wms_api_config.get("pda_handover_bind"))
            print("调拨发货-扫码箱单，生成交接单：", res)
            return res
        except Exception as e:
            raise Exception("err_info:", e)

    def pda_logistics_update(self, ids: list, express_type: int = 2):
        """
        调拨发货-交接单-维护物流
        @param ids:交接单id列表
        @param express_type: 运输方式：1-海运，2-空运， 3-陆运， 4-铁运， 5-快递
        @return:
        """
        wms_api_config.get("pda_logistics_update")["data"].update({
            "ids": ids,
            "expressType": express_type
        })
        try:
            res = self.send_request(**wms_api_config.get("pda_logistics_update"))
            print("调拨发货-交接单-维护物流：", res)
            return res
        except Exception as e:
            raise Exception("err_info:", e)

    def pda_delivery_confirm(self, hand_over_no: str):
        """
        调拨发货
        @return:
        """
        wms_api_config.get("pda_delivery_confirm")["data"].update({
            "handoverNo": hand_over_no,
        })
        try:
            res = self.send_request(**wms_api_config.get("pda_delivery_confirm"))
            print("调拨发货结果：", res)
            return res
        except Exception as e:
            raise Exception("err_info:", e)

    def pda_transfer_in_confirm(self, hand_over_no):
        """
        调拨入库-确认收货
        @param hand_over_no:
        @return:
        """
        wms_api_config.get("pda_transfer_in_confirm")["data"].update({
            "handoverNo": hand_over_no,
        })
        try:
            res = self.send_request(**wms_api_config.get("pda_transfer_in_confirm"))
            print("调拨入库-确认收货结果：", res)
            return res
        except Exception as e:
            raise Exception("err_info:", e)

    def pda_transfer_in_receive_all(self, box_no, storage_location_code, transfer_in_no):
        """
        调拨入库-整箱上架
        @param box_no: 箱单号
        @param storage_location_code: 收货库位
        @param transfer_in_no: 调拨入库单号
        @return:
        """
        wms_api_config.get("pda_transfer_in_receive_all")["data"].update({
            "boxNo": box_no,
            "storageLocationCode": storage_location_code,
            "transferInNo": transfer_in_no
        })
        try:
            res = self.send_request(**wms_api_config.get("pda_transfer_in_receive_all"))
            print("调拨入库-整箱上架结果：", res)
            return res
        except Exception as e:
            raise Exception("err_info:", e)

    def pda_transfer_in_box_scan(self, box_no, type=2):
        """
        调拨入库-逐渐上架-扫描箱单后详情页信息
        @param box_no:
        @param type:
        @return:
        """
        wms_api_config.get("pda_transfer_in_box_scan")["data"].update({
            "boxNo": box_no,
            "type": type
        })
        try:
            res = self.send_request(**wms_api_config.get("pda_transfer_in_box_scan"))
            print("调拨入库-扫描箱单后详情页信息：", res)
            return res
        except Exception as e:
            raise Exception("err_info:", e)

    def pda_transfer_in_receive_one(self, info):
        """
        调拨入库-逐渐上架
        @param info:
        @return:
        """

        wms_api_config.get("pda_transfer_in_receive_one")["data"].update(info)
        try:
            res = self.send_request(**wms_api_config.get("pda_transfer_in_receive_one"))
            print("调拨入库-逐渐上架：", res)
            return res
        except Exception as e:
            raise Exception("err_info:", e)


if __name__ == '__main__':
    pda = PdaController()
    """
    box_no = 'DC2210210012-1'
    sj_kw = ["KW-SJQ-01"]
    info = pda.pda_transfer_in_box_scan(box_no).get("data")
    box_info_prefix = {
        "boxNo": info.get("boxNo"),
        "transferInNo": info.get("transferInNo"),
        "storageLocationCode": sj_kw[0]
    }
    box_info_prefix = {
        ""
    }
    for i in info.get("details"):
        pass
    "从这里继续"

    print(info)
    """
    """
    # pda.wms.switch_warehouse("UKBH01")
    pick_order_no = "DJH2210210005"
    info = pda.pda_picking_detail(pick_order_no)

    picking_detail_info = info.get("data")
    location_code_list = ["KW-RQ-TP-01", "KW-RQ-TP-02", "KW-RQ-TP-03"]
    # location_code = "KW-RQ-TP-01"
    # 按需装托
    # pda.pda_submit_tray_info(location_code_list, picking_detail_info)
    pda.pda_submit_tray_info_many(location_code_list, picking_detail_info)

    
    # 创建调拨出库单
    pda.pda_finish_picking(pick_order_no, location_code_list)


    # 获取调拨出库-箱单相关信息
    kw = {
        "transferOutNos": ['DC2210190002'],
    }
    res = pda.wms.search_box_out_list(**kw)
    out_box_no_list = res.get("data")["records"]
    # 调拨复核
    for i in out_box_no_list:
        pda.pda_review_submit(i.get("boxNo"), i.get("storageLocationCode"))
    # 调拨发货交接
    for i in out_box_no_list:
        res = pda.pda_handover_bind(i.get("boxNo"))
    # 调拨发货
    handover_no = res.get("data")["handoverNo"]
    # handover_no = "DBJJ2204120030"
    pda.pda_delivery_confirm(handover_no)


    # 调拨收货--整箱
    pda.pda_transfer_in_confirm(handover_no)
    kw_box_in = {
        "handoverNo": handover_no,
    }
    res = pda.wms.search_box_in_list(**kw_box_in)
    box_no_info = res.get("data")["records"]
    storage_location_code_list = ["KW-SJQ-01"]
    for i in box_no_info:
        pda.pda_transfer_in_receive_all(i.get("boxNo"), storage_location_code_list[0], i.get("transferInNo"))
    """

    # box_no = "DC2204120030-1"
    # pda.pda_review_submit(box_no, location_code)
    # pda.pda_handover_bind(box_no)
    pda.wms.switch_warehouse("0517-3")
    handover_no = "CJJJ2307070001"
    # pda.pda_delivery_confirm(handover_no)     #发货
    # pda.pda_transfer_in_confirm(handover_no)    #收货

    data = {
        "boxNo": "CJDC2307070001-1",
        "storageLocationCode": "KW-SJQ-01",
        "transferInNo": "CJDR2307070001",
        "details": [{
            "waresSkuCode": "53586714577B01",
            "quantity": 2
        }]
    }
    pda.pda_transfer_in_receive_one(data)
