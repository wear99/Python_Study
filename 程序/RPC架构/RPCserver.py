# _*_ coding:utf-8 _*_

from xmlrpc.server import SimpleXMLRPCServer
from socketserver import ThreadingMixIn  # 多线程

from core.DataHandler import dataHandler
#import BaseHTTPServer

class RPCServer(ThreadingMixIn, SimpleXMLRPCServer):  # 继承了多线程和rpc server的类
    pass

if __name__ == '__main__':
    server = RPCServer(('127.0.0.1', 8001))  # 类实例化
    d = dataHandler()
    fun = {'find_code': d.find_code,
           'check_code': d.check_code,
           'get_code_info': d.get_code_info,
           'find_parent_bom': d.find_parent_bom,
           'find_child_bom': d.find_child_bom,
           'update_to_bom_db': d.update_to_bom_db,
           'update_to_code_db': d.update_to_code_db,
           'update_to_cost_db': d.update_to_cost_db,
           'update_to_change_db': d.update_to_change_db, "update_to_drawpath_db": d.update_to_drawpath_db, 'find_in_bom': d.find_in_bom,
           'remove_assemble': d.remove_assemble,
           'read_design_BOM': d.read_design_BOM,
           'modify_excel': d.modify_excel,
           'view_changed_cost': d.view_changed_cost,
           'bom_add_cost': d.bom_add_cost,
           'recalc_tree_cost': d.recalc_tree_cost,
           'scan_path': d.scan_path,
           'find_db': d.find_db,
           'save_to_excel': d.save_to_excel,
           'download_template': d.download_template,
           'load_drawpath_db': d.load_drawpath_db,
           'get_root':d.get_root
           }

    for key,item in fun.items():
        server.register_function(item,key)  # 注册函数 
        print('->方法 %s 已注册'%key)

    print('server 已启动,等待连接...')
    server.serve_forever()  # 启动服务，等待连接
