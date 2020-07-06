# utils.py
# 工具模块，将字符串变成字典
def str_to_dict(s, join_symbol="\n", split_symbol=":"):
    s_list = s.split(join_symbol)
    data = dict()
    for item in s_list:
        item = item.strip()
        if item:
            k, v = item.split(split_symbol, 1)
            data[k] = v.strip()
    return data