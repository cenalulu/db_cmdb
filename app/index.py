# coding: utf8
from flask import Flask, render_template, request, url_for, redirect, flash
from cmdb.serverlist import ServerList
from cmdb.instancelist import InstList
from cmdb.server_info_form import ServerInfoForm, ServerInitForm
from config import app_config

import sys

reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'cenalulu'


@app.route("/backup")
def backup():
    data = dict({'page_name': 'Backup Center'})
    return render_template('blank.html', data=data)


@app.route("/recover")
def recover():
    data = dict({'page_name': 'Backup Center'})
    return render_template('blank.html', data=data)


@app.route("/metrics")
def metrics():
    data = dict({'page_name': 'Metrics'})
    return render_template('blank.html', data=data)


@app.route("/slowlog")
def slowlog():
    data = dict({'page_name': 'Slow Query'})
    return render_template('blank.html', data=data)


@app.route("/querymonitor")
def query_monitor():
    data = dict({'page_name': 'Query Monitor'})
    return render_template('blank.html', data=data)


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
    owner = host_info.list_supported_dba()
    env = zip(env, env)
    mirror = zip(mirror, mirror)
    use_status = zip(use_status, use_status)
    owner = zip(owner, owner)
    status = host_info.list_supported_status()
    if status:
        status = zip(status, status)
    else:
        flash(host_info.get_last_error(), 'danger')
        status = tuple()

    server_form = ServerInfoForm()
    server_form.env.choices = env
    server_form.mirror.choices = mirror
    server_form.server_status.choices = status
    server_form.use_status.choices = use_status
    server_form.owner.choices = owner
    data = dict()
    if request.method == 'POST':
        server_post = request.form
        server_info = ServerList(app.config['CMDB_API_ADDR'])
        result = server_info.add_server(server_post)
        page_data = dict()
        page_data['add_result'] = dict()
        if not result:
            flash(server_info.get_last_error(), 'danger')
        else:
            flash('Add Server Success!', 'success')
            return redirect(url_for('server_info', server_id=request.form['server_id']))
        data['form_data'] = server_post
    else:
        page_data = ''
        data['form_data'] = dict()
    data['page_name'] = 'Add Server'
    data['form'] = server_form
    data['page_data'] = page_data
    return render_template('addserver.html', data=data)


@app.route("/deleteserver/<server_id>")
def delete_server(server_id=None):
    host_info = ServerList(app.config['CMDB_API_ADDR'])

    query_result = host_info.delete_by_id(server_id)
    if not query_result:
        flash(host_info.get_last_error(), 'danger')
        return redirect(url_for('server_info', server_id=server_id))
    else:
        flash('Delete Server Success', 'success')
        return redirect(url_for('server_list'))


@app.route("/serverinfo/<server_id>")
def server_info(server_id=None):
    data = dict()
    host_info = ServerList(app.config['CMDB_API_ADDR'])
    single_server_info = dict()

    query_result = host_info.info_by_id(server_id)
    if not query_result:
        flash(host_info.get_last_error(), 'danger')
    else:
        single_server_info = query_result[0]

    data['page_data'] = single_server_info
    data['page_data']['server_id'] = server_id
    data['page_name'] = 'Server Info'
    return render_template('serverinfo.html', data=data)


def fill_init_server_form(server_form=None, mirror=''):
    host_info = ServerList(app.config['CMDB_API_ADDR'])

    mirror_list = host_info.list_supported_mirror()
    mirror_list = zip(mirror_list, mirror_list)
    server_form.mirror.choices = mirror_list

    if not mirror: mirror = ''
    server_form.mirror.data = mirror
    return server_form

def fill_server_info_form(server_form=None, env='', mirror='', server_status='', use_status='', owner=''):
    host_info = ServerList(app.config['CMDB_API_ADDR'])

    env_list = host_info.list_supported_env()
    mirror_list = host_info.list_supported_mirror()
    use_status_list = host_info.list_supported_use_status()
    server_status_list = host_info.list_supported_status()
    owner_list = host_info.list_supported_dba()
    env_list = zip(env_list, env_list)
    mirror_list = zip(mirror_list, mirror_list)
    server_status_list = zip(server_status_list, server_status_list)
    use_status_list = zip(use_status_list, use_status_list)
    owner_list = zip(owner_list, owner_list)
    server_form.env.choices = env_list
    server_form.mirror.choices = mirror_list
    server_form.server_status.choices = server_status_list
    server_form.use_status.choices = use_status_list
    server_form.owner.choices = owner_list

    if not env: env = ''
    if not mirror: mirror = ''
    if not owner: owner = ''
    if not server_status: server_status = ''
    if not use_status: use_status = ''
    server_form.env.data = env
    server_form.mirror.data = mirror
    server_form.owner.data = owner
    server_form.server_status.data = server_status
    server_form.use_status.data = use_status
    return server_form


@app.route("/initsystem/<server_id>", methods=['GET', 'POST'])
def init_system(server_id=None):
    data = dict()
    host_info = ServerList(app.config['CMDB_API_ADDR'])
    if request.method == 'POST':
        request_dict = dict()
        request_dict['server_id'] = request.form.get('server_id')
        request_dict['ip'] = request.form.get('server_ip')
        request_dict['mirror'] = request.form.get('mirror')
        request_dict['comment'] = request.form.get('comment')
        result = host_info.init_system_with_mirror(request_dict)
        if not result:
            flash(host_info.get_last_error(), 'danger')
        else:
            flash('System initial request sent', 'success')
    else:
        if not server_id or server_id == 0:
            page_data = ''

    page_data = host_info.info_by_id(server_id)[0]
    server_form = ServerInitForm()
    if request.form.get('mirror', False):
        server_form = fill_init_server_form(server_form, request.form.get('mirror', ''))
    else:
        server_form = fill_init_server_form(server_form, mirror=page_data['mirror'])
    data['page_name'] = 'Server Info'
    data['form'] = server_form
    data['page_data'] = page_data
    return render_template('init_system.html', data=data)

@app.route("/serverinfoedit/<server_id>", methods=['GET', 'POST'])
def server_info_edit(server_id=None):
    data = dict()
    host_info = ServerList(app.config['CMDB_API_ADDR'])
    if request.method == 'POST':
        page_data = request.form
        result = host_info.save_server_info(page_data)
        if not result:
            flash(host_info.get_last_error(), 'danger')
        else:
            flash('Edit Server Information Success', 'success')
    else:
        if not server_id or server_id == 0:
            page_data = ''
        else:
            page_data = host_info.info_by_id(server_id)[0]

    server_form = ServerInfoForm()
    supported_select_key = ['owner', 'mirror', 'server_status', 'env']
    fill_select_data = dict()
    for key in supported_select_key:
        fill_select_data[key] = page_data[key]
    server_form = fill_server_info_form(server_form=server_form, **fill_select_data)
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
    supported_query_key = ['owner', 'mirror', 'server_status', 'env', 'use_status']
    query_condition = dict()
    all_servers = ServerList(app.config['CMDB_API_ADDR'])
    for key in supported_query_key:
        request_value = request.args.get(key, False)
        if request_value:
            query_condition[key] = request_value

    page_data = all_servers.list_all(data=query_condition)
    if all_servers.is_last_call_error():
        flash(all_servers.get_last_error(), 'danger')

    filter_form = ServerInfoForm()
    filter_form = fill_server_info_form(server_form=filter_form, **query_condition)

    message_list = ({'from': 'admin', 'time': '2013-01-01', 'content': 'This is a test message'},)
    task_list = ({'name': 'task 1', 'progress': 10},)
    data['message_list'] = message_list
    data['task_list'] = task_list
    data['page_name'] = 'Machine List'
    data['page_data'] = page_data
    data['filter_form'] = filter_form
    return render_template('serverlist.html', data=data)


@app.route("/")
def dashboard():
    data = dict()
    message_list = ({'from': 'admin', 'time': '2013-01-01', 'content': 'This is a test message'},)
    task_list = ({'name': 'task 1', 'progress': 10},)
    data['message_list'] = message_list
    data['task_list'] = task_list
    data['page_name'] = 'Dash Board'
    return render_template('dashboard.html', data=data)


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

