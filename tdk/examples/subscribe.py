"""
SPDX-FileCopyrightText: 2024 Contributors to the Eclipse Foundation

See the NOTICE file(s) distributed with this work for additional
information regarding copyright ownership.

This program and the accompanying materials are made available under the
terms of the Apache License Version 2.0 which is available at

    http://www.apache.org/licenses/LICENSE-2.0

SPDX-License-Identifier: Apache-2.0
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import asyncio

from uprotocol.transport.ulistener import UListener
from uprotocol.v1.umessage_pb2 import UMessage

from tdk.apis.apis import TdkApis
from tdk.core import protobuf_autoloader
from tdk.examples import common_methods


class MyListener(UListener):
    async def on_receive(self, msg: UMessage):
        common_methods.logging.debug('on receive called')
        common_methods.logging.debug(msg.payload)
        common_methods.logging.debug(msg.attributes.__str__())


async def subscribe_if_subscription_service_is_running():
    status = await tdk_apis.subscribe(topic, listener)
    common_methods.logging.debug(f"Register Listener status  {status}")
    while True:
        await asyncio.sleep(1)


async def subscribe_if_subscription_service_is_not_running():
    status = await tdk_apis.register_listener(topic, listener)
    common_methods.logging.debug(f"Register Listener status  {status}")
    while True:
        await asyncio.sleep(1)


if __name__ == '__main__':
    # create topic uuri
    one_second_topic = "/example.hello_world/1/one_second#Timer"
    topic = protobuf_autoloader.get_uuri_from_name(one_second_topic)

    listener = MyListener()
    config = common_methods.get_transport_config()
    tdk_apis = TdkApis(config)
    # if subscription service is not available, use up-L1 (Transport) apis
    asyncio.run(subscribe_if_subscription_service_is_not_running())
    # if subscription service is running, use up-L2 (Communication) apis
