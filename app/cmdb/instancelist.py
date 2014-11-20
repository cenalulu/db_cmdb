import urllib2
import json

class InstList:
    api_addr = "http://192.168.222.156:5000/"

    def __init__(self):
        self.api_addr = "http://192.168.222.156:5000/"

    def list_all(self):
        data = ''
        try:
            fp = urllib2.urlopen(self.api_addr + 'CMDB/getinstanceinfo', data, timeout=1)
            result = json.load(fp)
            if result['status'] == 0:
                return result['data']
            else:
                return ''
        except urllib2.URLError:
            return 0

    def info_by_id(self, server_id):
        data = ''
        try:
            fp = urllib2.urlopen(self.api_addr + 'CMDB/getinstanceinfo?id=' + server_id, data, timeout=1)
            result = json.load(fp)
            if result['status'] == 0:
                return result['data']
            else:
                return ''
        except urllib2.URLError:
            return 0

    def list_mirror(self):
        data = ''
        try:
            fp = urllib2.urlopen(self.api_addr + 'CMDB/getmirror', data, timeout=1)
            result = json.load(fp)
            if result['status'] == 0:
                return result['data']
            else:
                return ''
        except urllib2.URLError:
            return 0

    def list_env(self):
        data = ''
        try:
            fp = urllib2.urlopen(self.api_addr + 'CMDB/getenv', data, timeout=1)
            result = json.load(fp)
            if result['status'] == 0:
                return result['data']
            else:
                return ''
        except urllib2.URLError:
            return 0

