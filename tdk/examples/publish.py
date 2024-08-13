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

from uprotocol.communication.calloptions import CallOptions
from uprotocol.communication.upayload import UPayload
from uprotocol.v1.uri_pb2 import UUri

from simulator.mockservices.hello_world import HelloWorldService
from tdk.apis.apis import TdkApis
from tdk.examples import common_methods


async def publish_to_zenoh():
    # create topic uuri
    topic = UUri(ue_id=4, ue_version_major=1, resource_id=0x8000)

    # payload to publish UPayload.pack(/*your proto payload*/)
    payload = UPayload.pack(UUri())

    config = common_methods.get_transport_config()
    tdk_apis = TdkApis(config)

    status = await tdk_apis.publish(topic, CallOptions.DEFAULT, payload)
    common_methods.logging.debug(f"Publish status {status}")
    # Sleep for 3 seconds to simulate delay
    await asyncio.sleep(3)


async def publish_to_one_second_event_to_zenoh():
    config = common_methods.get_transport_config()
    tdk_apis = TdkApis(config)

    # create topic uuri
    one_second_topic = "/example.hello_world/1/one_second#Timer"
    timer_data = {'resource_id': 'one_second', 'time.hours': 2, 'time.minutes': 1, 'time.nanos': 2, 'time.seconds': 3}

    # start service
    service = HelloWorldService(transport_config=config, tdk_apis=tdk_apis)
    await service.start()

    status = await service.publish(one_second_topic, timer_data)
    common_methods.logging.debug(f"Publish status {status}")
    await asyncio.sleep(3)


if __name__ == '__main__':
    asyncio.run(publish_to_one_second_event_to_zenoh())
