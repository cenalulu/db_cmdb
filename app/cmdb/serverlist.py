#-*- encoding: utf8 -*-
__author__ = 'cenalulu'
import urllib2
import urllib
import json


class ServerList:
    api_addr = ""
    last_error = 0
    last_error_msg = ''


    def __init__(self, api_addr):
        self.api_addr = api_addr

    def __call_interface__(self, module_name, interface_name, json_obj=None):
        try:
            if json_obj:
                query_obj = {"data": json.dumps(json_obj)}
            else:
                query_obj = {"data": {}}
            encoded_data = urllib.urlencode(query_obj)
            fp = urllib2.urlopen(self.api_addr + module_name + '/' + interface_name, encoded_data, timeout=1)

            result = json.load(fp)
            if result['status'] == 0:
                return result['data']
            else:
                msg = 'Call remote interface return error. Module: %s, Interface: %s' \
                      ', Query String:%s, Error Code: %d, Error Message: %s'
                if not json_obj:
                    json_str = ''
                else:
                    json_str = json.dumps(json_obj)
                self.last_error = result['status']
                self.last_error_msg = msg % (module_name, interface_name, json_str, result['status'], result['data'])
                return tuple()
        except urllib2.URLError:
            msg = 'Failed to call remote interface. Module: %s, Interface: %s, Query String: %s'
            if not json_obj:
                json_str = ''
            else:
                json_str = json.dumps(json_obj)

            self.last_error = -1
            self.last_error_msg = msg % (module_name, interface_name, json_str)
            return tuple()

    def is_last_call_error(self):
        if self.last_error == 0:
            return False
        else:
            return True

    def get_last_error(self):
        last_error_msg = self.last_error_msg
        self.last_error = 0
        self.last_error_msg = ''
        return last_error_msg

    def list_all(self, data=None):
        result = self.__call_interface__('CMDB', 'getserverinfo', json_obj=data)
        return result

    def delete_by_id(self, server_id):
        data = {"server_id": server_id}
        result = self.__call_interface__('CMDB', 'deleteserver', json_obj=data)
        return result

    def info_by_id(self, server_id):
        data = {"server_id": server_id}
        result = self.__call_interface__('CMDB', 'getserverinfo', json_obj=data)
        return result

    def save_server_info(self, info):
        result = self.__call_interface__('CMDB', 'serverstatechange/0', json_obj=info)
        return result

    def add_server(self, info):
        result = self.__call_interface__('CMDB', 'addserver', json_obj=info)
        return result

    def list_supported_mirror(self):
        result = self.__call_interface__('CMDB', 'getmirror')
        return result

    def list_supported_env(self):
        result = self.__call_interface__('CMDB', 'getenv')
        return result

    def list_supported_use_status(self):
        use_status_list = ['已用', '待用']
        return use_status_list

    def list_supported_status(self):
        status_list = ['未初始化系統',  '系統初始化中', '系統已初始化', '上線前配置中', '在线' ,'DBA維護中', '服務器維護中', '下线']
        return status_list

if __name__ == '__main__':
    test_server = ServerList()
    print test_server.list_all()
    print 'a'
