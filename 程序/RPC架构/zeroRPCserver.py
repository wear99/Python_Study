import zerorpc

from socketserver import ThreadingMixIn  # 多线程
from core.DataHandler import dataHandler


class RPCServer(ThreadingMixIn, zerorpc.Server):  # 继承了多线程和rpc server的类
    pass


server = RPCServer(dataHandler())
#server = zerorpc.Server(dataHandler())
server.bind("tcp://127.0.0.1:8002")
server.run()
