from threading import Thread
import socket
from serversocket import ServerSocket
import re

clients = {}
def checkname(name, cid):
    for key, value in clients.items():
        if key != cid and value['name'] == name:
            return False
    return True

def sendMsg(msg, _from, _to=None):
    cid = _from['cid']
    closeCids = []
    for key, value in clients.items():
        if value['cid'] != cid and (not _to or value['name'] in _to):
            try:
                value['sock'].send(msg)
            except Exception as e:
                print(e)
                closeCids.append(key)
                
    for _cid in closeCids:
        del clients[cid]

def onReceiveMsg(server, sock, ip, data):
    cid = f'{ip[0]}_{ip[1]}'
    data = data.decode('utf-8')
    print(f"收到数据: {data}")
    _from = clients[cid]
    if data.startswith('name:'):
        name = data[5:].strip()
        if not name:
            sock.send(f"不能设置空名称，否则其他人找不见你".encode('utf-8'))
        elif not checkname(name, cid):
            sock.send(f"这个名字{name}已经被使用，请换一个试试".encode('utf-8'))
        else:
            if not _from['name']:
                sock.send(f"{name} 很高兴见到你，现在可以畅游元宇宙了".encode('utf-8'))
                msg = f"新成员{name} 加入了元宇宙，和TA聊聊吧".encode('utf-8')
                sendMsg(msg, _from)
            else:
                sock.send(f"更换名称完成".encode('utf-8'))
                msg = f"{_from['name']} 更换名称为 {name}，和TA聊聊吧".encode('utf-8')
                sendMsg(msg, _from)
            _from['name'] = name
        
    elif '@' in data:
        targets = re.findall(r'@(.+?) ', data)
        print(targets)
        msg = f"{_from['name']}: {data}".encode('utf-8')
        sendMsg(msg, _from, targets)
    else:
        msg = f"{_from['name']}：{data}".encode('utf-8')
        sendMsg(msg, _from)

def onCreateConn(server, sock, ip):
    cid = f'{ip[0]}_{ip[1]}'
    clients[cid] = {'cid': cid, 'sock': sock, '@allcount': 10, 'name': None}
    sock.send("你已经接入元宇宙，告诉我你的代号,输入格式为 name:lily.".encode('utf-8'))
    
def onCloseConn(server, sock, ip):
    cid = f'{ip[0]}_{ip[1]}'
    name = clients[cid]['name']
    if name:
        msg = f"{name} 从元宇宙中消失了".encode('utf-8')
        sendMsg(msg, clients[cid])
    del clients[cid]
    pass
    
if __name__ == '__main__':
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    server = ServerSocket(ip, 6000, onReceiveMsg, onCreateConn, onCloseConn)
    thread = None

    while True:
        print("start 启动服务器")
        print("stop 关闭动服务器")
        print('quit 退出程序')
        value = input("输入指令：")
        value = value.strip()
        if value == 'start':
            if thread:
                print("服务器正在运行")
            else:
                thread = Thread(target=server.run)
                thread.start()
                print("服务器启动完成")
            pass
        elif value == 'stop' or value == 'quit':
            if thread:
                server.stop()
                print("服务器正在关闭中")
                thread.join()
                print("服务器已经关闭")
                thread = None
            if value == 'quit':
                print("退出程序")
                break
            pass
        elif value == 'show':
            print(clients)
        else:
            print("无效指令，请重新输入!")