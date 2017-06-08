# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+


from flask import render_template
from flask_menu.classy import register_flaskview
from flask_menu.classy import classy_menu_item

from wazo_admin_ui.helpers.plugin import create_blueprint
from wazo_admin_ui.helpers.classful import BaseView
from wazo_admin_ui.helpers.form import BaseForm

from wtforms.fields import SubmitField, StringField, SelectField, BooleanField
from wtforms.validators import InputRequired, Length

opus = create_blueprint('opus', __name__)


class Plugin(object):

    def load(self, dependencies):
        core = dependencies['flask']

        OpusConfigurationView.service = OpusService()
        OpusConfigurationView.register(opus, route_base='/opus_configuration')
        register_flaskview(opus, OpusConfigurationView)

        core.register_blueprint(opus)


class OpusForm(BaseForm):
    name = StringField('Name', [Length(max=128),])
    packet_loss = StringField('Packet Loss', [Length(max=128),]) # 0 - 100
    complexity = StringField('Complexity', [Length(max=128),]) # 0 - 10
    signal = SelectField('Application', choices=[('auto', 'Auto'), ('voice', 'Voice'), ('music', 'Music')])
    application = SelectField('Application', choices=[('voip', 'VOIP'), ('audio', 'Audio'), ('low_delay', 'Low Delay')])
    max_playback_rate = StringField('Max Playback Rate', [Length(max=128),]) # 8000 - 48000
    bitrate = StringField('Bite Rate', [Length(max=128),]) # 500 - 512000
    cbr = BooleanField('CBR')
    fec = BooleanField('FEC')
    dtx = BooleanField('DTX')
    submit = SubmitField('Submit')


class OpusConfigurationView(BaseView):

    form = OpusForm
    resource = 'opus'

    @classy_menu_item('.advanced.opus', 'Opus', order=9, icon="heart")
    def index(self):
        return super(OpusConfigurationView, self).index()


class OpusService(object):

    def list(self):
        return {'items': []}
