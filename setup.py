#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2017-2020 by Sylvain Boily
# SPDX-License-Identifier: GPL-3.0+

from setuptools import find_packages
from setuptools import setup

setup(
    name='wazo_ui_opus',
    version='0.1',

    description='Wazo UI Opus Configuration',

    author='Sylvain Boily',
    author_email='sylvain@wazo.io',

    url='https://github.com/sboily/wazo-admin-ui-opus',

    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,

    entry_points={
        'wazo_ui.plugins': [
            'opus = wazo_ui_opus_quintana.plugin:Plugin',
        ]
    }
)

