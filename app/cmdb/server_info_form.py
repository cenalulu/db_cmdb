# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
import wtforms

class ServerInfoForm(Form):
    server_id = wtforms.StringField('SerialNO', validators=[])
    server_ip = wtforms.StringField('Server IP', validators=[wtforms.validators.IPAddress()])
    server_name = wtforms.StringField('Hostname', validators=[wtforms.validators.DataRequired()])
    system_type = wtforms.StringField('System Type', validators=[])
    env = wtforms.StringField('Environment', validators=[])
    server_status = wtforms.StringField('Status', validators=[])
    use_status = wtforms.SelectField('Use Status', validators=[], choices=[(1, '已使用'), (2, '待用')] )
    owner = wtforms.StringField('Owner', validators=[])

if __name__ == '__main__':
    test = ServerInfoForm()

