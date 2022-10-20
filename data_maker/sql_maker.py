from data_maker import mysql_report
from tools.random_operator import *

class MySql_maker:

    def __init__(self):
        self.mysql_report = mysql_report

    def rp_transfer_box_order_batch(self, num):
        time_star = time.time()
        for i in range(num):
            transfer_out_no = generate_random_no("DC", i)
            box_no = generate_random_no("DC", i, suffix="-1")
            container_no = generate_random_str(8)
            create_time = time.strftime('%Y-%m-%d %H:%m:%S', time.localtime(time.time()))
            sql = "INSERT INTO `supply_report`.`rp_transfer_box_order_batch` (`delivery_warehouse_code`, `delivery_warehouse_name`, `delivery_warehouse_short_name`, `receive_warehouse_code`, `receive_warehouse_name`, `receive_warehouse_short_name`, `box_no`, `transfer_out_no`, `storage_location_code`, `container_no`, `out_state`, `goods_sku_code`, `goods_sku_name`, `wares_sku_code`, `wares_sku_name`, `sku_qty`, `batch_no`, `create_user_id`, `create_username`, `create_time`, `del_flag`) \
                  VALUES ('UKBH01', '英国1号仓', 'UK01', 'UKBH02', '英国2号仓', 'UK02', '{box_no}', '{transfer_out_no}', 'KW-RQ-TP-01', '{container_no}', 3, 'J011194-2V', 'aa', 'J011194-2VA01', '餐桌吊灯 1/1 X1', 1, '', 308, '黄乐乐', '{create_time}', 0);".format(box_no=box_no, transfer_out_no=transfer_out_no, container_no=container_no, create_time=create_time)
            # print(sql)
            self.mysql_report.execute(sql)
        self.mysql_report.close()
        time_end = time.time()
        time_use = time_end - time_star  #单条插入的形式，10000条数据耗时：187.49860405921936
        print(time_use)
if __name__ == '__main__':

    # sql = 'select * from rp_transfer_box_order_batch'
    # data = mysql_report.get_sql_many(sql, 5)
    # print(data)

    sql_maker = MySql_maker()
    # sql_maker.rp_transfer_box_order_batch(5)
    sql_maker.rp_transfer_box_order_batch(10000)
