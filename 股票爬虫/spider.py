import csv
import json
import requests
from prettytable import PrettyTable

def getData(baseUrl, headers):
    response = requests.get(url=baseUrl, headers=headers)
    data = json.loads(response.text)['data']['diff']
    result = []
    for key, value in data.items():
        value['f2'] = '%.2f' % (value['f2'] / 100)
        value['f3'] = '%.2f' % (value['f3'] / 100) + '%'
        value['f4'] = '%.2f' % (value['f4'] / 100)
        value['f5'] = '%.2f' % (value['f5'] / 10000) + '万'
        value['f6'] = '%.2f' % (value['f6'] / 100000000) + '亿'
        value['f7'] = '%.2f' % (value['f7'] / 100) + '%'
        value['f15'] = '%.2f' % (value['f15'] / 100)
        value['f16'] = '%.2f' % (value['f16'] / 100)
        value['f17'] = '%.2f' % (value['f17'] / 100)
        value['f18'] = '%.2f' % (value['f18'] / 100)
        value['f10'] = '%.2f' % (value['f10'] / 100)
        value['f8'] = '%.2f' % (value['f8'] / 100) + '%'
        value['f9'] = '%.2f' % (value['f9'] / 100)
        value['f23'] = '%.2f' % (value['f23'] / 100)
        result.append([key, value['f12'], value['f14'], value['f2'], value['f3'], value['f4'], value['f5'], value['f6'],
                       value['f7'], value['f15'], value['f16'], value['f17'], value['f18'], value['f10'], value['f8'],
                       value['f9'], value['f23']])
    return result

def printData(result):
    table = PrettyTable()
    table.field_names = ["序号", "代码", "名称", "最新价", "涨跌幅", "涨跌额", "成交量(手)", "成交额", "振幅", "最高",
                         "最低", "今开", "昨收", "量比", "换手率", "市盈率（动态）", "市净率"]
    table.add_rows(result)
    print(table)


import csv
from datetime import datetime


def saveData(result):
    # 获取当前日期并格式化为字符串
    current_date = datetime.now().strftime('%Y-%m-%d')
    # 使用当前日期作为文件名的一部分
    file_path = f'D:/股价选取开发/A股数据集/A股股票数据_{current_date}.csv'

    with open(file_path, 'w', encoding='utf-8-sig', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["序号", "代码", "名称", "最新价", "涨跌幅", "涨跌额", "成交量(手)", "成交额", "振幅", "最高",
                         "最低", "今开", "昨收", "量比", "换手率", "市盈率（动态）", "市净率"])
        writer.writerows(result)


def main():
    baseUrl = 'https://22.push2.eastmoney.com/api/qt/clist/get?pn=1&pz=6000&po=1&fid=f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    result = getData(baseUrl, headers)
    printData(result)
    saveData(result)

if __name__ == "__main__":
    main()
