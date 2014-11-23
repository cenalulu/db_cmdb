# coding: utf8
from flask import Flask, render_template, request, url_for
from cmdb.serverlist import ServerList
from cmdb.instancelist import InstList
from cmdb.server_info_form import ServerInfoForm
from config import app_config

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


@app.route("/addserver/", methods=['GET', 'POST'])
def add_server():
    host_info = ServerList(app.config['CMDB_API_ADDR'])
    env = host_info.list_supported_env()
    mirror = host_info.list_supported_mirror()
    use_status = host_info.list_supported_use_status()
    status = host_info.list_supported_status()
    env = zip(env, env)
    mirror = zip(mirror, mirror)

    server_form = ServerInfoForm()
    server_form.env.choices = env
    server_form.mirror.choices = mirror
    server_form.server_status.choices = status
    server_form.use_status.choices = use_status
    data = dict()
    if request.method == 'POST':
        server_post = request.form
        server = ServerList(app.config['CMDB_API_ADDR'])
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
            data['notification'] = [{'level': 'success', 'msg': 'Add Server Success!'}]
        data['form_data'] = server_post
    else:
        page_data = ''
        data['form_data'] = dict()
    data['page_name'] = 'Add Server'
    data['form'] = server_form
    data['page_data'] = page_data
    return render_template('addserver.html', data=data)


@app.route("/serverinfo/<server_id>")
def server_info(server_id=None):
    data = dict()
    host_info = ServerList(app.config['CMDB_API_ADDR'])
    single_server_info = dict()

    query_result = host_info.info_by_id(server_id)
    if not query_result:
        data['notification'] = [{'level': 'danger', 'msg': host_info.get_last_error()}]
    else:
        single_server_info = query_result[0]

    data['page_data'] = single_server_info
    data['page_data']['server_id'] = server_id
    data['page_name'] = 'Server Info'
    return render_template('serverinfo.html',data=data)


@app.route("/serverinfoedit/<server_id>", methods=['GET', 'POST'])
def server_info_edit(server_id=None):
    host_info = ServerList(app.config['CMDB_API_ADDR'])
    if request.method == 'POST':
        page_data = request.form
    else:
        if not server_id or server_id == 0:
            page_data = ''
        else:
            page_data = host_info.info_by_id(server_id)
    env = host_info.list_supported_env()
    mirror = host_info.list_supported_mirror()
    use_status = host_info.list_supported_use_status()
    status = host_info.list_supported_status()
    env = zip(env, env)
    mirror = zip(mirror, mirror)
    status = zip(status, status)
    use_status = zip(use_status, use_status)

    server_form = ServerInfoForm()
    server_form.env.choices = env
    server_form.mirror.choices = mirror
    server_form.server_status.choices = status
    server_form.use_status.choices = use_status
    data = dict()
    data['page_name'] = 'Server Info'
    data['form'] = server_form
    data['page_data'] = page_data
    return render_template('serverinfoedit.html', data=data)


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
    data = dict()
    all_servers = ServerList(app.config['CMDB_API_ADDR'])
    page_data = all_servers.list_all()
    if all_servers.is_last_call_error():
        data['notification'] = [{'level': 'danger', 'msg': all_servers.get_last_error()}]
    message_list = ({'from': 'admin', 'time': '2013-01-01', 'content': 'This is a test message'},)
    task_list = ({'name': 'task 1', 'progress': 10},)

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
    app.jinja_env.cache = None
    app.config.from_object(app_config)
    app.run(host='0.0.0.0', port=app.config['PORT'])

