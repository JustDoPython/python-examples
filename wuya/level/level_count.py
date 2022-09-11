import networkx as nx
import pandas as pd
from pyvis import network as net

df = pd.read_excel('./doc/1_evidence.xls')
df = df.loc[:, ['id','name','invite_id','invited_id']]
df.columns = ['id','title','to', 'from']

G = nx.from_pandas_edgelist(df, 'from', 'to', create_using=nx.DiGraph())

# 找到根节点
top_node = []
for node, degrees in G.in_degree():
    if degrees == 0:
        top_node.append(node)
print('Big Boss:', top_node)

# 设置所有节点级别
l = nx.shortest_path_length(G, 100000)
nx.set_node_attributes(G, l, 'level')

# 计算每级人员数目
data = {}
for node, level in l.items():
    if level in data.keys():
        data[level].append(node)
    else:
        data[level] = [node]
for level, nodes in data.items():
    print(level, len(nodes))

# 添加颜色
for node in G.nodes:
    G.nodes[node]['title'] = str(node)
    level = G.nodes[node]['level']

    if level == 0:
        G.nodes[node]['color'] = 'red'
    elif level == 1:
        G.nodes[node]['color'] = 'orange'
    elif level == 2:
        G.nodes[node]['color'] = 'yellow'

# 给下线前十的目标添加颜色
degrees = G.out_degree()
top_nodes = sorted(degrees, key=lambda x: x[1], reverse=True)[:10]
print(top_nodes)

for node in top_nodes:
    G.nodes[node[0]]['color'] = 'green'

nt = net.Network('960px', '1280px', directed=True)
nt.from_nx(G)
nt.show('1_evidence.html')

