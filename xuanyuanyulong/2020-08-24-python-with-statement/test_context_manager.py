class testContextManager:
    def __enter__(self):
        print("进入运行时上下文，调用__enter__方法")

    def __exit__(self, exc_type, exc_value, traceback):
        print("退出运行时上下文，调用__exit__方法")


with testContextManager() as o:
    pass