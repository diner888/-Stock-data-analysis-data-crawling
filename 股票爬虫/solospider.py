import pandas as pd
from typing import List
import requests
from jsonpath import jsonpath
from datetime import datetime

# 获取当前日期并格式化为字符串
current_date = datetime.now().strftime('%Y-%m-%d')

class CustomedSession(requests.Session):
    def request(self, *args, **kwargs):
        kwargs.setdefault('timeout', 60)
        return super(CustomedSession, self).request(*args, **kwargs)


session = CustomedSession()
adapter = requests.adapters.HTTPAdapter(pool_connections=50, pool_maxsize=50, max_retries=5)
session.mount('http://', adapter)
session.mount('https://', adapter)

# 请求地址
QEURY_URL = 'http://push2his.eastmoney.com/api/qt/stock/kline/get'
# HTTP 请求头
EASTMONEY_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko',
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
}

# 获取单只股票的历史K线数据
def get_k_history_data(
        stock_codes: str,  # 股票代码
        beg: str = '19000101',  # 开始日期，19000101，表示 1900年1月1日
        end: str = '20500101',  # 结束日期
        klt: int = 101,  # 行情之间的时间间隔 1、5、15、30、60分钟; 101:日; 102:周; 103:月
        fqt: int = 1,  # 复权方式，0 不复权 1 前复权 2 后复权
):
    try:
        # 生成东方财富专用的secid
        if stock_codes[:3] == '000':  # 沪市指数
            secid = f'1.{stock_codes}'
        elif stock_codes[:3] == '399':  # 深证指数
            secid = f'0.{stock_codes}'

        if stock_codes[0] != '6':  # 沪市股票
            secid = f'0.{stock_codes}'
        else:
            secid = f'1.{stock_codes}'  # 深市股票

        EASTMONEY_KLINE_FIELDS = {'f51': '日期', 'f52': '开盘', 'f53': '收盘', 'f54': '最高', 'f55': '最低',
                                  'f56': '成交量', 'f57': '成交额', 'f58': '振幅', 'f59': '涨跌幅', 'f60': '涨跌额',
                                  'f61': '换手率', }
        fields = list(EASTMONEY_KLINE_FIELDS.keys())
        fields2 = ",".join(fields)
        params = (
            ('fields1', 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13'),
            ('fields2', fields2),
            ('beg', beg),
            ('end', end),
            ('rtntype', '6'),
            ('secid', secid),
            ('klt', f'{klt}'),
            ('fqt', f'{fqt}'),
        )
        code = secid.split('.')[-1]
        json_response = session.get(QEURY_URL, headers=EASTMONEY_REQUEST_HEADERS, params=params, verify=False).json()
        data_list = []
        klines: List[str] = jsonpath(json_response, '$..klines[:]')
        if not klines:
            return data_list

        name = json_response['data']['name']
        rows = [kline.split(',') for kline in klines]
        # 0           1      2     3      4      5        6           7        8        9       10
        # 日期,       开盘,   收盘, 最高,  最低,   成交量,  成交额,      振幅,    涨跌幅,   涨跌额, 换手率
        # 2024-05-08, 4.89,  4.82, 4.91,  4.80,  61811,  29955564.00,  2.25,  -1.23,    -0.06,  0.98
        for row in rows:
            time, open, close, high, low, vol, quota, mm, change, range, tun = row
            data_list.append({
                '日期': time,
                '开盘': open,
                '收盘': close,
                '最高': high,
                '最低': low,
                '成交量': vol,
                '成交额': quota,
                '振幅': mm,
                '涨跌幅': change,
                '涨跌额': range,
                '换手率': tun,
                '代码': code,
                '名称': name
            })

        return data_list
    except Exception as e:
        print('get_k_history_data error-----------------------', str(e))
        return data_list


def save_to_csv(data, file_path):
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False, encoding='utf-8-sig')


if __name__ == "__main__":
    # 读取上传的表格
    file_path = f'D:\股价选取开发\A股数据集\A股股票数据_{current_date}.csv'
    data = pd.read_csv(file_path)

    # 获取所有股票代码
    codes_list = data['代码'].astype(str).unique()

    all_stock_data = []
    for codes in codes_list:
        # 搜索股票代码
        data = get_k_history_data(stock_codes=codes, beg='20240101', end='20500101')
        # save_to_csv(data, f'D:\股价选取开发\A股数据集\单股数据\{current_date}.csv')  # 修改为你实际的路径
        # print('数据已保存到CSV文件中')
        if data:
            all_stock_data.extend(data)
        # 保存所有数据到一个CSV文件
    if all_stock_data:
        save_to_csv(all_stock_data, f'D:\\股价选取开发\\A股数据集\\单股数据\\{current_date}.csv')
        print(f'所有股票数据已保存到CSV文件中')
    else:
        print('未获取到任何股票数据')

