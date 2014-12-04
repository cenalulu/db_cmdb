#-*- encoding: utf8 -*-
import urllib2
import urllib
import json

class InstList:
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
        result = self.__call_interface__('CMDB', 'addinstane', json_obj=info)
        return result
