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
        except urllib2.URLError, e:
            if not json_obj:
                msg = 'Failed to call remote interface. Module: %s, Interface: %s, Error Message: %s'
                self.last_error = -1
                self.last_error_msg = msg % (module_name, interface_name, e)
            else:
                msg = 'Failed to call remote interface. Module: %s, Interface: %s, Query String: %s, Error Message: %s'
                json_str = json.dumps(json_obj)
                self.last_error = -1
                self.last_error_msg = msg % (module_name, interface_name, json_str, e)

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

    def init_system_with_mirror(self, info):
        info['template_id'] = 1
        info['flow_name'] = '数据库服务器系统初始化'
        result = self.__call_interface__('TEMPLATE', 'add_flow', json_obj=info)
        return result

    def save_server_info(self, info):
        result = self.__call_interface__('CMDB', 'serverstatechange/0', json_obj=info)
        return result

    def add_server(self, info):
        result = self.__call_interface__('CMDB', 'addserver', json_obj=info)
        return result

    def list_supported_mirror(self):
        result = self.__call_interface__('CMDB', 'getmirror')
        mirror_list = list()
        mirror_list.append('')
        if result:
            for mirror in result:
                mirror_list.append(mirror)
            return mirror_list
        else:
            return False

    def list_supported_env(self):
        result = self.__call_interface__('CMDB', 'getenv')
        env_list = list()
        env_list.append('')
        if result:
            for env in result:
                env_list.append(env)
            return env_list
        else:
            return False

    def list_supported_dba(self):
        query_obj = {"role": "DBA", "status": "在职"}
        result = self.__call_interface__('USER', 'getuser', json_obj=query_obj)
        dba_list = list()
        dba_list.append('')
        if result:
            for user in result:
                dba_list.append(user['realname'])
            return dba_list
        else:
            return False

    def list_supported_use_status(self):
        result = self.__call_interface__('CMDB', 'getusestatus')
        status_list = list()
        status_list.append('')
        if result:
            for status in result:
                status_list.append(status['status'])
            return status_list
        else:
            return False

    def list_supported_status(self):
        result = self.__call_interface__('CMDB', 'getserverstatus')
        status_list = list()
        status_list.append('')
        if result:
            for status in result:
                status_list.append(status['status'])
            return status_list
        else:
            return False

if __name__ == '__main__':
    test_server = ServerList()
    print test_server.list_all()
    print 'a'
