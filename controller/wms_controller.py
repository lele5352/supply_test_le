from tools.request_operator import RequestOperator
from tools.mysql_operator import MySqlOperator
from config.sys_config import env_config
from controller.ums_controller import UmsController
from config.api_config.wms_api import wms_api_config
from tools.log_operator import logger as log
import time

class WmsController(RequestOperator):

    def __init__(self, ums):
        self.prefix = env_config.get("web_prefix")
        self.headers = ums.header
        super().__init__(self.prefix, self.headers)

        # self.db = MySqlOperator(**env_config.get("mysql_info_ims"))

    def get_wareskucode_info(self, sku_code):
        """
        获取仓库sku信息详情
        @return:
        """
        wms_api_config.get("get_by_wareSkuCode")["data"].update({"warehouseSkuCode": sku_code})
        res = self.send_request(**wms_api_config.get("get_by_wareSkuCode"))
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
        wms_api_config.get("get_warehouses_list")["data"].update({
            "t": self.time_tamp
        })
        res = self.send_request(**wms_api_config.get("get_warehouses_list"))
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
        for i in warehouses_list:
            if warehouse_code == i["ext"]["warehouseCode"]:
                warehouse_info = {
                    "warehouseId": i["ext"]["warehouseId"],
                    "warehouseName": i["ext"]["warehouseName"],
                    "warehouseCode": i["ext"]["warehouseCode"],
                    "id": i["id"]
                }
        return warehouse_info


    def switch_warehouse(self, warehouse_code):
        """
        切换仓库
        :param warehouse_code: 仓库code
        :return:
        """
        warehouse_info = self.get_warehouse_info(warehouse_code)
        wms_api_config.get("switch_warehouse")["data"].update({"dataPermId": warehouse_info.get("id")})

        res = self.send_request(**wms_api_config.get("switch_warehouse"))
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
        wms_api_config.get("other_add_skuinfo_page")["data"].update({"skuCodeLike": skucode})
        res = self.send_request(**wms_api_config.get("other_add_skuinfo_page"))
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
            #获取sku详情，然后拿到bom比例来决定入库数量
            res = self.get_wareskucode_info(i.get("skuCode"))
            bom_num = res.get("bomDetailList")[0].get("skuNum")
            i.update({"planSkuQty": (bom_num * num)})
            i["warehouseSkuCode"] = i.pop("skuCode")
            i["warehouseSkuName"] = i.pop("skuName")
            i["saleSkuCode"] = i.pop("saleSku")
            i["saleSkuName"] = i.pop("skuZhName")
            i["saleSkuImg"] = i.pop("skuImageUrl")
            i["warehouseSkuWeight"] = i.pop("weight")

        timestamp = int(time.time()) * 1000
        wms_api_config.get("entryorder")["data"].update({"skuInfoList": sku_list, "eta": timestamp, "timestamp": timestamp, "operationFlag": operation_flag})
        res = self.send_request(**wms_api_config.get("entryorder"))
        if res.get("code") == 200:
            log.info(res)
            entryorder_info = res.get("data")
            return entryorder_info
        else:
            log.error(res)
            return


    def get_sku_info_by_entryCode(self, entryorder_info):
        """
        获取入库单内sku相关信息
        :param entryorder_info: 入库单相关信息，包含：entryorderId、entryorderCode
        :return: 入库单内的sku列表信息
        """
        wms_api_config.get("get_sku_info_by_entryCode")["data"].update(entryorder_info)
        res = self.send_request(**wms_api_config.get("get_sku_info_by_entryCode"))
        if res.get("code") == 200:
            log.info(res)
            entryorder_sku_list = res.get("data")["records"]
            return entryorder_sku_list
        else:
            log.error(res)
            return


    def get_entry_order_by_id(self, entryo_order_id):
        """
        获取其他入库单相关信息
        :param entryo_order_id: 入库单id
        :return: 入库单相关单据信息
        """
        timestamp = int(time.time()) * 1000
        uri_path_prefix = wms_api_config.get("get_entry_order_by_id")["uri_path"]
        wms_api_config.get("get_entry_order_by_id")["data"].update({"t": timestamp})
        wms_api_config.get("get_entry_order_by_id")["uri_path"] = uri_path_prefix + entryo_order_id
        res = self.send_request(**wms_api_config.get("get_entry_order_by_id"))
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
        wms_api_config.get("put_on_the_shelf")["data"].update({"entryOrderId": entryo_order_id, "skuList": sku_list})
        res = self.send_request(**wms_api_config.get("put_on_the_shelf"))
        if res.get("code") == 200:
            log.info(res)
            return res.get("message")
        else:
            log.error(res)
            return


    def del_wares(self):
        sql_ims_list = [
            "DELETE FROM wares_inventory WHERE goods_sku_code = '53586714577';",
            "DELETE FROM goods_inventory WHERE goods_sku_code = '53586714577' ;",
            "DELETE FROM central_inventory WHERE goods_sku_code = '53586714577';",
        ]

        # sql_wms_list = [
        #     "DELETE FROM trf_transfer_out_order WHERE warehouse_id =536;",
        #     "DELETE FROM trf_transfer_out_order_detail WHERE warehouse_id =536;",
        #     "DELETE FROM trf_transfer_in_order WHERE warehouse_id =517;",
        #     "DELETE FROM trf_transfer_in_order_detail WHERE warehouse_id =536;",
        #     "DELETE FROM trf_box_order WHERE warehouse_id =536;",
        #     "DELETE FROM trf_box_order_detail WHERE warehouse_id =536;",
        #     "DELETE FROM trf_box_order_in WHERE warehouse_id =517;",
        #     "DELETE FROM trf_box_order_detail_in WHERE warehouse_id =536;",
        #     "DELETE FROM trf_handover_order WHERE warehouse_id =536;",
        #     "DELETE FROM trf_transfer_demand WHERE warehouse_id =536;",
        #     "DELETE FROM trf_transfer_pick_order WHERE warehouse_id =536;",
        #     "DELETE FROM trf_transfer_pick_order_detail WHERE warehouse_id = 536;"
        # ]

        # sql = "select * from wares_inventory where goods_sku_code = '53586714577';"
        # data = self.db.get_sql_all(sql)
        for i in sql_ims_list:
            self.db.executemany(i)
        self.db.close()

        print("数据清理完成")

    """按需调拨"""

    #调拨需求查询，获取调拨需求相关数据
    def demand_list(self, **kwargs):
        """
        调拨需求查询，获取调拨
        :param kwargs:
        :return:
        """
        wms_api_config.get("demand_list")["data"].update({
            "states": kwargs.get("states"),
            "receiveWarehouseCode": kwargs.get("receiveWarehouseCode"),
            "demandCodeList": kwargs.get("demandCodeList"),
            "goodsSkuCodeList": kwargs.get("goodsSkuCodeList"),
            "startCreateTime": kwargs.get("startCreateTime"),
            "endCreateTime": kwargs.get("endCreateTime"),
            "sourceCodeList": kwargs.get("sourceCodeList"),
            "customerType": kwargs.get("customerType"),
            "createUserId": kwargs.get("createUserId"),
            "demandType": kwargs.get("demandType"),
            "cancelFlag": kwargs.get("cancelFlag"),
            "saleOrderCodes": kwargs.get("saleOrderCodes")
        })
        res = self.send_request(**wms_api_config.get("demand_list"))
        if res.get("code") == 200:
            log.info(res)
            print("调拨需求查询：", res)
            return res
        else:
            log.error(res)
            return


    # def demand_info(self, demands):
    #     """
    #     获取调拨需求相关信息
    #     @param demands:
    #     @return:
    #     """
    #     if demands:
    #         demands_info = []
    #         for i in demands:
    #             demands_info.append({
    #                 "id": i.get("id"),
    #                 "demandCode": i.get("demandCode")
    #             })
    #         print("获取调拨需求相关信息:", demands_info)
    #         return demands_info
    #     else:
    #         print("传入需求为空！请检查查询接口：demand_list()返回值")

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
        wms_api_config.get("picking_create")["data"].update({
            "demandCodes": demand_code_list,
            "pickType": pick_type
        })
        res = self.send_request(**wms_api_config.get("picking_create"))
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
        wms_api_config.get("assign_pick_user")["data"].update({
            "pickOrderNos": [pick_order_no]
        })
        res = self.send_request(**wms_api_config.get("assign_pick_user"))
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
        wms_api_config.get("picking_detail")["uri_path"] = "/api/ec-wms-api/transferOut/picking/detail/{0}".format(pick_order_no)
        wms_api_config.get("picking_detail")["data"].update({
            "t": self.time_tamp
        })
        res = self.send_request(**wms_api_config.get("picking_detail"))
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
        wms_api_config.get("do_picking")["data"].update({
            "pickOrderNo": pick_order_no,
            "details": picking_info
        })
        res = self.send_request(**wms_api_config.get("do_picking"))
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
        wms_api_config.get("search_box_out_list")["data"].update({
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
        res = self.send_request(**wms_api_config.get("search_box_out_list"))
        if res.get("code") == 200:
            log.info(res)
            print("查询调拨出库-箱单：", res)
            return res
        else:
            log.error(res)
            return


    def search_box_in_list(self, **kwargs):
        """
        查询调拨入库-箱单相关信息
        :param kwargs: category：
        :return:
        """
        wms_api_config.get("search_box_in_list")["data"].update({
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
        res = self.send_request(**wms_api_config.get("search_box_in_list"))
        if res.get("code") == 200:
            log.info(res)
            print("查询调拨入库-箱单：", res)
            return res
        else:
            log.error(res)
            return


    """仓间调拨相关"""
    def cj_sku_info_page(self, sku_code_list):
        """
        仓间调拨：查询调拨的sku信息
        @param sku_code_list:
        @return:
        """
        wms_api_config.get("cj_sku_info_page")["data"].update({
            "skuCodes": sku_code_list
        })
        res = self.send_request(**wms_api_config.get("cj_sku_info_page"))
        if res.get("code") == 200:
            log.info(res)
            print("仓间：sku信息查询：", res)
            return res
        else:
            log.error(res)
            return


    def cj_create_inner(self, receive_warehouse_code, sku_items, remark):
        """
        仓间调拨：新增
        :param receive_warehouse_code: 收货仓库code
        :param sku_code_list: 仓库sku列表
        :return:
        """
        # 更新请求参数内相关字段值
        wms_api_config.get("cj_create_inner")["data"].update({
            "t": self.time_tamp,
            "receiveWarehouseCode": receive_warehouse_code,
            "remark": remark,
            "skuItems": sku_items
        })
        res = self.send_request(**wms_api_config.get("cj_create_inner"))
        if res.get("code") == 200:
            log.info(res)
            print("仓间：新增仓间调拨：", res)
            return res
        # 返回参数示例：{"code":200,"message":"操作成功","data":{"instructOrderId":230,"instructOrderNo":"CJDC2204160001","pickOrderNo":"CJJH2204160001"}}
        else:
            log.error(res)
            return



    def cj_platform_transferout_page(self, **kwargs):
        """
        仓间调拨：调拨出库-列表也查询
        @param kwargs:
        @return:
        """
        wms_api_config.get("cj_platform_transferout_page")["data"].update(**kwargs)
        res = self.send_request(**wms_api_config.get("cj_platform_transferout_page"))
        if res.get("code") == 200:
            log.info(res)
            print("仓间：查询仓间调拨出库页面：", res)
            # 返回参数示例：{"code":200,"message":"操作成功","data":{"records":[{"transferOutId":230,"transferOutCode":"CJDC2204160001"...}}
            return res
        else:
            log.error(res)
            return


    def cj_detail_page(self, pick_order_id):
        uri = wms_api_config.get("cj_detail_page")["uri_path"].format(pick_order_id)
        wms_api_config.get("cj_detail_page").update({
            "uri_path": uri
        })
        res = self.send_request(**wms_api_config.get("cj_detail_page"))
        if res.get("code") == 200:
            log.info(res)
            print("仓间：查看出库单详情页：", res)
            return res
            # 返回参数示例：{"code":200,"message":"操作成功","data":{"records":[{"transferOutId":230,"transferOutCode":"CJDC2204160001"...}}
        else:
            log.error(res)
            return


    def cj_confirmPick(self, pick_order_id, pick_order_no, pick_items):
        wms_api_config.get("cj_confirmPick")["data"].update({
            "pickOrderId": pick_order_id,
            "pickOrderNo": pick_order_no,
            "pickItems": pick_items
        })
        res = self.send_request(**wms_api_config.get("cj_confirmPick"))
        if res.get("code") == 200:
            log.info(res)
            print("仓间：确认拣货：", res)
            # 返回参数示例：{"code":200,"message":"操作成功","data":"CJDC2204160001-1"}
            return res
        else:
            log.error(res)
            return


    def cj_deliver_inner(self, instruct_order_id):
        wms_api_config.get("cj_deliver_inner")["data"].update({
            "instructOrderId": instruct_order_id
        })
        res = self.send_request(**wms_api_config.get("cj_deliver_inner"))
        if res.get("code") == 200:
            log.info(res)
            print("仓间：调拨出库-发货 ：", res)
            # 返回参数示例：{'code': 200, 'message': '操作成功','data': {'handoverOrderNo': 'CJJJ2204180005', 'entryOrderNo': 'CJDR2204180002'}}
            return res
        else:
            log.error(res)
            return


    """库内服务相关"""
    # def stockoperation_adjustReceipt




if __name__ == '__main__':
    ums = UmsController()
    wms = WmsController(ums)
    # wms.get_warehouses_list()
    wms.get_wareskucode_info("71230293819")
    # wms.switch_warehouse("LELE-BH")
    # wms.entryorder("94991138113", ["A"], 2)
    # wms.get_sku_info_by_entryCode(wms.entryorder("53586714577", ["B", "D"], 5))
    # wms.get_entry_order_by_id("1843")
    # wms.del_wares()

    kw = {
        "sourceCodeList": ["DB00000026"]
    }
    # 调拨需求列表查询
    # res = wms.demand_list(**kw)
    # demands_info = res.get("data")["records"]
    # demands_info = wms.demand_info(demands_list)
    # res = wms.picking_create(demands_info)
    # picking_order_no = res.get("data")

    # wms.assign_pick_user("DJH2204120035")
    # picking_info = wms.picking_detail("DJH2204120035")
    # wms.do_picking("DJH2204120035", picking_info)
    kw_box_out = {
        "transferOutNos": ['DC2204120031'],
    }
    # wms.search_box_out_list(**kw_box_out)

    kw_box_in = {
        "handoverNo": "DBJJ2204120030",
    }
    # wms.search_box_in_list(**kw_box_in)

    # 仓间调拨-新增
    sku_info_list = [
        {"sku_code": "53586714577G01", "num": 1},
    ]
    # wms.cj_create_inner("UKBH01", sku_info_list)

    # 仓间调拨-列表查询
    search_cj = {
        "pickOrderNos": ["CJJH2204180002"],
    }
    # wms.cj_platform_transferout_page(**search_cj)
    # 仓间调拨-出库单详情页
    # wms.cj_detail_page(153)
    # 仓间调拨确认拣货
    # wms.cj_confirmPick()

