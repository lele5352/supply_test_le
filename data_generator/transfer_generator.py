from data_generator import wms, wms_service


def transfer_maker(delivery_warehouse_code, delivery_target_warehouse_code, receive_warehouse_code,
                   receive_target_warehouse_code, goods_sku_code, demand_qty, bom_version,
                   delivery_kw_tp_code_list, receive_kw_sj_code_list):
    # 切换到发货仓库
    wms.switch_warehouse(delivery_warehouse_code)
    # 新增调拨需求
    demands = wms_service.transfer_demand_creat(delivery_warehouse_code, delivery_target_warehouse_code,
                                                receive_warehouse_code, receive_target_warehouse_code,
                                                goods_sku_code, demand_qty, bom_version,
                                                demand_qty)
    try:
        demand_code = demands.get("data")["demandCode"]
    except Exception as demand_code:
        print("未知错误 %s" % demand_code)
    wms.demand_list(demand_code_list=[demand_code])


if __name__ == '__main__':
    transfer_maker("UKBH01", "", "UKBH022", "", "53586714577", 1, "C", '', '')