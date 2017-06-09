# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+


import ConfigParser
import requests 
import json

from flask import render_template
from flask_menu.classy import register_flaskview
from flask_menu.classy import classy_menu_item

from wazo_admin_ui.helpers.plugin import create_blueprint
from wazo_admin_ui.helpers.classful import BaseView
from wazo_admin_ui.helpers.form import BaseForm

from wtforms.fields import SubmitField, StringField, SelectField, BooleanField
from wtforms.validators import InputRequired, Length, NumberRange

opus = create_blueprint('opus', __name__)

config_file = '/etc/asterisk/codecs.d/opus_via_ui.conf'


class Plugin(object):

    def load(self, dependencies):
        core = dependencies['flask']

        OpusConfigurationView.service = OpusService()
        OpusConfigurationView.register(opus, route_base='/opus_configuration')
        register_flaskview(opus, OpusConfigurationView)

        core.register_blueprint(opus)


class OpusForm(BaseForm):
    name = StringField('Name', [InputRequired, Length(max=128)])
    packet_loss = StringField('Packet Loss', [NumberRange(min=0, max=100),])
    complexity = StringField('Complexity', [NumberRange(min=0, max=10),]) # 0 - 10
    signal = SelectField('Signal', choices=[('', 'Select...'), ('auto', 'Auto'), ('voice', 'Voice'), ('music', 'Music')])
    application = SelectField('Application', choices=[('', 'Select...'), ('voip', 'VOIP'), ('audio', 'Audio'), ('low_delay', 'Low Delay')])
    max_playback_rate = StringField('Max Playback Rate', [NumberRange(min=800, max=48000),])
    bitrate = StringField('Bite Rate', [NumberRange(min=500, max=512000),])
    cbr = BooleanField('CBR')
    fec = BooleanField('FEC')
    dtx = BooleanField('DTX')
    submit = SubmitField('Submit')


class OpusConfigurationView(BaseView):

    form = OpusForm
    resource = 'opus'

    @classy_menu_item('.advanced.opus', 'Opus', order=9, icon="compress")
    def index(self):
        return super(OpusConfigurationView, self).index()


class OpusService(object):

    def list(self):
        config = {'items': self._read_sections()}
        print config
        return config

    def create(self, resource):
        self._create_section(resource)
        self._reload_asterisk()
        return True

    def delete(self, section):
        self._remove_section(section)
        self._reload_asterisk()

    def _read_sections(self):
        config = ConfigParser.RawConfigParser()
        config.read(config_file)
        return [dict(config.items(s), name=s) for s in config.sections()]

    def _create_section(self, resource):
        config = ConfigParser.RawConfigParser()
        section = resource['name']
        config.add_section(section)
        config.set(section, 'type', 'opus')
        options = [
            'packet_loss',
            'complexity',
            'signal',
            'application',
            'max_playback_rate',
            'bitrate',
            'cbr',
            'fec',
            'dtx'
        ]
        for option in options:
            self._add_option(config, section, option, resource)

        with open(config_file, 'a+') as configfile:
            config.write(configfile)

    def _add_option(self, config, section, name, resource):
        if resource.get(name):
            config.set(section, name, resource.get(name))

    def _remove_section(self, section):
        config = ConfigParser.RawConfigParser()
        config.read(config_file)
        config.remove_section(section)

        with open(config_file, 'wb') as configfile:
            config.write(configfile)

    def _reload_asterisk(self):
        uri = 'http://localhost:8668/services'
        headers = {'content-type': 'application/json'}
        service = {'asterisk': 'reload'}
        req = requests.post(uri, data=json.dumps(service), headers=headers)
