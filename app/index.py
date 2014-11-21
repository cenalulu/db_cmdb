# coding: utf8
from flask import Flask, render_template, request, url_for
from cmdb.serverlist import ServerList
from cmdb.instancelist import InstList
from cmdb.server_info_form import ServerInfoForm
import urllib2
import urllib
import json

import sys
reload(sys)
sys.setdefaultencoding('utf8')



app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'cenalulu'


@app.route("/blank")
def blank():
    data = dict({'page_name': 'DashBoard'})
    return render_template('blank.html', data=data)


@app.route("/serverinfotest")
def server_info_test():
    server_form = ServerInfoForm()
    return render_template("serverinfotest.html", form=server_form)


@app.route("/addserver/", methods=['GET', 'POST'])
def add_server():
    server_form = ServerInfoForm()
    data = dict()
    if request.method == 'POST':
        server_post = request.form
        server = ServerList()
        result = server.add_server(server_post)
        page_data = dict()
        page_data['add_result'] = dict()
        if result['status'] != 0:
            page_data['add_result']['status'] = -1
            if result.has_key('data'):
                page_data['add_result']['msg'] = "[Failed]:" + result['data']
            else:
                page_data['add_result']['msg'] = "[Failed]: Unknown CMDB API error"
        else:
            page_data['add_result']['status'] = 0
            page_data['add_result']['msg'] = "[Success]: Add Server Succeed"
        data['form_data'] = server_post
    else:
        page_data = ''
        data['form_data'] = dict()
    data['page_name'] = 'Add Server'
    data['form'] = server_form
    data['page_data'] = page_data
    return render_template('addserver.html', data=data)


@app.route("/serverinfo/<server_id>", methods=['GET', 'POST'])
def server_info(server_id=None):
    if request.method == 'POST':
        page_data = request.form
    else:
        if not server_id or server_id == 0:
            page_data = ''
        else:
            host_info = ServerList()
            page_data = host_info.info_by_id(server_id)
    server_form = ServerInfoForm()
    data = dict()
    data['page_name'] = 'Server Info'
    data['form'] = server_form
    data['page_data'] = page_data
    return render_template('serverinfo.html', data=data)


@app.route('/servermodify', methods=['GET', 'POST'])
def servermodify():
    return render_template('servermodify.html')


@app.route("/instancelist/")
def instance_list():
    inst_list = InstList()
    page_data = inst_list.list_all()
    message_list = ({'from': 'admin', 'time': '2013-01-01', 'content': 'This is a test message'},)
    task_list = ({'name': 'task 1', 'progress': 10},)
    data = dict()
    data['message_list'] = message_list
    data['task_list'] = task_list
    data['page_name'] = 'Instance List'
    data['page_data'] = page_data

    return render_template('instancelist.html', data=data)


@app.route("/serverlist")
def server_list():
    conf_list = ServerList()
    page_data = conf_list.list_all()
    message_list = ({'from': 'admin', 'time': '2013-01-01', 'content': 'This is a test message'},)
    task_list = ({'name': 'task 1', 'progress': 10},)

    data = dict()
    data['message_list'] = message_list
    data['task_list'] = task_list
    data['page_name'] = 'Machine List'
    data['page_data'] = page_data
    return render_template('serverlist.html', data=data)


@app.route("/")
def index():
    data = dict()
    message_list = ({'from': 'admin', 'time': '2013-01-01', 'content': 'This is a test message'},)
    task_list = ({'name': 'task 1', 'progress': 10},)
    data['message_list'] = message_list
    data['task_list'] = task_list
    data['page_name'] = 'Dash Board'
    return render_template('frame.html', data=data)


@app.route("/mmmlist")
def mmm_list():
    message_list = ({'from': 'admin', 'time': '2013-01-01', 'content': 'This is a test message'},)
    task_list = ({'name': 'task 1', 'progress': 10},)

    data = dict()
    data['message_list'] = message_list
    data['task_list'] = task_list
    data['page_name'] = 'ToDo'
    return render_template('mmmlist.html', data=data)

if __name__ == "__main__":
    app.run('0.0.0.0')

