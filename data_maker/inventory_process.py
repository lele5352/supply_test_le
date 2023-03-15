from data_maker import *
import time

class InventoryProcess:
    def __init__(self):
        self.time_tamp = int(time.time() * 1000)
        # self.wms = wms
        # self.st = st
        # self.pda = pda

    def kw_inventory_process(self, warehouse_code, **kwargs):

        # 切换到相关仓库
        wms.switch_warehouse(warehouse_code)
        # 新增盘点单
        st.inventory_process_order_create(**kwargs)
        #   查询盘点单
        order_info = st.inventory_process_order_page()  #默认值查询新建状态的单据
        order_no = order_info[0].get("inventoryProcessOrderNo")
        # order_id = order_info[0].get("inventoryProcessOrderId")
        #   盘点单内库位数量--生成盘点任务时使用
        loqty = order_info[0].get("locQty")

        #   盘点单生成盘点任务单--默认使用纸质单盘点
        st.inventory_process_order_generate_task(order_no, loqty)
        #   通过盘点单找到盘点任务单
        task_info = st.inventory_process_task_page(**{"inventoryProcessOrderNoLike": order_no})
        task_id = task_info[0].get("inventoryProcessTaskId")
        task_no = task_info[0].get("inventoryProcessTaskNo")
        #   分配人员
        task_no_list = [task_no]
        st.inventory_process_assign(task_no_list)
        #   打印
        st.inventory_process_print(task_no)

        #   查看任务详情，获取提交相关的参数
        # task_id = 1909
        # task_no = "PD2301310003_T1-1"
        task_detail = st.inventory_process_task_detailPage(task_id)
        st.inventory_process_commit(task_no, task_detail)









if __name__ == '__main__':

    ip = InventoryProcess()
    warehouse = "KWDR-TEST"
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

    ip.kw_inventory_process(warehouse, **data)
