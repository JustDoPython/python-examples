import os
import re
path=os.getcwd()
fr=open(path+'/gaoxiao-dict.txt','r',encoding='utf-8')
dic={}
keys=[]
for line in fr:
	v=line.strip().split(':')
	dic[v[0]]=v[1]
	keys.append(v[0])
fr.close()
#规范命名的函数
def normalReName(name):
	isTikuban=re.findall(r'【题库版】',name)
	if len(isTikuban)!=0:
		m=name.replace('【题库版】','').replace('_','')
		os.rename(name+'.pdf',m+'.pdf')
	else:
		m=name
	s=re.findall(r'.*?大学|.*?学院|.*?（北京）|.*?（华东）|.*?（武汉）',m)
	university=''
	for i in range (0,len(s)):
		university+=s[i]
	code=re.search('\d{3}',m)
	year=re.findall('\d{4}',m)
	if '年' in m:
		b=m.replace(university+code.group(),'').replace(year[0]+'年','')
	else:
		b=m.replace(university+code.group(),'').replace(year[0],'')
	new_name=dic[university]+'+'+university+'+'+code.group()+b+'+'+year[0]+'年'
	os.rename(m+'.pdf',new_name+'.pdf')
file_name_list=os.listdir(path)
for file in file_name_list:
	name=file.split('.')[0]
	kuozhan=file.split('.')[1]
	if name!='watermark' and kuozhan=='pdf':
		normalReName(name)