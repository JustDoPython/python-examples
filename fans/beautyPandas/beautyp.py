import pandas as pd
from datetime import datetime,timedelta


df2 = pd.read_excel("C:/sf3/sf3/excel/1170_07-28.xlsx",sheet_name="邵阳")

new = df2.set_index(pd.to_datetime(df2['最后上线时间']))
new.index.name = 'last'
new.sort_values('最后上线时间', ascending=True,inplace=True)

new['设备类型'] = new['设备别名'].str.split('0').str[0].str.split(' ').str[0]
new2 = new.groupby(['设备类型','最后上线时间','设备别名','连接状态','所属监测点'],as_index=False)

new3 = new2.all()
now = datetime.now().strftime('%Y-%m-%d')
sevenDaysAgo = (datetime.now() + timedelta(days=-7)).strftime('%Y-%m-%d')
new3.style.highlight_between(left=sevenDaysAgo,right=now,subset=['最后上线时间'],props='font-weight:bold;color:rgb(64, 158, 255)')\
.highlight_between(left='普适型声光报警器',right='普适型声光报警器',subset=['设备类型'],props='background:#c7f5fe')\
.highlight_between(left='普适型声光报警器',right='声光报警器',subset=['设备类型'],props='background:#c7f5fe')\
.highlight_between(left='普适型GNSS基准站',right='普适型GNSS基准站',subset=['设备类型'],props='background:#ffa5a5')\
.highlight_between(left='普适型GNSS基站',right='普适型GNSS基站',subset=['设备类型'],props='background:#ffa5a5')\
.highlight_between(left='普适型GNSS监测站',right='普适型GNSS监测站',subset=['设备类型'],props='background:#a1eafb')\
.highlight_between(left='普适型裂缝计',right='普适型裂缝计',subset=['设备类型'],props='background:#a6e3e9')\
.highlight_between(left='普适型雨量计',right='普适型雨量计',subset=['设备类型'],props='background:#71c9ce')\
.highlight_between(left='在线',right='在线',subset=['连接状态'],props='background:#f9ed69')\
.highlight_between(left='普适型变形桩',right='普适型变形桩',subset=['设备类型'],props='background:#cbf1f5')