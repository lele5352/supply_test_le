import pymysql
"""
    目标：完成数据库相关工具类封装
    分析：
        1.主要方法
            假设：def get_sql_one(sql):获取数据库数据
        2.辅助方法
            2.1获取链接对象
            2.2获取游标对象
            2.3执行sql语句
            2.4关闭游标对象
            2.5关闭链接对象
"""

class MySqlOperator:

    def __init__(self, mysql_info, db):
        mysql_info['db'] = db
        try:
            self.conn = pymysql.connect(**mysql_info, charset='utf8', cursorclass=pymysql.cursors.DictCursor)
        except Exception as e:
            print("errMsg：", e)
        self.cour = self.conn.cursor()


    # 关闭数据库
    def close(self):
        # 如果数据打开，则关闭；否则没有操作
        if self.conn and self.cour:
            self.cour.close()
            self.conn.close()
        return

    #主要方法  ->在外界调用此方法可以完成数据库相应的操作

    def get_sql_one(self, sql):
        """
        单个查询
        :param sql:
        :return:
        """
        self.cour.execute(sql)
        return self.cour.fetchone()

    def get_sql_many(self, sql, num):
        """
        批量查询
        :param sql:
        :param num:
        :return:
        """
        self.cour.execute(sql)
        return self.cour.fetchmany(size=num)

    def get_sql_all(self, sql):
        """
        全量查询
        :param sql:
        :return:
        """
        self.cour.execute(sql)
        return self.cour.fetchall()

    # 单个数据-修改、删除、新增
    def execute(self, sql):
        # 定义游标对象及数据变量
        sursor = None
        try:
            if self.conn and self.cour:
                self.cour.execute(sql)
                # 提交事务
                self.conn.commit()
        except Exception as e:
            # 事务回滚
            self.conn.rollback()
            print("execute error:", e)
            self.close()

    # 批量数据-修改、删除、新增
    def executemany(self, sql):
        # 定义游标对象及数据变量
        sursor = None
        try:
            if self.conn and self.cour:
                self.cour.executemany(sql)
                # 提交事务
                self.conn.commit()
        except Exception as e:
            # 事务回滚
            self.conn.rollback()
            print("executemany error:", e)
            self.close()



if __name__ == '__main__':
    sql = "select * from central_inventory where goods_sku_code = '53586714577';"
    sql_1 = "delete from central_inventory where goods_sku_code = '53586714577' and warehouse_id =536;"
    sql_info = {
                    "mysql_info": {
                    "user": "erp",
                    "passwd": "sd)*(YSHDG;l)D_FKds:D#&y}",
                    "host": "10.0.0.127",
                    "port": 3306},
                    "db": "supply_ims"
                }
    # data = MySqlOperator(**sql_info).get_sql_all(sql)

    mysql_info = {
                    "user": "erp",
                    "passwd": "sd)*(YSHDG;l)D_FKds:D#&y}",
                    "host": "10.0.0.127",
                    "port": 3306}

    sql2 = "INSERT INTO `supply_report`.`rp_transfer_box_order_batch` (`delivery_warehouse_code`, `delivery_warehouse_name`, `delivery_warehouse_short_name`, `receive_warehouse_code`, `receive_warehouse_name`, `receive_warehouse_short_name`, `box_no`, `transfer_out_no`, `storage_location_code`, `container_no`, `out_state`, `goods_sku_code`, `goods_sku_name`, `wares_sku_code`, `wares_sku_name`, `sku_qty`, `batch_no`, `create_user_id`, `create_username`, `create_time`, `del_flag`) VALUES ('UKBH01', '英国1号仓', 'UK01', 'UKBH02', '英国2号仓', 'UK02', 'DC1200000001', 'DC1200000001-1', 'KW-RQ-TP-01', 'Q416TzaR', 3, 'J011194-2V', 'aa', 'J011194-2VA01', '餐桌吊灯 1/1 X1', 1, '', 308, '2022-10-20 17:10:03', 0);"
    data = MySqlOperator(mysql_info, "supply_report").execute(sql2)
    print(data)