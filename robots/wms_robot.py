from robots.robot import AppRobot, ServiceRobot
from tools.log_operator import logger as log
from config.api_config.wms_api_config import BaseApiConfig, TransferApiConfig, OtherEntryOrderApiConfig


class WmsAppRobot(AppRobot):

    def __init__(self):
        # self.dbo = WMSDBOperator
        super().__init__()

    def get_wareskucode_info(self, sku_code):
        """
        获取仓库sku信息详情
        @return:
        """
        OtherEntryOrderApiConfig.GetByWareSkuCode.data.update({"warehouseSkuCode": sku_code})
        info = OtherEntryOrderApiConfig.GetByWareSkuCode.get_attributes()
        res = self.call_api(**info)
        if res.get("code") == 200:
            log.info(res)
            return res.get("data")
        else:
            log.error(res)

    def get_warehouses_list(self):
        """
        获取仓库列表
        :return:
        """
        BaseApiConfig.GetWarehousesList.data.update({"t": self.time_tamp()})
        info = BaseApiConfig.GetWarehousesList.get_attributes()
        res = self.call_api(**info)
        if res.get("code") == 200:
            log.info(res)
            return res.get("data")
        else:
            log.error(res)
            return

    def get_warehouse_info(self, warehouse_code):
        """
        通过code获取仓库相关信息
        :param warehouse_code: 仓库code
        :return: 仓库信息，包含：{"id": xxx, "warehouse_id":xxx, "warehouse_name":xxx, "warehouse_code":xxx}
        """
        warehouses_list = self.get_warehouses_list()
        warehouse_info = {}
        for i in warehouses_list:
            if warehouse_code == i["ext"]["warehouseCode"]:
                warehouse_info = {
                    "warehouseId": i["ext"]["warehouseId"],
                    "warehouseName": i["ext"]["warehouseName"],
                    "warehouseCode": i["ext"]["warehouseCode"],
                    "id": i["id"]
                }
        if warehouse_info:
            return warehouse_info
        else:
            return None

    def switch_warehouse(self, warehouse_code):
        """
        切换仓库
        :param warehouse_code: 仓库code
        :return:
        """
        warehouse_info = self.get_warehouse_info(warehouse_code)
        BaseApiConfig.SwitchWarehouse.data.update({"dataPermId": warehouse_info.get("id")})
        info = BaseApiConfig.SwitchWarehouse.get_attributes()
        res = self.call_api(**info)
        if res.get("code") == 200:
            log.info(res)
            print("切换到「{0}」仓库成功".format(warehouse_code))
            return res
        else:
            log.error(res)
            return

    def other_add_skuinfo_page(self, skucode):
        """
        其他入库时所需sku信息相关参数
        :param skucode: 仓库sku
        :return:
        """
        OtherEntryOrderApiConfig.OtherAddSkuInfoPage.data.update({"skuCodeLike": skucode})
        info = OtherEntryOrderApiConfig.OtherAddSkuInfoPage.get_attributes()
        res = self.call_api(**info)
        return res.get("data").get("records")

    def entryorder(self, sku_code, bom_version, num, operation_flag=1):
        """
        新增其他入库单
        :param sku_code: 仓库sku
        :param bom_version: BOM版本
        :param num: 入库套数
        :param operation_flag: 其他入库单状态：1已提交  0暂存，默认值为：1
        :return: 字典类型的入库单信息，包含：{"entryorderId" : xxx,"entryorderCode": xxx}
        """
        sku_info = self.other_add_skuinfo_page(sku_code)
        sku_list = []
        for i in sku_info:
            if i.get("bomVersion") in bom_version:
                sku_list.append(i)
        for i in sku_list:
            del i["sort"]
            del i["volume"]
            # 获取sku详情，然后拿到bom比例来决定入库数量
            res = self.get_wareskucode_info(i.get("skuCode"))
            bom_num = res.get("bomDetailList")[0].get("skuNum")
            i.update({"planSkuQty": (bom_num * num)})
            i["warehouseSkuCode"] = i.pop("skuCode")
            i["warehouseSkuName"] = i.pop("skuName")
            i["saleSkuCode"] = i.pop("saleSku")
            i["saleSkuName"] = i.pop("skuZhName")
            i["saleSkuImg"] = i.pop("skuImageUrl")
            i["warehouseSkuWeight"] = i.pop("weight")
        OtherEntryOrderApiConfig.OtherEntryOrder.data.update(
            {"skuInfoList": sku_list, "eta": self.time_tamp(),
             "timestamp": self.time_tamp(),
             "operationFlag": operation_flag})
        info = OtherEntryOrderApiConfig.OtherEntryOrder.get_attributes()
        res = self.call_api(**info)
        if res.get("code") == 200:
            log.info(res)
            return res.get("data")
        else:
            log.error(res)
            return

    def get_sku_info_by_entryCode(self, entryorder_info):
        """
        获取入库单内sku相关信息
        :param entryorder_info: 入库单相关信息，包含：entryorderId、entryorderCode
        :return: 入库单内的sku列表信息
        """
        OtherEntryOrderApiConfig.GetSkuInfoByEntryCode.data.update(entryorder_info)
        info = OtherEntryOrderApiConfig.GetSkuInfoByEntryCode.get_attributes()
        res = self.call_api(**info)
        if res.get("code") == 200:
            log.info(res)
            entryorder_sku_list = res.get("data")["records"]
            return entryorder_sku_list
        else:
            log.error(res)
            return

    def get_entry_order_by_id(self, entry_order_id):
        """
        获取其他入库单相关信息
        :param entry_order_id: 入库单id -> str
        :return: 入库单相关单据信息
        """
        uri_path_prefix = OtherEntryOrderApiConfig.GetEntryOrderById.uri_path + entry_order_id
        OtherEntryOrderApiConfig.GetEntryOrderById.uri_path = uri_path_prefix
        OtherEntryOrderApiConfig.GetEntryOrderById.data.update({"t": self.time_tamp()})
        info = OtherEntryOrderApiConfig.GetEntryOrderById.get_attributes()
        res = self.call_api(**info)

        if res.get("code") == 200:
            log.info(res)
            return res.get("data")
        else:
            log.error(res)
            return

    def put_on_the_shelf(self, shelves_location_code, skuqty, entryo_order_id, entryorder_sku_list):
        """
        其他入库上架
        :param shelves_location_code: 上架库位code
        :param skuqty: 上架数量
        :param entryo_order_id: 其他入库单id
        :param skulist: 上架的sku列表
        :return:
        """
        sku_list = []
        for i in entryorder_sku_list:
            x = {
                "shelvesLocationCode": shelves_location_code,
                "skuQty": skuqty * (int(i["warehouseSkuLabel"][-1])),
                "skuCode": i["warehouseSkuCode"],
                "abnormalQty": 0
            }
            sku_list.append(x)
        OtherEntryOrderApiConfig.PutOnTheShelf.data.update({"entryOrderId": entryo_order_id, "skuList": sku_list})
        info = OtherEntryOrderApiConfig.PutOnTheShelf.get_attributes()
        res = self.call_api(**info)
        if res.get("code") == 200:
            log.info(res)
            return res.get("message")
        else:
            log.error(res)
            return

    """按需调拨"""

    # 调拨需求查询，获取调拨需求相关数据
    def demand_list(self, states=None, receive_warehouse_code=None, demand_code_list=None, goods_sku_code_list=None,
                    start_create_time=None, end_create_time=None, source_code_list=None, customer_type=None,
                    create_user_id=None, demand_type=None, cancel_flag=None, sale_order_codes=None):
        """
        调拨需求列表页查询

        @param states: 状态
        @param receive_warehouse_code: 收货仓编码
        @param demand_code_list: 需求list
        @param goods_sku_code_list: 销售skulist
        @param start_create_time: 创建开始时间
        @param end_create_time:   创建结束时间
        @param source_code_list:  OMS订单
        @param customer_type:    客户类型： 1-普通客户，2-大客户
        @param create_user_id:    创建人
        @param demand_type:  需求类型：1-缺货，2-备货
        @param cancel_flag: 取消状态：1-是，2-否
        @param sale_order_codes:  销售订单
        @return:
        """

        TransferApiConfig.TransferDemandList.data.update(
            {
                "states": states,
                "receiveWarehouseCode": receive_warehouse_code,
                "demandCodeList": demand_code_list,
                "goodsSkuCodeList": goods_sku_code_list,
                "startCreateTime": start_create_time,
                "endCreateTime": end_create_time,
                "sourceCodeList": source_code_list,
                "customerType": customer_type,
                "createUserId": create_user_id,
                "demandType": demand_type,
                "cancelFlag": cancel_flag,
                "saleOrderCodes": sale_order_codes
            }
        )
        info = TransferApiConfig.TransferDemandList.get_attributes()
        res = self.call_api(**info)

        name = self.demand_list.__name__
        self.respond_result(name, res)

    def demand_info(self, demands):
        if demands:
            demands_info = []
            for i in demands:
                demands_info.append({
                    "id": i.get("id"),
                    "demandCode": i.get("demandCode")
                })
            print("获取调拨需求相关信息:", demands_info)
            return demands_info
        else:
            print("传入需求为空！请检查查询接口：demand_list()返回值")

    def picking_create(self, demandes_info, pick_type=1):
        """
        新增拣货单
        :param demandes_info:
        :param pick_type: 1-纸质单，2-PDA，默认值为：1
        :return:
        """
        demand_code_list = []
        for item in demandes_info:
            demand_code_list.append(str(item.get("demandCode")))

        TransferApiConfig.PickingCreate.data.update({
            "demandCodes": demand_code_list,
            "pickType": pick_type
        })
        info = TransferApiConfig.PickingCreate.get_attributes()
        res = self.call_api(**info)
        if res.get("code") == 200:
            log.info(res)
            print("创建拣货单：", res)
            return res
        else:
            log.error(res)
            return

    def assign_pick_user(self, pick_order_no):
        """
        分配拣货人
        :param pick_order_no: 拣货单号
        :return:
        """
        TransferApiConfig.AssignPickUser.data.update({"pickOrderNos": [pick_order_no]})
        info = TransferApiConfig.PickingCreate.get_attributes()
        res = self.call_api(**info)
        if res.get("code") == 200:
            log.info(res)
            print("分配拣货人：", res)
            return res
        else:
            log.error(res)
            return

    def picking_detail(self, pick_order_no):
        """
        获取拣货单详情（为“确认拣货”参数组装提供数据）
        @param pick_order_no: 拣货单号
        @return:
        """
        url = TransferApiConfig.PickingDetail.uri_path
        TransferApiConfig.PickingDetail.uri_path = url.format(pick_order_no)

        TransferApiConfig.PickingDetail.data.update({"t": self.time_tamp()})
        info = TransferApiConfig.PickingDetail.get_attributes()
        res = self.call_api(**info)
        # 待改善
        picking_info = res.get("data")["details"]
        if res.get("code") == 200:
            log.info(res)
            print("查询拣货单详情：", picking_info)
            return picking_info
        else:
            log.error(res)
            return

    def do_picking(self, pick_order_no, picking_info):
        """
        确认拣货
        @param pick_order_no: 拣货单号
        @param picking_info: 拣货单信息，可由“picking_detail()”函数查询获取
        @return:
        """
        # 修改实实际拣货的数量
        for item1 in picking_info:
            item1.update({
                "realPickQty": item1.get("shouldPickQty")
            })

        TransferApiConfig.DoPicking.data.update({
            "pickOrderNo": pick_order_no,
            "details": picking_info
        })
        info = TransferApiConfig.DoPicking.get_attributes()
        res = self.call_api(**info)
        if res.get("code") == 200:
            log.info(res)
            print("确认拣货：", res)
            return res
        else:
            log.error(res)
            return

    def search_box_out_list(self, **kwargs):
        """
        查询调拨出库-箱单信息
        :param kwargs:
        :return:
        """
        TransferApiConfig.SearchBoxOutList.data.update({
            "boxNos": kwargs.get("boxNos"),
            "storageLocationCodes": kwargs.get("storageLocationCodes"),
            "transferOutNos": kwargs.get("transferOutNos"),
            "state": kwargs.get("state"),
            "receiveWarehouseCode": kwargs.get("receiveWarehouseCode"),
            "createUsername": kwargs.get("createUsername"),
            "startCreateTime": kwargs.get("startCreateTime"),
            "endCreateTime": kwargs.get("endCreateTime"),
            "startUpdateTime": kwargs.get("startUpdateTime"),
            "endUpdateTime": kwargs.get("endUpdateTime"),
            "saleSkuCodes": kwargs.get("saleSkuCodes"),
            "waresSkuCodes": kwargs.get("waresSkuCodes")
        })
        info = TransferApiConfig.SearchBoxOutList.get_attributes()
        res = self.call_api(**info)
        if res.get("code") == 200:
            log.info(res)
            print("查询调拨出库-箱单：", res)
            return res
        else:
            log.error(res)
            return

    def search_box_in_list(self, **kwargs):
        """
        PC-查询调拨入库-箱单相关信息
        :param kwargs: category：
        :return:
        """
        TransferApiConfig.SearchBoxInList.data.update({
            "handoverNo": kwargs.get("handoverNo"),
            "transferInNo": kwargs.get("transferInNo"),
            "inState": kwargs.get("inState"),
            "deliveryWarehouseCode": kwargs.get("deliveryWarehouseCode"),
            "boxNos": kwargs.get("boxNos"),
            "waresSkuCodes": kwargs.get("waresSkuCodes"),
            "startEta": kwargs.get("startEta"),
            "endEta": kwargs.get("endEta"),
            "startCreateTime": kwargs.get("startCreateTime"),
            "endCreateTime": kwargs.get("endCreateTime"),
            "category": kwargs.get("category"),
        })
        info = TransferApiConfig.SearchBoxInList.get_attributes()
        res = self.call_api(**info)
        if res.get("code") == 200:
            log.info(res)
            print("查询调拨入库-箱单：", res)
            return res
        else:
            log.error(res)
            return


class WmsServiceRobot(ServiceRobot):

    def transfer_demand_creat(self, delivery_warehouse_code, delivery_target_warehouse_code, receive_warehouse_code,
                              receive_target_warehouse_code, goods_sku_code, demand_qty, bom_version, demand_type=2):
        """
        新增调拨需求
        @param delivery_warehouse_code:
        @param delivery_target_warehouse_code:
        @param receive_warehouse_code:
        @param receive_target_warehouse_code:
        @param goods_sku_code:
        @param demand_qty:
        @param bom_version:
        @param demand_type:
        @return:
        """
        TransferApiConfig.TransferDemandCreate.data.update({
            "deliveryWarehouseCode": delivery_warehouse_code,
            "deliveryTargetWarehouseCode": delivery_target_warehouse_code,
            "receiveWarehouseCode": receive_warehouse_code,
            "receiveTargetWarehouseCode": receive_target_warehouse_code,
            "goodsSkuCode": goods_sku_code,
            "demandQty": demand_qty,
            "demandType": demand_type,
            "bomVersion": bom_version
        })
        info = TransferApiConfig.TransferDemandCreate.get_attributes()
        res = self.call_api(**info)
        if res.get("code") == 200:
            log.info(res)
            print("新增调拨需求：", res)
            return res
        else:
            log.error(res)
            print("新增调拨需求：", res)
            return

    def transfer_demand_cancel(self, demand_code):
        """
        取消调拨需求
        @param demand_code: 需求编码
        @return:
        """
        TransferApiConfig.TransferDemandCancle.data.update({
            "demandCode": demand_code
        })
        info = TransferApiConfig.TransferDemandCancle.get_attributes()
        res = self.call_api(**info)
        if res.get("code") == 200:
            log.info(res)
            print("取消调拨需求：", res)
            return res
        else:
            log.error(res)
            return


if __name__ == '__main__':
    # sku_code = "53586714577C01"
    # wms =WmsAppRobot()

    # wms = WmsAppRobot().do_picking("123")
    """
    "LELE-BH", "", "LELE-ZF", "LELE-ZF", "HW9493FU49", 2, "A"
    "LELE-BH", "", "LELE-ZF", "LELE-ZF", "HW9493FU49", 2, "C"
    "LELE-BH", "", "LELE-ZF", "LELE-ZF", "HW6526W5Y5", 2, "A"
    """
    wms_ser = WmsServiceRobot("transfer").transfer_demand_creat("LELE-BH", "", "LELE-ZF", "LELE-ZF", "HW6526W5Y5", 10,
                                                                "A")
    # wms_ser = WmsServiceRobot("transfer").transfer_demand_creat("LELE-BH", "", "PPBH", "", "HW6526W5Y5",
    #                                                             2, "A")

    # wms_ser = WmsServiceRobot("transfer").transfer_demand_cancel("XQ2303290008")
    # wms = WmsAppRobot().demand_list(demand_code_list=['XQ2303080010'])
    # wms.get_warehouse_info("UKBH01")
