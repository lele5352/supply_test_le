from datetime import time, datetime
from openpyxl import load_workbook

import pandas as pd
import os


def count_time(data_frame, start_time_column, end_time_column, count_time_column='时长'):
    """
    计算时长
    @param data_frame: 读取到的Excel句柄
    @param start_time_column: "开始时间"列名称
    @param end_time_column: "结束时间"列名称
    @param count_time_column: "时长"列名称
    @return:
    """

    # 将时间1和时间2列格式化为时间格式
    data_frame[start_time_column] = pd.to_datetime(data_frame[start_time_column], format='%H:%M:%S')
    data_frame[end_time_column] = pd.to_datetime(data_frame[end_time_column], format='%H:%M:%S')
    # 新增时长列
    data_frame[count_time_column] = (data_frame[end_time_column] - data_frame[
        start_time_column]).dt.total_seconds() / 3600
    data_frame[count_time_column] = data_frame[count_time_column].round(2)

    # 将时间1和时间2转换为字符串格式
    data_frame[start_time_column] = data_frame[start_time_column].dt.strftime('%H:%M:%S')
    data_frame[end_time_column] = data_frame[end_time_column].dt.strftime('%H:%M:%S')
    return


def tx_tapd(file_path, tapd_sheet_name):
    """
    处理【TAPD】相关的主表
    @param file_path:
    @param tapd_sheet_name: 原sheet名称
    @return:
    """

    try:
        # 从 Excel 文件中读取【TAPD_ip】表格
        df = pd.read_excel(file_path, sheet_name=tapd_sheet_name)
        if df.empty:
            raise ValueError(f"错误：表格【{tapd_sheet_name}】读取的信息为空，请检查表格内容")
        else:
            # 拆分“签到日期”列
            split_values = df['签到日期'].str.split(' ', expand=True)

            # 创建新的列，分别表示日期和星期
            df['签到日期-日期'] = split_values[0]
            df = df.rename(columns={"签到日期-日期": "日期"})

            # 将字符串列转换为日期时间格式
            df['日期'] = pd.to_datetime(df['日期'])

            return df
    except Exception as e:
        raise e


def tx_menjin(file_path, entrance_guard_sheet_name):
    """
    处理【门禁】相关的表格
    @param file_path:
    @param entrance_guard_sheet_name: 门禁sheet相关的名称
    @return:
    """

    try:
        # 从 Excel 文件中读取【entrance_guard_sheet_name】表格
        df = pd.read_excel(file_path, sheet_name=entrance_guard_sheet_name)
        if df.empty:
            raise ValueError(f"表格【{entrance_guard_sheet_name}】读取的信息为空，请检查表格内容")
        else:
            # 根据姓名和日期进行分组，获取每组的第一条数据和最后一条数据
            df = df.groupby(['讯息日期', '姓名']).agg({'讯息时间': ['min', 'max']}).reset_index()

            df.columns = ['讯息日期', '姓名', 'min', 'max']

            # 重命名列名
            df = df.rename(columns={"讯息日期": "日期", "min": "场地门禁签入", "max": "场地门禁签出"})

            # 获取时长列
            count_time(df, "场地门禁签入", "场地门禁签出")

            # 将字符串列转换为日期时间格式
            df['日期'] = pd.to_datetime(df['日期'])
            return df
    except Exception as e:
        raise e


def tx_zr_zw(file_path, fingerprint_sheet_name):
    """
    处理【中软-指纹】表格
    @param file_path:
    @param fingerprint_sheet_name:
    @return:
    """
    try:
        # 从 Excel 文件中读取【中软-指纹】表格
        df = pd.read_excel(file_path, sheet_name=fingerprint_sheet_name)
        if df.empty:
            raise ValueError(f"表格【{fingerprint_sheet_name}】读取的信息为空，请检查表格内容")
        else:
            # 按照姓名和日期分组，同时在'进'列中取最早时间，在'出'列中取最晚时间
            df = df.groupby(['姓名', '日期']).agg({'时间': ['min', 'max']}).reset_index()
            df.columns = ['姓名', '日期', 'min', 'max']

            # 重命名列名
            df = df.rename(columns={"min": "签入时间", "max": "签出时间"})

            # 获取时长列
            count_time(df, "签入时间", "签出时间")

            # 将字符串列转换为日期时间格式
            df['日期'] = pd.to_datetime(df['日期'])
            return df
    except Exception as e:
        raise e


def tx_rt_zw(file_path, fingerprint_sheet_name):
    """
    处理【软通-指纹】表格
    @param file_path:
    @param fingerprint_sheet_name:
    @return:
    """
    try:
        # 从 Excel 文件中读取【软通-指纹】表格
        df = pd.read_excel(file_path, sheet_name=fingerprint_sheet_name)
        if df.empty:
            raise ValueError(f"表格【{fingerprint_sheet_name}】读取的信息为空，请检查表格内容")
        else:
            # 拆分“时间”列
            df['打卡时间'] = pd.to_datetime(df['打卡时间'], format='%Y-%m-%d (%H:%M)')
            df['日期'] = df['打卡时间'].dt.date
            df['时间'] = df['打卡时间'].dt.time

            """
            如果单元格内时间为str格式时，可以使用下面的方式
            split_values = fp_df['打卡时间'].str.split(' ', expand=True)
            # 将字符串转换为年月日的时间类型
            fp_df['日期'] = pd.to_datetime(split_values[0], format='%Y-%m-%d').dt.date
            # 将字符串转换为时分秒的时间类型
            fp_df['时间'] = pd.to_datetime(split_values[1], format='%H:%M:%S').dt.time
            """

            # 将数据按日期分组
            df = df.groupby(['日期', '姓名']).agg({'时间': ['min', 'max']}).reset_index()
            df.columns = ['日期', '姓名', 'min', 'max']

            # 重命名列名
            df = df.rename(columns={"min": "签入时间", "max": "签出时间"})
            # 获取时长列
            count_time(df, "签入时间", "签出时间")

            # 将字符串列转换为日期时间格式
            df['日期'] = pd.to_datetime(df['日期'])
            return df
    except Exception as e:
        raise e


def tx_yxc_face(file_path, face_sheet_name):
    """
    处理【杨协成-人脸】表格
    @param file_path:
    @param face_sheet_name:
    @return:
    """
    try:
        # 从 Excel 文件中读取【杨协成-人脸】表格
        df = pd.read_excel(file_path, sheet_name=face_sheet_name)
        if df.empty:
            raise ValueError(f"表格【{face_sheet_name}】读取的信息为空，请检查表格内容")
        else:
            df['时间'] = pd.to_datetime(df['时间'], format='%Y-%m-%d %H:%M:%S')
            df['日期'] = df['时间'].dt.date
            df['时间'] = df['时间'].dt.time

            # 将数据按日期分组
            df = df.groupby(['日期', '姓名']).agg({'时间': ['min', 'max']}).reset_index()
            df.columns = ['日期', '姓名', 'min', 'max']

            # 重命名列名
            df = df.rename(columns={"min": "签入时间", "max": "签出时间"})
            # 获取时长列
            count_time(df, "签入时间", "签出时间")
            # 将字符串列转换为日期时间格式
            df['日期'] = pd.to_datetime(df['日期'])

            return df
    except Exception as e:
        raise e


def tx_welink(file_path, weLink_sheet_name):
    """
    处理【welink打卡】表格
    @param file_path:
    @param weLink_sheet_name:
    @return:
    """
    try:
        # 从 Excel 文件中读取【中软-指纹】表格
        df = pd.read_excel(file_path, sheet_name=weLink_sheet_name, usecols=[" 打卡日期", " 姓名", " 上班时间", " 下班时间"])
        if df.empty:
            raise ValueError(f"表格【{weLink_sheet_name}】读取的信息为空，请检查表格内容")
        else:
            df = df.rename(columns={" 打卡日期": "日期", " 姓名": "姓名", " 上班时间": "签入时间", " 下班时间": "签出时间"})

            # 将字符串列转换为日期时间格式
            df['日期'] = pd.to_datetime(df['日期'])
            return df
    except Exception as e:
        raise e


def tx_oa_new(file_path, summary_sheet):
    print("开始处理子sheet表格...")
    # 列表内表名顺序与执行顺序需要一致！！！
    sheet_name_list = ['TAPD-主表', '中软-门禁', '软通-门禁', '杨协成-门禁', '中软-指纹', '软通-指纹', '杨协成-人脸', 'welink打卡']
    try:
        tapd_df = tx_tapd(file_path, sheet_name_list[0])
        zr_mj_df = tx_menjin(file_path, sheet_name_list[1])
        rt_mj_df = tx_menjin(file_path, sheet_name_list[2])
        yxc_mj_df = tx_menjin(file_path, sheet_name_list[3])
        zr_zw_df = tx_zr_zw(file_path, sheet_name_list[4])
        rt_zw_df = tx_rt_zw(file_path, sheet_name_list[5])
        yxc_face_df = tx_yxc_face(file_path, sheet_name_list[6])
        we_link_df = tx_welink(file_path, sheet_name_list[7])

        # 门禁表格相关竖向合并
        merged_mj = pd.concat([zr_mj_df, rt_mj_df, yxc_mj_df], ignore_index=True)

        # 指纹和人脸表格相关竖向合并
        merged_zw_face = pd.concat([zr_zw_df, rt_zw_df, yxc_face_df], ignore_index=True)

        # 按姓名和日期列汇总合并
        print("开始合并...")
        merged1 = pd.merge(tapd_df, merged_mj, on=['姓名', '日期'], how='left')
        merged2 = pd.merge(merged1, merged_zw_face, on=['姓名', '日期'], how='left')
        merged = pd.merge(merged2, we_link_df, on=['姓名', '日期'], how='left')

        # 跑出结果的数据做相关列名做相关调整，对齐预期表格
        merged.insert(merged.columns.get_loc('状态') + 1, '实际签入大厦', None)
        merged.insert(merged.columns.get_loc('实际签入大厦') + 1, '实际签出大厦', None)
        merged.drop(columns=['日期', '时长_x', '时长_y'], inplace=True)

        # 打开Excel文件，准备写入
        with pd.ExcelWriter(file_path, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
            # 将合并后的数据写入sheet时，不保留当前数据的表头，设置起始行为的最后一行的下一行
            merged.to_excel(writer, sheet_name=summary_sheet, index=False, header=False, startrow=2)
        return print("大功告成！！！")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    path = os.path.join(os.path.expanduser("~"), 'Desktop')
    excel_path = path + '/V1.xlsx'
    summary_sheet = '双打卡数据信息'

    tx_oa_new(excel_path, summary_sheet)
    # tx_tapd(excel_path, 'TAPD-主表')
