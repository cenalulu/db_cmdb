# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
import wtforms


class ServerInfoForm(Form):
    server_id = wtforms.StringField('SerialNO', validators=[])
    server_ip = wtforms.StringField('Server IP', validators=[wtforms.validators.IPAddress()])
    server_name = wtforms.StringField('Hostname', validators=[wtforms.validators.DataRequired()])
    mirror = wtforms.SelectField('System Type', validators=[], choices=[])
    env = wtforms.SelectField('Environment', validators=[], choices=[])
    server_status = wtforms.SelectField('Status', validators=[], choices=[])
    use_status = wtforms.SelectField('Use Status', validators=[], choices=[])
    owner = wtforms.SelectField('Owner', validators=[], choices=[])


if __name__ == '__main__':
    test = ServerInfoForm()

