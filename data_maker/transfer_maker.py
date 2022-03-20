from controller.wms_controller import *
from tools.request_operator import RequestOperator

class TransferMaker(WmsController):

    def __init__(self):
        self.prefix = env_config.get("app_prefix")
        self.headers = UmsController().get_app_headers()


    def add_stock(self, warehouse_code, salesku, bom_ver, skunum, shelves_location_code):
        self.switch_warehouse(warehouse_code)
        entryorder_info = self.entryorder(salesku, bom_ver, skunum)
        entryorder_sku_list = self.get_sku_info_by_entryCode(entryorder_info)
        entryo_order_id = entryorder_info.get("entryOrderId")
        res = self.put_on_the_shelf(shelves_location_code, skunum, entryo_order_id, entryorder_sku_list)
        print("上架操作：", res)

if __name__ == '__main__':
    transfer = TransferMaker()
    transfer.add_stock("UKBH01", "53586714577", ["B", "D"], 5, "KW-SJQ-01")



