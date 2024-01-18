# -------------------------------------------------------------------------
#
# Copyright (c) 2023 General Motors GTO LLC
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
# SPDX-FileType: SOURCE
# SPDX-FileCopyrightText: 2023 General Motors GTO LLC
# SPDX-License-Identifier: Apache-2.0
#
# -------------------------------------------------------------------------

import json
import os
from urllib.parse import unquote

from flask import redirect, url_for, render_template, request

from simulatorui import blueprint
from simulatorui.utils import adb_utils
from utils.constant import FILENAME_RPC_LOGGER, FILENAME_PUBSUB_LOGGER


@blueprint.route('/')
def route_default():
    return redirect(url_for('simulator_blueprint.route_configuration'))


@blueprint.route('/configuration.html')
def route_configuration():
    deviceInfo = {'Image': "", 'Build_date': "", 'Build_id': "", 'Model': ""}
    emu_status = 'Emulator is not running'
    try:
        device = adb_utils.get_emulator_device()
        if device is not None:
            status = device.shell("getprop init.svc.bootanim")
            if status.__contains__('stopped'):
                emu_status = 'Emulator is running'
                os.system("adb forward tcp:6095 tcp:6095")
                deviceInfo = {'Image': device.shell("getprop ro.product.bootimage.name"),
                              'Build_date': device.shell("getprop ro.bootimage.build.date"),
                              'Build_id': device.shell("getprop ro.bootimage.build.id"),
                              'Model': device.shell("getprop ro.product.model")}
            else:
                emu_status = 'Emulator is loading'


    except Exception:
        pass

    return render_template('home/configuration.html', segment=get_segment(request), deviceInfo=deviceInfo,
                           emu_status=emu_status)


@blueprint.route('/pub-sub.html')
def route_pubsub():
    services_json_path = os.getcwd() + os.sep + "simulatorui" + os.sep + "services.json"
    pubsub_json_path = os.getcwd() + os.sep + "simulatorui" + os.sep + "pub-sub.json"

    if 'simulatorui' in os.getcwd():
        pubsub_json_path = os.sep + "pub-sub.json"
        services_json_path = os.sep + "services.json"
    f = open(pubsub_json_path)
    pubsub = json.load(f)
    f.close()
    f = open(services_json_path)
    services = json.load(f)
    f.close()

    return render_template('home/pub-sub.html', segment=get_segment(request), services=services, pubsub=pubsub,
                           json_proto={})


@blueprint.route('/rpc-logger.html')
def start_rpc_dashboard():
    try:
        f = open(os.path.join(os.getcwd(), FILENAME_RPC_LOGGER))
        data = f.read()
        f.close()
    except:
        data = ''
    return render_template('home/rpc-logger.html', rpc_calls=data, segment=get_segment(request))


@blueprint.route('/pub-sub-logger.html')
def pub_dashboard():
    try:
        f = open(os.path.join(os.getcwd(), FILENAME_PUBSUB_LOGGER))
        data = f.read()
        f.close()
    except:
        data = ''
    return render_template('home/pub-sub-logger.html', data=data, segment=get_segment(request))


@blueprint.route('/send-rpc.html')
def route_sendrpc():
    rpc_json_path = os.getcwd() + os.sep + "simulatorui" + os.sep + "rpc.json"
    services_json_path = os.getcwd() + os.sep + "simulatorui" + os.sep + "services.json"

    if 'simulatorui' in os.getcwd():
        rpc_json_path = os.sep + "rpc.json"
        services_json_path = os.sep + "services.json"

    f = open(rpc_json_path)
    rpcs = json.load(f)
    f.close()
    f = open(services_json_path)
    services = json.load(f)
    f.close()

    return render_template('home/send-rpc.html', segment=get_segment(request), services=services, rpcs=rpcs)


@blueprint.route('/mockservice.html')
def route_mockservices():
    return render_template('home/mockservice.html', segment=get_segment(request))


# Helper - Extract current page name from request
def get_segment(request):
    try:
        segment = request.path.split('/')[-1]
        if segment == '':
            segment = 'index'
        return segment
    except:
        return None


@blueprint.route('/getuiconfiguration')
def getconfiguration():
    try:
        resource = str(request.args.get('resource'))
        service = str(unquote(request.args.get('service')))
        ui = json.loads(service)
        layout = None
        for i in ui:
            for key, value in i.items():
                if resource == key:
                    layout = value
                    break

        return layout
    except Exception as e:
        print(f'Exception:{e}')
        return None


@blueprint.route('/getmockservices')
def get_mock_services():
    mockservice_pkgs = []
    running_services = []
    json_path = os.getcwd() + os.sep + "simulatorui" + os.sep + "services.json"
    if 'simulatorui' in os.getcwd():
        json_path = os.sep + "services.json"
    f = open(json_path)
    mockservices = json.load(f)
    f.close()
    for m in mockservices:
        pkgs = {'entity': m['name'], 'name': m['display_name']}
        mockservice_pkgs.append(pkgs)

    if os.path.isfile("service_status.txt"):
        with open('service_status.txt', 'r+') as f:
            lines = f.read()
            running_services = json.loads(lines)

    return {'result': True, 'pkgs_mock': mockservice_pkgs, 'running': running_services}
