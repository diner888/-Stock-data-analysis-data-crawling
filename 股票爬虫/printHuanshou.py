import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

def plot_stock_turnover(data_path, stock_codes):
    # 获取当前日期并格式化为字符串
    current_date = datetime.now().strftime('%Y-%m-%d')

    # 加载数据
    data = pd.read_csv(data_path)

    # 将日期列转换为日期类型
    data['日期'] = pd.to_datetime(data['日期'])

    # 设置样式
    sns.set(style="whitegrid")

    # 创建图形对象并设置大小
    plt.figure(figsize=(14, 8))

    # 为每个股票代码绘制折线图
    for stock_code in stock_codes:
        # 根据股票代码筛选数据
        filtered_data = data[data['代码'].astype(str) == stock_code]

        if not filtered_data.empty:
            # 绘制换手率随时间变化的折线图
            sns.lineplot(data=filtered_data, x='日期', y='换手率', marker='o', label=f'股票代码 {stock_code}')
        else:
            print(f"未找到股票代码 {stock_code} 的数据。")

    # 设置标题和标签
    plt.title('不同股票的换手率随时间变化情况', fontsize=20, fontweight='bold', fontname='SimHei')
    plt.xlabel('日期', fontsize=15, fontname='SimHei')
    plt.ylabel('换手率', fontsize=15, fontname='SimHei')

    # 美化日期标签
    plt.xticks(rotation=45)

    # 显示图例
    plt.legend(title='股票代码')

    # 显示网格
    plt.grid(True, linestyle='--', alpha=0.7)

    # 显示图表
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # 获取用户输入的股票代码，使用逗号分隔
    user_input = input("请输入股票代码，以逗号分隔: ")
    stock_codes = [code.strip() for code in user_input.split(',')]

    # 数据文件路径
    data_path ="D:/股价选取开发/A股数据集/单股数据/2024-05-24.csv"

    # 调用函数绘制图表
    plot_stock_turnover(data_path, stock_codes)
