import dis

with open("test_dis.py", "r", encoding="utf-8") as f:
    s = f.read()

compile_obj = compile(s, "test_dis.py","exec")

dis.dis(compile_obj)