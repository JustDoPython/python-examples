import pandas as pd
import numpy as np

# 读取文件 整理数据 

## 读取文件 选择特定的列，队列进行归一化，之后对整个数值进行归一化
config = {
    '学校名称': {'name': '学校'},
    '省市': {'name': '省市'},
    '排名': {'name': '排名', 'fun': lambda x: 500-int(x) if x is not np.nan else int(x)},
    '总分': {'name': '总分'},
    '生源质量（新生高考成绩得分）':{'name': '生源质量', 'norm': True},
    '培养成果（本科毕业生就业率）':{'name': '就业', 'alias': '培养结果（毕业生就业率）', 'norm': True, 'fun': lambda x: float(x[:-1])/100 if x is not np.nan else float(x)},
    '社会声誉（社会捐赠收入·千元）':{'name': '声誉', 'norm': True},
    '科研规模（论文数量·篇）':{'name': '科研规模', 'norm': True},
    '科研质量（论文质量·FWCI）':{'name': '科研质量', 'norm': True, 'fun': lambda x: float(x) if str(x).find(">")==-1 else float(x[1:]) },
    '顶尖成果（高被引论文·篇）':{'name': '顶尖成果', 'norm': True},
    '顶尖人才（高被引学者·人）':{'name': '顶尖人才', 'norm': True},
    '科技服务（企业科研经费·千元）':{'name': '科技服务', 'norm': True},
    '成果转化（技术转让收入·千元）':{'name': '成果转化', 'norm': True},
    '学生国际化（留学生比例）':{'name': '学生国际化', 'norm': True, 'fun': lambda x: float(x) if str(x).find("%")==-1 else float(x[:-1])}
}

data = {}

for year in range(2015, 2020):
    print(year)
    # rawdf = pd.read_excel('./code/university/data/university_%d.xlsx' % year)
    rawdf = pd.read_excel('./data/university_%d.xlsx' % year)

    df = pd.DataFrame(columns=[config[col]['name'] for col in config])

    for col in config:
        colConf = config[col]
        if col in rawdf or colConf.get('alias', 'None') in rawdf:
            if colConf.get('alias', 'None') in rawdf:
                col = colConf.get('alias')

            if colConf.get('fun') is not None:
                dft = rawdf[col].apply(colConf.get('fun'))
            else:
                dft = rawdf[col]
            colname = colConf.get('name')
            if colConf.get('norm'):
                print(colname)
                df[colname] = (dft - dft.min())/(dft.max() - dft.min())
            else:
                df[colname] = dft
        
    # 设置index
    df = df.set_index('学校')
    df = df.fillna(0)
    data[year] = df

for year in data:
    df = data[year]
    df.to_excel('./data/university_1_%d.xlsx' % year, index=True)
# todo 注意异常值和缺省值的处理
# todo 处理空缺指