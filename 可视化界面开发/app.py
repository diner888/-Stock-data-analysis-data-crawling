from datetime import datetime
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
from matplotlib.font_manager import FontProperties
# 设置matplotlib字体支持中文显示
matplotlib.rcParams['font.family'] = 'SimHei'  # 指定字体为SimHei
matplotlib.rcParams['axes.unicode_minus'] = False  # 正确显示负号

# 获取当前日期并格式化为字符串
current_date = datetime.now().strftime('%Y-%m-%d')

def main():
    # 加载数据
    data = pd.read_csv(f"D:\\股价选取开发\\A股数据集\\A股股票数据_{current_date}.csv")
    # data1=pd.read_csv(f"D:\\股票选取开发\\A股数据集\\单股数据\\{current_date}")
    # 数据预处理
    data['市净率'] = data['市净率'].astype(str).str.rstrip('%').astype(float)
    data['换手率'] = data['换手率'].astype(str).str.rstrip('%').astype(float)
    data['涨跌幅'] = data['涨跌幅'].astype(str).str.rstrip('%').astype(float)
    # 应用标题
    st.title('A股市面信息')
    st.write(f"股票信息更新时间为：{current_date}")
    # 添加筛选器侧边栏
    name = st.sidebar.multiselect('股票名称', data['名称'].unique())

    if name:
        selected_codes = data[data['名称'].isin(name)]['代码'].astype(str).unique()
        st.sidebar.write("选择的股票代码: ", ', '.join(selected_codes))
        
    filter_type = st.sidebar.radio('筛选类型', ('市净率', '量比', '换手率','涨跌幅'))
    if filter_type == '市净率':
        gdp_per_capita_range = st.sidebar.slider('市净率',
                                                 min_value=float(data['市净率'].min()),
                                                 max_value=float(data['市净率'].max()),
                                                 value=(float(data['市净率'].min()), float(data['市净率'].max())),
                                                 step=0.1)  # 确保步长类型为浮点数

        # 数据筛选
        filtered_data = data[(data['名称'].isin(name)) & (data['市净率'].between(*gdp_per_capita_range))]

        # 显示筛选后的数据
        st.write(f"筛选后的数据包含 {filtered_data.shape[0]} 条记录")
        st.dataframe(filtered_data)

        # 按名称分组并计算平均市净率
        grouped_data = filtered_data.groupby('名称', as_index=False)['市净率'].mean()
        sns.set(style="whitegrid")

        # 创建一个包含子图的图形对象 - 量比
        fig_volume, ax_volume = plt.subplots(figsize=(12, 8))

        # 绘制条形图 - 量比
        sns.barplot(x='名称', y='市净率', data=grouped_data, ax=ax_volume, palette='viridis')
        ax_volume.set_xticklabels(grouped_data['名称'], rotation=0, ha='right')  # 设置x轴标签旋转角度和对齐方式
        ax_volume.set_ylabel('市净率', fontname='SimHei')
        ax_volume.set_title('不同股票的市净率情况', fontname='SimHei')
        # 强制所有文本元素使用 SimHei 字体
        for label in ax_volume.get_xticklabels():
            label.set_fontname('SimHei')
            label.set_fontsize(20)  # 设置字体大小为20

        # 显示图形 - 量比
        st.pyplot(fig_volume)



        # # 显示选择的公司名称，每个公司之间用空格隔开
        # company_names = ' '.join(filtered_data['名称'].unique())
        # st.write(f"股票名称：{company_names}")

        # 股票知识
        st.title("股票指标解释")
        st.header("市净率")
        st.write("市净率（PB）市净率的计算方法是：市净率=股票市价/每股净资产")
        st.write(
            "股票净值即资本公积金、资本公益金、法定公积金、任意公积金、未分配盈余等项目的合计,它代表全体股东共同享有的权益,也称净资产。净资产的多少是由股份公司经营状况决定的,股份公司的经营业绩越好,其资产增值越快,股票净值就越高,因此股东所拥有的权益也越多")
        st.write(
            "**所以,股票净值是决定股票市场价格走向的主要根据。上市公司的每股内含净资产值高而每股市价不高的股票,即市净率越低的股票,其投资价值越高。相反,其投资价值就越小**")
        st.write(
            "市净率能够较好地反映出\"有所付出,即有回报\",它能够帮助投资者寻求哪个上市公司能以较少的投入得到较高的产出,对于大的投资机构,它能帮助其辨别投资风险")
        st.write("**这里要指出的是：市净率不适用于短线炒作。提高获利能力**")
        st.write(
            "市净率可用于投资分析。每股净资产是股票的账面价值，它是用成本计量的，而每股市价是这些资产的现在价值，它是证券市场上交易的结果。市价高于账面价值时企业资产的质量较好，有发展潜力，反之则资产质量差，没有发展前景。优质股票的市价都超出每股净资产许多，一般说来市净率达到3可以树立较好的公司形象。市价低于每股净资产的股票，就象售价低于成本的商品一样，属于“处理品”。当然，“处理品”也不是没有购买价值，问题在于该公司今后是否有转机，或者购入后经过资产重组能否提高获利能力。")

    elif filter_type == '量比':
        volume_ratio_range = st.sidebar.slider('量比',
                                               min_value=float(data['量比'].min()),
                                               max_value=float(data['量比'].max()),
                                               value=(float(data['量比'].min()), float(data['量比'].max())),
                                               step=0.1)  # 确保步长类型为浮点数

        # 数据筛选 - 量比
        filtered_data_volume = data[(data['名称'].isin(name)) & (data['量比'].between(*volume_ratio_range))]

        # 显示筛选后的数据 - 量比
        st.write(f"筛选后的数据包含 {filtered_data_volume.shape[0]} 条记录")
        st.dataframe(filtered_data_volume)

        # 按名称分组并计算平均量比
        grouped_data_volume = filtered_data_volume.groupby('名称', as_index=False)['量比'].mean()
        # 设置样式
        sns.set(style="whitegrid")

        # 创建一个包含子图的图形对象 - 量比
        fig_volume, ax_volume = plt.subplots(figsize=(12, 8))

        # 绘制条形图 - 量比
        sns.barplot(x='名称', y='量比', data= grouped_data_volume, ax=ax_volume, palette='viridis')
        ax_volume.set_xticklabels( grouped_data_volume['名称'], rotation=0, ha='right')  # 设置x轴标签旋转角度和对齐方式
        ax_volume.set_ylabel('量比', fontname='SimHei')
        ax_volume.set_title('不同股票的量比情况', fontname='SimHei')
        # 强制所有文本元素使用 SimHei 字体
        for label in ax_volume.get_xticklabels():
            label.set_fontname('SimHei')
            label.set_fontsize(20)  # 设置字体大小为20

        # 显示图形 - 量比
        st.pyplot(fig_volume)

        # # 显示选择的公司名称，每个公司之间用空格隔开
        # company_names_volume = ' '.join(filtered_data_volume['名称'].unique())
        # st.write(f"股票名称：{company_names_volume}")

        # 股票知识
        st.title("股票指标解释")
        st.header("量比")
        st.write("量比＝现成交总手 /（过去5日平均每分钟成交量×当日累计开市时间（分））")
        st.write(
            "当量比大于1时，说明当日每分钟的平均成交量要大于过去5日的平均数值，交易比过去5日火爆；而当量比小于1时，说明现在的成交比不上过去5日的平均水平。在观察成交量方面，卓有成效的分析工具是量比，它将某只股票在某个时点上的成交量与一段时间的成交量平均值进行比较，排除了因股本不同造成的不可比情况，是发现成交量异动的重要指标。在时间参数上，多使用１０日平均量，也有使用5平均值的。在大盘处于活跃的情况下，适宜用较短期的时间参数，而在大盘处于熊市或缩量调整阶段宜用稍长的时间参数。")
        st.write(
            "一般来说，若某日量比为０.８-１.５倍，则说明成交量处于正常水平；量比在１.５-２.５倍之间则为温和放量，如果股价也处于温和缓升状态，则升势相对健康，可继续持股，若股价下跌，则可认定跌势难以在短期内结束，从量的方面判断应可考虑停损退出；量比在２.５-５倍，则为明显放量，若股价相应地突破重要支撑或阻力位置，则突破有效的几率颇高，可以相应地采取行动；量比达５-１０倍，则为剧烈放量，如果是在个股处于长期低位出现剧烈放量突破，涨势的后续空间巨大，是“钱”途无量的象征，东方集团、乐山电力在５月份突然启动之时，量比之高令人讶异。但是，如果在个股已有巨大涨幅的情况下出现如此剧烈的放量，则值得高度警惕。")
        st.write(
            "**某日量比达到１０倍以上的股票，一般可以考虑反向操作。**在涨势中出现这种情形，说明见顶的可能性压倒一切，即使不是彻底反转，至少涨势会休整相当长一段时间。在股票处于绵绵阴跌的后期，突然出现的巨大量比，说明该股在目前位置彻底释放了下跌动能。")
        st.write(
            "量比在２０倍以上的情形基本上每天都有一两单，是极端放量的一种表现，这种情况的反转意义特别强烈，如果在连续的上涨之后，成交量极端放大，但股价出现“滞涨”现象，则是涨势行将死亡的强烈信号。当某只股票在跌势中出现极端放量，则是建仓的大好时机。")
        st.write(
            "**量比在０.５倍以下的缩量情形也值得好好关注，其实严重缩量不仅显示了交易不活跃的表象，同时也暗藏着一定的市场机会。缩量创新高的股票多数是长庄股，缩量能创出新高，说明庄家控盘程度相当高，而且可以排除拉高出货的可能。缩量调整的股票，特别是放量突破某个重要阻力位之后缩量回调的个股，常常是不可多得的买入对象。**")
        st.write("**涨停板时量比在１倍以下的股票，上涨空间无可限量，第二天开盘即封涨停的可能性极高。**")

    elif filter_type == '换手率':
        turnover_rate_range = st.sidebar.slider('换手率',
                                                min_value=float(data['换手率'].min()),
                                                max_value=float(data['换手率'].max()),
                                                value=(float(data['换手率'].min()), float(data['换手率'].max())),
                                                step=0.1)  # 确保步长类型为浮点数

        # 数据筛选 - 换手率
        filtered_data_turnover = data[(data['名称'].isin(name)) & (data['换手率'].between(*turnover_rate_range))]

        # 显示筛选后的数据 - 换手率
        st.write(f"筛选后的数据包含 {filtered_data_turnover.shape[0]} 条记录")
        st.dataframe(filtered_data_turnover)

        # 按名称分组并计算平均换手率
        grouped_data_turnover = filtered_data_turnover.groupby('名称', as_index=False)['换手率'].mean()
        # 设置样式
        sns.set(style="whitegrid")

        # 创建一个包含子图的图形对象 - 量比
        fig_volume, ax_volume = plt.subplots(figsize=(12, 8))

        # 绘制条形图 - 量比
        sns.barplot(x='名称', y='换手率', data=grouped_data_turnover, ax=ax_volume, palette='viridis')
        ax_volume.set_xticklabels(grouped_data_turnover['名称'], rotation=0, ha='right')  # 设置x轴标签旋转角度和对齐方式
        ax_volume.set_ylabel('换手率', fontname='SimHei')
        ax_volume.set_title('不同股票的换手率情况', fontname='SimHei')
        # 强制所有文本元素使用 SimHei 字体
        for label in ax_volume.get_xticklabels():
            label.set_fontname('SimHei')
            label.set_fontsize(20)  # 设置字体大小为20

        # 显示图形 - 量比
        st.pyplot(fig_volume)

        # 绘制换手率随时间变化图表





        # # 显示选择的公司名称，每个公司之间用空格隔开
        # company_names_turnover = ' '.join(filtered_data_turnover['名称'].unique())
        # st.write(f"股票名称：{company_names_turnover}")
        # 股票知识
        st.title("股票指标解释")
        st.header("换手率")
        st.write(
            """
              换手率也称“周转率”，指在一定时间内市场中股票转手买卖的频率，是反映股票流通性强弱的指标之一。\n
            **其计算公式为：周转率(换手率)＝(某一段时期内的成交量)/(发行总股数)x100%**\n
              例如，某只股票在一个月内成交了2000万股，而该股票的总股本为1亿股，则该股票在这个月的换手率为20%。
            在我国，股票分为可在二级市场流通的社会公众股和不可在二级市场流通的国家股和法人股两个部分，一般只对可流通部分的股票计算换手率，以更真实和准确地反映出股票的流通性。
            按这种计算方式，上例中那只股票的流通股本如果为2000万，则其换手率高达100%。
            在国外，通常是用某一段时期的成交金额与某一时点上的市值之间的比值来计算周转率。\n
            换手率的高低往往意味着这样几种情况：\n
            (1)股票的换手率越高，意味着该只股票的交投越活跃，人们购买该只股票的意愿越高，属于热门股；反之，股票的换手率越低，则表明该只股票少人关注，属于冷门股。\n
            (2)换手率高一般意味着股票流通性好，进出市场比较容易，不会出现想买买不到、想卖卖不出的现象，具有较强的变现能力。然而值得注意的是，换手率较高的股票，往往也是短线资金追逐的对象，投机性较强，股价起伏较大，风险也相对较大。\n
            (3)将换手率与股价走势相结合，可以对未来的股价做出一定的预测和判断。某只股票的换手率突然上升，成交量放大，可能意味着有投资者在大量买进，股价可能会随之上扬。如果某只股票持续上涨了一个时期后，换手率又迅速上升，则可能意味着一些获利者要套现，股价可能会下跌。\n
            """
        )
    elif filter_type == '涨跌幅':
        volume_ratio_range = st.sidebar.slider('涨跌幅',
                                               min_value=float(data['涨跌幅'].min()),
                                               max_value=float(data['涨跌幅'].max()),
                                               value=(float(data['涨跌幅'].min()), float(data['涨跌幅'].max())),
                                               step=0.1)  # 确保步长类型为浮点数

        # 数据筛选 - 量比
        filtered_data_volume = data[(data['名称'].isin(name)) & (data['涨跌幅'].between(*volume_ratio_range))]

        # 显示筛选后的数据 - 量比
        st.write(f"筛选后的数据包含 {filtered_data_volume.shape[0]} 条记录")
        st.dataframe(filtered_data_volume)

        # 按名称分组并计算平均量比
        grouped_data_volume = filtered_data_volume.groupby('名称', as_index=False)['涨跌幅'].mean()

        # 设置样式
        sns.set(style="whitegrid")

        # 创建一个包含子图的图形对象 - 量比
        fig_volume, ax_volume = plt.subplots(figsize=(12, 8))

        # 绘制条形图 - 量比
        sns.barplot(x='名称', y='涨跌幅', data=grouped_data_volume, ax=ax_volume, palette='viridis')
        ax_volume.set_xticklabels(grouped_data_volume['名称'], rotation=0, ha='right')  # 设置x轴标签旋转角度和对齐方式
        ax_volume.set_ylabel('涨跌幅',fontname='SimHei')
        ax_volume.set_title('不同股票的涨跌幅情况',fontname='SimHei')
        # 强制所有文本元素使用 SimHei 字体
        for label in ax_volume.get_xticklabels():
            label.set_fontname('SimHei')
            label.set_fontsize(20)  # 设置字体大小为20

        # 显示图形 - 量比
        st.pyplot(fig_volume)
        #
        # # 显示选择的公司名称，每个公司之间用空格隔开
        # company_names_volume = ' '.join(filtered_data_volume['名称'].unique())
        # st.write(f"股票名称：{company_names_volume}")
        st.title("股票指标解释")
        # 涨跌幅名词解释
        explanation =  """
**涨跌幅**是指股票、基金、债券等金融产品在一个交易日内价格相对于前一交易日收盘价的变动幅度。它通常用百分比来表示，反映了该金融产品价格的波动情况。具体来说：

- **涨幅**：当价格比前一交易日收盘价上涨时，称为涨幅。
- **跌幅**：当价格比前一交易日收盘价下跌时，称为跌幅。

计算公式如下：

$$
\\text{涨跌幅} (\%) = \\frac{\\text{当日收盘价} - \\text{前一交易日收盘价}}{\\text{前一交易日收盘价}} \\times 100\\%
$$

### 例子
如果某只股票前一交易日的收盘价是100元，今天的收盘价是110元，那么它的涨跌幅为：

$$
\\text{涨跌幅} = \\frac{110 - 100}{100} \\times 100\\% = 10\\%
$$

如果今天的收盘价是90元，那么它的涨跌幅为：

$$
\\text{涨跌幅} = \\frac{90 - 100}{100} \\times 100\\% = -10\\%
$$

### 作用
涨跌幅是投资者判断市场走势和个股表现的重要指标之一。通过分析涨跌幅，投资者可以了解市场的整体情况以及具体股票的波动性，从而做出相应的投资决策。

在实际操作中，交易所通常会对单个股票的涨跌幅设置一个上限和下限，即涨跌停板，以防止市场过度波动。例如，中国大陆A股市场的涨跌幅限制一般为10%，这意味着一个交易日内股票的价格变动不得超过前一交易日收盘价的10%。
"""
        st.markdown(explanation)


if __name__ == "__main__":
    main()
