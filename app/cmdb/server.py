#-*- encoding: utf8 -*-
__author__ = 'cenalulu'
import urllib2
import urllib
import json
from cmdb_api_base import CmdbApiBase

class ServerList(CmdbApiBase):

    def list_all(self, data=None):
        result = self.__call_interface__('CMDB', 'getserverinfo', json_obj=data)
        return result

    def online_by_id(self, server_id):
        data = {
            "server_id": server_id,
            "server_status": "在线"
        }
        result = self.__call_interface__('CMDB', 'serverstatechange/0', json_obj=data)
        return result

    def offline_by_id(self, server_id):
        data = {
            "server_id": server_id,
            "server_status": "下线"
        }
        result = self.__call_interface__('CMDB', 'serverstatechange/0', json_obj=data)
        return result

    def delete_by_id(self, server_id):
        data = {"server_id": server_id}
        result = self.__call_interface__('CMDB', 'deleteserver', json_obj=data)
        return result

    def machine_info_by_id(self, server_id):
        data = {"server_id": server_id}
        result = self.__call_interface__('CMDB', 'getengineinfo', json_obj=data)
        return result

    def info_by_id(self, server_id):
        data = {"server_id": server_id}
        result = self.__call_interface__('CMDB', 'getserverinfo', json_obj=data)
        return result

    def get_ip_by_id(self, server_id=None):
        data = {"server_id": server_id}
        result = self.__call_interface__('CMDB', 'getserverinfo', json_obj=data)
        return result[0]['server_ip']

    def init_system_with_mirror(self, info):
        result = self.__call_interface__('CMDB', 'init_system', json_obj=info)
        return result

    def save_server_info(self, info):
        result = self.__call_interface__('CMDB', 'serverstatechange/0', json_obj=info)
        return result

    def get_total_cnt(self):
        result = self.__call_interface__('CMDB', 'getservercount')
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
            return zip(mirror_list, mirror_list)
        else:
            return False

    def list_supported_env(self):
        result = self.__call_interface__('CMDB', 'getenv')
        env_list = list()
        env_list.append('')
        if result:
            for env in result:
                env_list.append(env)
            return zip(env_list,env_list)
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
            return zip(dba_list, dba_list)
        else:
            return False

    def list_supported_use_status(self):
        result = self.__call_interface__('CMDB', 'getusestatus')
        status_list = list()
        status_list.append('')
        if result:
            for status in result:
                status_list.append(status['status'])
            return zip(status_list, status_list)
        else:
            return False

    def list_supported_status(self):
        result = self.__call_interface__('CMDB', 'getserverstatus')
        status_list = list()
        status_list.append('')
        if result:
            for status in result:
                status_list.append(status['status'])
            return zip(status_list, status_list)
        else:
            return False

if __name__ == '__main__':
    test_server = ServerList()
    print test_server.list_all()
    print 'a'
