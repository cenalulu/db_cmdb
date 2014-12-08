# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
import wtforms
from server import ServerList


class ServerInitForm(Form):
    server_id = wtforms.StringField('SerialNO', validators=[])
    server_ip = wtforms.StringField('Server IP', validators=[wtforms.validators.IPAddress()])
    mirror = wtforms.SelectField('Mirror', validators=[], choices=[])
    comment = wtforms.TextAreaField('Memo', validators=[])

class ServerInfoForm(Form):
    server_id = wtforms.StringField('SerialNO', validators=[])
    server_ip = wtforms.StringField('Server IP', validators=[wtforms.validators.IPAddress()])
    server_name = wtforms.StringField('Hostname', validators=[wtforms.validators.DataRequired()])
    use_status = wtforms.SelectField('Use Status', validators=[], choices=[])
    server_status = wtforms.SelectField('Status', validators=[], choices=[])
    mirror = wtforms.SelectField('Mirror', validators=[], choices=[])
    env = wtforms.SelectField('Env', validators=[], choices=[])
    owner = wtforms.SelectField('Owner', validators=[], choices=[])

class InstanceInfoForm(Form):
    server_id = wtforms.StringField('SerialNO', validators=[])
    server_ip = wtforms.StringField('Server IP', validators=[wtforms.validators.IPAddress()])
    port = wtforms.StringField('Instance Port', validators=[])
    status = wtforms.SelectField('Status', validators=[], choices=[])
    type = wtforms.SelectField('Type', validators=[], choices=[])
    dba_owner = wtforms.SelectField('DBA Owner', validators=[], choices=[])
    biz_owner = wtforms.StringField('Biz Owner', validators=[])


if __name__ == '__main__':
    test = ServerInfoForm()

