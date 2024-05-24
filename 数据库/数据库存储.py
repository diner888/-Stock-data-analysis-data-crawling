import mysql.connector
import pandas as pd
import datetime

current_date=datetime.datetime.now()
# 数据库连接配置
db_config = {
    'user': 'root',
    'password': 'lqh32104295',
    'host': '3306',
    'database': '@localhost'
}

# 提前定义connection变量
connection = None

# 连接到数据库
try:
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    # 创建表的SQL语句
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS stock_data (
        id INT AUTO_INCREMENT PRIMARY KEY,
        code VARCHAR(10) NOT NULL,
        name VARCHAR(100) NOT NULL,
        latest_price DECIMAL(10, 2) NOT NULL,
        change_percentage VARCHAR(10) NOT NULL,
        change_amount DECIMAL(10, 2) NOT NULL,
        volume VARCHAR(20) NOT NULL,
        turnover DECIMAL(15, 2) NOT NULL,
        amplitude VARCHAR(10) NOT NULL,
        highest DECIMAL(10, 2) NOT NULL,
        lowest DECIMAL(10, 2) NOT NULL,
        opening_price DECIMAL(10, 2) NOT NULL,
        previous_closing_price DECIMAL(10, 2) NOT NULL,
        volume_ratio DECIMAL(10, 2) NOT NULL,
        turnover_rate VARCHAR(10) NOT NULL,
        dynamic_pe_ratio DECIMAL(10, 2) NOT NULL,
        pb_ratio DECIMAL(10, 2) NOT NULL
    );
    """
    cursor.execute(create_table_sql)

    # 读取CSV文件
    file_path = f"D:\\股价选取开发\\A股数据集\\A股股票数据_{current_date}.csv"
    data = pd.read_csv(file_path)

    # 定义插入数据的SQL语句
    insert_sql = """
    INSERT INTO stock_data (
        code, name, latest_price, change_percentage, change_amount, volume, turnover,
        amplitude, highest, lowest, opening_price, previous_closing_price, volume_ratio,
        turnover_rate, dynamic_pe_ratio, pb_ratio
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    # 插入数据
    for index, row in data.iterrows():
        cursor.execute(insert_sql, (
            row['代码'], row['名称'], row['最新价'], row['涨跌幅'], row['涨跌额'], row['成交量(手)'],
            row['成交额'], row['振幅'], row['最高'], row['最低'], row['今开'], row['昨收'],
            row['量比'], row['换手率'], row['市盈率（动态）'], row['市净率']
        ))

    # 提交事务
    connection.commit()

except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    # 关闭数据库连接
    if connection.is_connected():
        cursor.close()
        connection.close()