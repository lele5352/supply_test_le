from tools.request_operator import RequestOperator
from controller.ums_controller import UmsController
from config.sys_config import env_config
from config.api_config.stock_operation_api import stock_opeartion_config
from tools.log_operator import logger as log
import time


class StockOpearationController(RequestOperator):

    def __init__(self, ums):
        self.prefix = env_config.get("web_prefix")
        self.headers = ums.header
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


if __name__ == '__main__':
    ums = UmsController()
    st = StockOpearationController(ums)

    st.adjust_receipt([{"waresSkuCode": "53586714577B01",
                        "storageLocationCode": "KW-SJQ-01",
                        "changeCount": "1",
                        "changeType": "2",
                        "adjustReason": "2"}])

    # st.adjust_receipt_page(1, 0, 1)

    st.adjust_receipt_batch_audit(2, [1259])
