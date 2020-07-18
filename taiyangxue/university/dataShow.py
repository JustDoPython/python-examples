import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

mpl.rcParams['font.sans-serif'] = ['KaiTi']
mpl.rcParams['font.serif'] = ['KaiTi']
data = {}
for year in range(2015, 2020):
    data[str(year)+"年"] = pd.read_excel('./data/university_1_%d.xlsx' % year, index_col=0)

def trendChart(schools, indicator='总分'):
    """
    给定学校(数组)，得到这些学校5年的趋势图
    """
    ret = pd.DataFrame(index=[str(x)+"年" for x in range(2015,2020)],columns=schools)

    for year in data:
        df = data[year][indicator]
        for school in schools:
            if school in df.index:
                ret.loc[year, school] = df[school]
            else:
                ret.loc[year, school] = np.nan

    ret.plot.line(title="%s 走势" % indicator, linewidth=1.5, yticks=[])
    plt.show()

def indicatorChart(schools, indicators=['生源质量','声誉','科研规模',
'科研质量','顶尖成果','顶尖人才','科技服务',], year=2019):
    """
    指定学校，年份，以及需要对比的指标，显示出雷达图
    """
    year = str(year) + '年'
    result = pd.DataFrame(index=schools,columns=indicators)
    df = data[year][indicators]
    for school in schools:
        if school in df.index:
            result.loc[school] = df.loc[school]

    labels=result.columns.values #特征值
    kinds = list(result.index) #成员变量
    result = pd.concat([result, result[[labels[0]]]], axis=1) # 由于在雷达图中，要保证数据闭合，这里就再添加第一列，并转换为np.ndarray
    centers = np.array(result.iloc[:,:])
    n = len(labels)
    angle = np.linspace(0, 2 * np.pi, n, endpoint=False)# 设置雷达图的角度,用于平分切开一个圆面
    angle = np.concatenate((angle, [angle[0]]))#为了使雷达图一圈封闭起来,需要下面的步骤
    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True) # 参数polar, 以极坐标的形式绘制图
    
    for i in range(len(kinds)):
        ax.plot(angle, centers[i], linewidth=1.5, label=kinds[i])
        plt.fill(angle,centers[i] , 'r', alpha=0.05) 
        
    ax.set_thetagrids(angle * 180 / np.pi, labels)
    plt.title(year + ' 指标对比')
    plt.legend()
    plt.show()

if __name__ == '__main__':
    # trendChart(['北京理工大学',    '西北工业大学',    '东华大学',    '福州大学',    '中国矿业大学',], '成果转化')
    # indicatorChart(['清华大学','北京大学','烟台大学','北京科技大学','西安交通大学','西北工业大学'])
    # indicatorChart(['山东工商学院','烟台大学','宝鸡文理学院'])
    # indicatorChart(['西安交通大学','北京科技大学','北京理工大学'])
    indicatorChart(['清华大学', '北京大学','上海交通大学', '浙江大学', '复旦大学'])
    trendChart(['北京理工大学', '西北工业大学', '东华大学', '福州大学', '中国矿业大学'], '排名')





