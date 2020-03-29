# 引入包
import tushare as tu

# 获取上证指数历史三年的数据
tu.get_hist_data('000001')

# 当然我们也可以只获取一段时间范围内的数据
tu.get_hist_data('000001',start='2020-01-05',end='2020-02-05')

# 获取所有股票当前行情
tu.get_today_all()

# 获取茅台和格力两支股票的实时数据
data = tu.get_realtime_quotes(['600519','000651'])

# 也可以设置只显示某些值
data[['code','name','price','bid','ask','volume','amount','time']]

#或者获取上证指数 深圳成指 沪深300指数 上证50 中小板 创业板
tu.get_realtime_quotes(['sh','sz','hs300','sz50','zxb','cyb'])

# 获取大盘行情
data = tu.get_index()

# 获取茅台当前日期的大单交易数据，默认400手
tu.get_sina_dd('600519', date='2020-03-27')

# 获取交易100手以上的数据
tu.get_sina_dd('600519', date='2020-03-27', vol=100)
