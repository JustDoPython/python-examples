import time
import threading

class DataSource:
    def __init__(self, dataFileName, startLine=0, maxcount=None):
        self.dataFileName = dataFileName
        self.startLine = startLine  # 第一行行号为1
        self.line_index = startLine # 当前读取位置
        self.maxcount = maxcount  # 读取最大行数
        self.lock = threading.RLock() # 同步锁        

        self.__data__ = open(self.dataFileName, 'r', encoding= 'utf-8')
        for i in range(self.startLine):
            l = self.__data__.readline()

    def getLine(self):
        self.lock.acquire()
        try:
            if self.maxcount is None or self.line_index < (self.startLine + self.maxcount):
                line = self.__data__.readline()
                if line:
                    self.line_index += 1
                    return True, line
                else:
                    return False, None
            else:
                return False, None

        except Exception as e:
            return False, "处理出错:" + e.args
        finally:
            self.lock.release()
    
    def __del__(self):
        if not self.__data__.closed:
            self.__data__.close()
            print("关闭数据源:", self.dataFileName)

def process(worker_id, datasource):
    count = 0
    while True:
        status, data = datasource.getLine()
        if status:
            print(">>> 线程[%d] 获得数据， 正在处理……" % worker_id)
            time.sleep(3) # 等待3秒模拟处理过程
            print(">>> 线程[%d] 处理数据 完成" % worker_id)
            count += 1
        else:
            break # 退出循环
    print(">>> 线程[%d] 结束， 共处理[%d]条数据" % (worker_id, count))


def main():
    datasource = DataSource('data.txt') # 创建数据源类
    workercount = 10 # 开启的线程数
    workers = []
    for i in range(workercount):
        worker = threading.Thread(target=process, args=(i+1, datasource))
        worker.start()
        workers.append(worker)
    
    for worker in workers:
        worker.join()