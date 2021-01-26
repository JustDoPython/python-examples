# 年化复合回报 15%
(1+0.15)**100
# 1174313.4507002793

# 定投的收益
import numpy_financial as npf
npf.fv(0.1, 12, -1000, 0)
# 21384.28376721003
npf.pmt(0.1, 12, 0, 50000)
# -2338.165755014362


# 定期不定额的收益率
pmts = [-1000, 100, -1300, -2000, 5200]
npf.irr(pmts)
# 0.10969579295711918

# 不定期不定额的收益率
from XIRR import xirr
import datetime

dates = [datetime.date(2019, 2,4), 
datetime.date(2019, 6, 17), 
datetime.date(2019,11, 18),
datetime.date(2020,4, 27),
datetime.date(2020,10, 19)]

values = [-300.3,-500.5,741.153,-600.6,1420.328547]

xirr(values, dates)
# 输出为: 0.779790640991537