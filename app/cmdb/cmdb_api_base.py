# coding: utf-8

import urllib2
import urllib
import json


class CmdbApiCallException(Exception):
    def __init__(self, error_no=0, msg='', module='', interface='', param=''):
        self.error_no = error_no
        self.message = msg
        self.module = module
        self.interface = interface
        self.param = param

    def detail_msg(self):
        template_msg = "CMDB API Error: Module %s; Interface %s; Error Code: %s; Message: %s"
        msg = template_msg % (self.module, self.interface, self.error_no, self.message)
        return msg


class CmdbApiBase:
    __api_addr = ""
    __last_error = 0
    __last_error_msg = ''

    def __init__(self, __api_addr):
        self.__api_addr = __api_addr

    def __call_interface__(self, module_name, interface_name, json_obj=None):
        """

        :rtype : dict
        """
        try:
            param_json_str = ''
            if json_obj:
                param_json_str = json.dumps(json_obj)
                query_obj = {"data": json.dumps(json_obj)}
            else:
                query_obj = {"data": {}}
            encoded_data = urllib.urlencode(query_obj)
            fp = urllib2.urlopen(self.__api_addr + module_name + '/' + interface_name, encoded_data, timeout=1)

            result = json.load(fp)
            if not result:
                raise CmdbApiCallException(error_no=0, msg="Result from remote api is not a valid json str",
                                           module=module_name, interface=interface_name, param=param_json_str)

            if result['status'] == 0:
                return result['data']
            else:
                raise CmdbApiCallException(error_no=result['status'], msg=result['data'],
                                           module=module_name, interface=interface_name, param=param_json_str)
        except urllib2.URLError, e:
            raise CmdbApiCallException(error_no=e.errno, msg=e.args[0],
                                       module=module_name, interface=interface_name, param=e.args[0])

