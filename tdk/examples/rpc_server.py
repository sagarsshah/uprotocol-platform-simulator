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
from datetime import datetime

from uprotocol.communication.requesthandler import RequestHandler
from uprotocol.communication.upayload import UPayload
from uprotocol.v1.uattributes_pb2 import (
    UPayloadFormat,
)
from uprotocol.v1.umessage_pb2 import UMessage

from tdk.apis.apis import TdkApis
from tdk.examples import common_methods


class MyRequestHandler(RequestHandler):
    def handle_request(self, msg: UMessage) -> UPayload:
        common_methods.logging.debug("Request Received by Service Request Handler")
        attributes = msg.attributes
        payload = msg.payload
        source = attributes.source
        sink = attributes.sink
        common_methods.logging.debug(f"Receive {payload} from {source} to {sink}")
        response_payload = format(datetime.utcnow()).encode('utf-8')  # your response payload
        payload = UPayload(data=response_payload, format=UPayloadFormat.UPAYLOAD_FORMAT_TEXT)
        return payload


async def register_rpc():
    uuri = common_methods.create_method_uri()
    config = common_methods.get_transport_config()
    tdk_apis = TdkApis(config)
    status = await tdk_apis.register_request_handler(uuri, MyRequestHandler())
    common_methods.logging.debug(f"Request Handler Register status {status}")
    while True:
        await asyncio.sleep(1)


if __name__ == '__main__':
    asyncio.run(register_rpc())
