import socket
from threading import Thread

close = False

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
def receive(client):
    while True:
        try:
            s_info = client.recv(1024)  # 接受服务端的消息并解码
            if not s_info:
                print(f"{bcolors.WARNING}服务器链接断开{bcolors.ENDC}")
                break
            print(f"{bcolors.OKCYAN}新的消息：{bcolors.ENDC}\n", bcolors.OKGREEN + s_info.decode('utf-8')+ bcolors.ENDC)
        except Exception:
            print(f"{bcolors.WARNING}服务器链接断开{bcolors.ENDC}")
            break
        if close:
            break
            
def createClient(ip, port):
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((ip, port))
    return client
    
def help():
    print(":start\t启动")
    print(":stop\t关闭")
    print(':quit\t退出')
    print(':help\t帮助\n--------------')
    
if __name__ == '__main__':
    # 获取本机计算机名称
    hostname = socket.gethostname()
    # 获取本机ip
    # ip = '20.2.100.200' #socket.gethostbyname(hostname)
    ip = socket.gethostbyname(hostname)
    
    client = None
    
    thread = None
    help()
    while True:
        pass
        value = input("")
        value = value.strip()
        
        if value == ':start':
            if thread:
                print(f"{bcolors.OKBLUE}您已经在元宇宙中了{bcolors.ENDC}")
            else:
                client = createClient(ip, 6000)
                thread = Thread(target=receive, args=(client,))
                thread.start()
                print(f"{bcolors.OKBLUE}您进入元宇宙了{bcolors.ENDC}")
        elif value == ':quit' or value == ':stop':
            if thread:
                client.close()
                close = True
                print(f"{bcolors.OKBLUE}正在退出中…{bcolors.ENDC}")
                thread.join()
                print(f"{bcolors.OKBLUE}元宇宙已退出{bcolors.ENDC}")
                thread = None
            if value == ':quit':
                print(f"{bcolors.OKBLUE}退出程序{bcolors.ENDC}")
                break
            pass
        elif value == 'help':
            help()
        else:
            if client:
                # 聊天模式
                client.send(value.encode('utf-8'))
            else:
                print(f'{bcolors.WARNING}还没接入元宇宙，请先输入 :start 接入{bcolors.ENDC}')
    client.close()