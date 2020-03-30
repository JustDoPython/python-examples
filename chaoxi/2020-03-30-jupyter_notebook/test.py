import numpy as np
import pandas as pd
# 创建一个多维数组
data=pd.DataFrame(np.arange(20).reshape(4,5),index=list('abcd'),columns=list('ABCDE'))
print(data)