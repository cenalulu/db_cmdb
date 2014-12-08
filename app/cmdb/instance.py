#-*- encoding: utf8 -*-
import urllib2
import urllib
import json
from cmdb_api_base import CmdbApiBase

class InstList(CmdbApiBase):

    def list_all(self, data=None):
        result = self.__call_interface__('CMDB', 'getinstanceinfo', json_obj=data)
        return result

    def list_supported_type(self):
        result = self.__call_interface__('CMDB', 'gettype')
        supported_list = list()
        supported_list.append('')
        if result:
            for entry in result:
                supported_list.append(entry['status'])
        else:
            return False
        return zip(supported_list, supported_list)

    def list_supported_dba(self):
        query_obj = {"role": "DBA", "status": "在职"}
        result = self.__call_interface__('USER', 'getuser', json_obj=query_obj)
        dba_list = list()
        dba_list.append('')
        if result:
            for user in result:
                dba_list.append(user['realname'])
        else:
            return False

        return zip(dba_list, dba_list)

    def list_supported_status(self):
        result = self.__call_interface__('CMDB', 'getinstancestatus')
        status_list = list()
        status_list.append('')
        if result:
            for status in result:
                status_list.append(status['status'])
        else:
            return False
        return zip(status_list, status_list)

    def info_by_id(self, instance_id):
        data = {"id": instance_id}
        result = self.__call_interface__('CMDB', 'getinstanceinfo', json_obj=data)
        return result

    def add_instance(self, info):
        result = self.__call_interface__('CMDB', 'addinstance', json_obj=info)
        return result

    def get_total_cnt(self):
        result = self.__call_interface__('CMDB', 'getinstancecount')
        return result
