from config.api_config.wms_api import wms_api_config
from config.sys_config import env_config
from tools.request_operator import RequestOperator
from controller.ums_controller import UmsController

class PdaController(RequestOperator):

    def __init__(self, ums):
        self.prefix = env_config.get("app_prefix")
        self.headers = ums.header
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
            print(res)
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
            #拼接参数--装托的sku信息
            tray_infos = []
            for i in picking_detail_info.get("details"):
                sku_info = {
                    "id": i["id"],
                    "waresSkuCode": i["waresSkuCode"],
                    "waresSkuName": i["waresSkuName"],
                    "goodsSkuCode": i["goodsSkuCode"],
                    "goodsSkuName": i["goodsSkuName"],
                    "skuQty": i["realPickQty"]
                }
                tray_infos.append(sku_info)

            wms_api_config.get("pda_submit_tray_info")["data"].update({
                "storageLocationCode": location_code_list[0],
                "pickOrderNo": pick_order_no,
                "trayInfos": tray_infos
            })
            try:
                res = self.send_request(**wms_api_config.get("pda_submit_tray_info"))
                print(res)
                return res
            except Exception as e:
                raise Exception("err_info:", e)

        else:
            print("传入的拣货单信息为空，请检查'pda_picking_detail()'函数返回参数")

    def pda_move_storage(self):
        """
        不成套移出
        :return:
        """
        pass

    def pda_finish_picking(self, location_code):
        """
        创建出库单
        :param location_code:
        :return:
        """
        pass



if __name__ == '__main__':
    ums = UmsController()
    pda = PdaController(ums)
    pda.pda_picking_detail("DJH2204110002")