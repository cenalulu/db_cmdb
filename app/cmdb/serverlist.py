__author__ = 'cenalulu'
import urllib2
import urllib
import json


class ServerList:
    api_addr = "http://192.168.222.156:5000/"

    def __init__(self):
        self.api_addr = "http://192.168.222.156:5000/"

    def info_by_id(self, server_id):
        data = {"id": server_id}
        encoded_data = urllib.urlencode(data)
        try:
            fp = urllib2.urlopen(self.api_addr + 'CMDB/getserverinfo', encoded_data, timeout=1)
            result = json.load(fp)
            if result['status'] == 0:
                return result['data'][0]
            else:
                return ''
        except urllib2.URLError:
            return 0

    def add_server(self, info):
        request_str = json.dumps(info)
        data = {"serverjson": request_str}
        encoded_data = urllib.urlencode(data)

        try:
            fp = urllib2.urlopen(self.api_addr + 'CMDB/addservice', encoded_data, timeout=1)
            result = json.load(fp)
            return result
        except urllib2.URLError:
            return {"status": -1, "data": "Failed to access remote API"}

    def list_all(self):
        data = ''
        try:
            fp = urllib2.urlopen(self.api_addr + 'CMDB/getserverinfo', data, timeout=1)
            result = json.load(fp)
            if result['status'] == 0:
                return result['data']
            else:
                return ''
        except urllib2.URLError:
            return 0

if __name__ == '__main__':
    test_server = ServerList()
    print test_server.list_all()
    print 'a'
