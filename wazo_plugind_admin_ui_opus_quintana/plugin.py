# -*- coding: utf-8 -*-
# Copyright 2017 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0+

from flask_menu.classy import register_flaskview

from wazo_admin_ui.helpers.plugin import create_blueprint
from flask import render_template

from flask_menu.classy import classy_menu_item
from wazo_admin_ui.helpers.classful import LoginRequiredView


opus = create_blueprint('opus', __name__)


class Plugin(object):

    def load(self, dependencies):
        core = dependencies['flask']

        OpusConfigurationView.register(opus, route_base='/opus_configuration')
        register_flaskview(opus, OpusConfigurationView)

        core.register_blueprint(opus)


class OpusConfigurationView(LoginRequiredView):

    @classy_menu_item('.advanced.opus', 'Opus', order=9, icon="heart")
    def index(self):
        return render_template('opus/index.html')

