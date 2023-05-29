from tools.request_operator import RequestOperator
from controller.ums_controller import UmsController
# from config.sys_config import env_config
from config import env_config

from config.api_config.stock_operation_api import stock_opeartion_config
from tools.log_operator import logger as log
from controller import *

import random
import time


class StockOpearationController(RequestOperator):

    def __init__(self):
        self.prefix = web_prefix
        self.headers = app_headers
        super().__init__(self.prefix, self.headers)

    def get_wares_skuname_by_code(self, skucode):
        """
        查询sku名称
        :param skucode:
        :return: sku的中文名称
        """
        stock_opeartion_config.get("get_wares_skuname_by_code")["data"].update({
            "waresSkuCode": skucode,
            "t": self.time_tamp
        })
        res = self.send_request(**stock_opeartion_config.get("get_wares_skuname_by_code"))
        if res.get("code") == 200:
            log.info("查询sku名称：get_wares_skuname_by_code。", res)
            return res.get("data")
        else:
            log.error(res)
            return

    def get_storage_location_info(self, skucode, storage_location_code):
        """
        获取库位库存信息
        :param skucode: sku编码
        :param storage_location_code: 库位信息
        :return:sku的库位库存信息
        """
        stock_opeartion_config.get("get_wares_skuname_by_code")["data"].update({
            "waresSkuCode": skucode,
            "storageLocationCode": storage_location_code,
            "t": self.time_tamp
        })
        res = self.send_request(**stock_opeartion_config.get("get_storage_location_info"))
        print(res)
        return res.get("data")

    def adjust_receipt(self, adjust_sku_info):
        """
        调整单
        :param adjust_sku_info:
        [
            {
                "waresSkuCode": ,
                "storageLocationCode": ,
                "changeCount": ,#调整单的数量
                "changeType": ,#调整单的类型： 1-盘亏，2-盘盈
                "adjustReason": #调整单的原因： 1-报损，2-库内盘盈，3-库内盘亏，4-供应商弃货，5-商品属性调整，6-拣货短拣异常，7-平台调拨装箱异常
            }
        ]
        :return:
        """
        list_info = []
        for i in adjust_sku_info:
            sku_code = i.get("waresSkuCode")
            adjust_sku = {
                "waresSkuCode": sku_code,
                "storageLocationCode": i.get("storageLocationCode"),
                "adjustReason": i.get("adjustReason"),
                "changeCount": i.get("changeCount"),
                "changeType": i.get("changeType"),
                "remark": "",
                "waresSkuName": self.get_wares_skuname_by_code(sku_code)
            }
            list_info.append(adjust_sku)
        stock_opeartion_config.get("adjust_receipt")["data"] = list_info
        res = self.send_request(**stock_opeartion_config.get("adjust_receipt"))
        print(res)

    def adjust_receipt_page(self, status, change_type, source):
        """
        调整单分页查询
        :param status:  状态：null-全部，1-待审核，2-已审核，3-已驳回
        :param change_type:  变动类型 0-全部，1-盘亏，2-盘盈
        :param source: 来源：0-全部，1-人工创建，2-短拣异常
        :return: 查询结果列表
        """
        stock_opeartion_config.get("adjust_receipt_page")["data"].update({
            "status": status,
            "changeType": change_type,
            "source": source,
        })
        res = self.send_request(**stock_opeartion_config.get("adjust_receipt_page"))
        print(res.get("data")["records"])
        return res.get("data")["records"]

    def adjust_receipt_batch_audit(self, audit_result, ids):
        """
        调整单-审核
        :param audit_result: int 调整结果：1-通过，2-驳回
        :param ids: list 调整单id列表
        :return:
        """
        stock_opeartion_config.get("adjust_receipt_batch_audit")["data"]["ids"] = ids
        stock_opeartion_config.get("adjust_receipt_batch_audit")["data"].update({
            "auditResult": audit_result
        })
        res = self.send_request(**stock_opeartion_config.get("adjust_receipt_batch_audit"))
        print(res.get("message"))

    def inventory_process_order_create(self, **kwargs):
        """
        新增盘点单
        @param kwargs:
        {
          "inventoryProcessType": 盘点类型(0-常规盘点;1-短拣盘点;2-抽盘),
          "inventoryProcessLatitude": 盘点维度(0-库位;1-SKU),
          "inventoryProcessRange": 盘点范围(0-库位;1-库存+SKU),
          "locDetails": [   #盘点单库位详情(盘点纬度是库位时，不能为空)
            {
              "locCode": 库位编码
            }
          ],
          "skuDetails": [   #盘点单SKU详情(盘点纬度是SKU时，不能为空)
            {
              "locCode": 库位编码,
              "skuCode": sku编码
            }
          ]
        }
        @return:
        """
        stock_opeartion_config.get("inventory_process_order_create")["data"].update(
            kwargs
        )
        res = self.send_request(**stock_opeartion_config.get("inventory_process_order_create"))
        print("新增盘点单：", res.get("message"))
        return

    def inventory_process_order_page(self, **kwargs):
        """
        盘点单列表页查询，默认参数查询"新建"状态的单据
        @param kwargs:
        @return:
        """
        stock_opeartion_config.get("inventory_process_order_page")["data"].update(
            kwargs
        )
        res = self.send_request(**stock_opeartion_config.get("inventory_process_order_page"))
        print("盘点单-列表页查询信息：", res.get("data")["records"])
        return res.get("data")["records"]

    def inventory_process_order_generate_task(self, order_no, maxQty, operationMode=1):
        """
        盘点单生成盘点任务单
        @param order_no: 盘点单号
        @param maxQty: 每个任务内最大数量
        @param operationMode: 作业方式  0-PDA操作，1-纸质单
        @return:
        """
        para = {
            "inventoryProcessOrderNo": order_no,
            "operationMode": maxQty,
            "maxQty": operationMode
        }
        log.info("生成盘点任务时请求参数为：%s", para)
        stock_opeartion_config.get("inventory_process_order_generate_task")["data"].update(para)
        res = self.send_request(**stock_opeartion_config.get("inventory_process_order_generate_task"))
        print("盘点单生成盘点任务：", res.get("message"))
        return

    def inventory_process_order_page(self, **kwargs):
        """
        盘点单列表页查询，默认参数查询"新建"状态的单据
        @param kwargs:
        @return:
        """
        stock_opeartion_config.get("inventory_process_order_page")["data"].update(
            kwargs
        )
        res = self.send_request(**stock_opeartion_config.get("inventory_process_order_page"))
        print("盘点单-列表页查询信息：", res.get("data")["records"])
        return res.get("data")["records"]

    def inventory_process_task_page(self, **kwargs):
        """
        盘点任务列表页查询
        @param kwargs:
        @return:
        """
        stock_opeartion_config.get("inventory_process_task_page")["data"].update(
            kwargs
        )
        res = self.send_request(**stock_opeartion_config.get("inventory_process_task_page"))
        print("盘点任务-列表页查询信息：", res.get("data")["records"])
        return res.get("data")["records"]

    def inventory_process_assign(self, task_no_list):
        """
        盘点任务分配人员
        @param task_no_list：任务单号列表（支持批量）
        @return:
        """
        stock_opeartion_config.get("inventory_process_assign")["data"].update(
            {
                "inventoryProcessTaskNo": task_no_list
            }
        )
        res = self.send_request(**stock_opeartion_config.get("inventory_process_assign"))
        print("盘点任务分配人员：", res.get("message"))
        return

    def inventory_process_print(self, task_no):
        """
        打印
        @param task_no：任务单号
        @return:
        """
        stock_opeartion_config.get("inventory_process_print")["data"].update(
            {
                "inventoryProcessTaskNo": task_no,
                "t": self.time_tamp
            }
        )
        res1 = self.send_request(**stock_opeartion_config.get("inventory_process_print"))
        print("打印结果：", res1.get("message"))
        stock_opeartion_config.get("inventory_process_printTimes")["data"].update(
            {
                "inventoryProcessTaskNo": task_no,
                "t": self.time_tamp
            }
        )
        res2 = self.send_request(**stock_opeartion_config.get("inventory_process_printTimes"))
        print("打印次数：", res2.get("message"))
        return

    def inventory_process_task_detailPage(self, taskid):
        """
        盘点任务详情页信息
        @param kwargs:
        @return:
        """
        stock_opeartion_config.get("inventory_process_task_detailPage")["data"].update({
            "inventoryProcessTaskId": taskid
        }
        )
        res = self.send_request(**stock_opeartion_config.get("inventory_process_task_detailPage"))
        print("盘点任务-详情页信息：", res.get("data")["records"])
        return res.get("data")["records"]

    def inventory_process_commit(self, task_no, task_detail):
        """
        盘点任务提交
        @return:
        """
        rep_list = []
        for i in task_detail:
            item = {
                "skuCode": i.get("skuCode"),
                "locCode": i.get("locCode"),
                "inventoryProcessTaskNo": task_no,
                "inventoryProcessTaskDetailId": i.get("inventoryProcessTaskDetailId"),
                "inventoryProcessQty": i.get("skuInventoryStartQty") + random.randint(-1, 1),#实际盘点数量
                "inventoryStartQty": i.get("skuInventoryStartQty")
            }
            rep_list.append(item)
        rep_detail = {
            "inventoryProcessTaskNo": task_no,
            "commitDetails": rep_list
        }
        print("盘点任务-提交参数拼装：", rep_detail)
        log.info("盘点任务-提交参数拼装：%s", rep_detail)
        stock_opeartion_config.get("inventory_process_commit")["data"].update(rep_detail)
        res = self.send_request(**stock_opeartion_config.get("inventory_process_commit"))
        print(res)
        return

if __name__ == '__main__':


    st = StockOpearationController()
    # st.adjust_receipt([{"waresSkuCode": "53586714577A01",
    #                     "storageLocationCode": "KW-SJQ-01",
    #                     "changeCount": "1",
    #                     "changeType": "2",
    #                     "adjustReason": "2"}])

    # st.adjust_receipt_page(1, 0, 1)

    # st.adjust_receipt_batch_audit(2, [5382])

    data = {
        "inventoryProcessLatitude": 0,
        "inventoryProcessRange": 0,
        "inventoryProcessType": 0,
        "locDetails": [
            {
                "locCode": "KW-SJQ-3150"
            }
        ]
    }

    # st.inventory_process_order_create()

    task_no = "PD2302020036_T2-1"
    st.inventory_process_print(task_no)
    # st.inventory_process_print(task_no)
    # dic = {"inventoryProcessTaskNoLike": task_no}
    # task_id = st.inventory_process_task_page(**dic)[0].get("inventoryProcessTaskId")
    # task_detail = st.inventory_process_task_detailPage(task_id)

    # st.inventory_process_commit(task_no, task_detail)
