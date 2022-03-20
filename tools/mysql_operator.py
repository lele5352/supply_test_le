import pymysql
import json
"""
    目标：完成数据库相关工具类封装
    分析：
        1.主要方法
            假设：def get_sql_one(sql):获取数据库数据
        2.辅助方法
            1.获取链接对象
            2.获取游标对象
            3.关闭游标对象
            4.关闭链接对象
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
        # cursor = self.get_cursor()
        self.cour.execute(sql)
        data = self.cour.fetchone()
        self.close()
        return data

    def get_sql_many(self, sql, num):
        self.cour.execute(sql)
        data = self.cour.fetchmany(size=num)
        self.close()
        return data

    def get_sql_all(self, sql):
        self.cour.execute(sql)
        data = self.cour.fetchall()
        self.close()
        return data

    # 修改、删除、新增
    def update_sql(self, sql):
        # 定义游标对象及数据变量
        sursor = None
        try:
            self.cour.execute(sql)
            # 提交事务
            self.conn.commit()
        except Exception as e:
            # 事务回滚
            self.conn.rollback()
            print("get_sql_one error:", e)
        finally:
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
                "db": "supply_ims_new"
    }
    data = MySqlOperator(**sql_info).get_sql_all(sql)
    print(data)