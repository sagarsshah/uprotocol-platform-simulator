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
from uprotocol.v1.uattributes_pb2 import (
    UPayloadFormat,
)

from tdk.apis.apis import TdkApis
from tdk.examples import common_methods


async def send_rpc_request_to_zenoh():
    # create uuri
    method_uri = common_methods.create_method_uri()

    # create UPayload
    data = "GetCurrentTime"  # your request payload
    request_payload = UPayload(format=UPayloadFormat.UPAYLOAD_FORMAT_TEXT, data=bytes([ord(c) for c in data]))

    # invoke RPC method
    common_methods.logging.debug(f"Send request to {method_uri}")

    config = common_methods.get_transport_config()
    tdk_apis = TdkApis(config)

    response_payload = await tdk_apis.invoke_method(method_uri, request_payload, CallOptions(timeout=1000))
    common_methods.logging.debug(f"RESPONSE PAYLOAD {response_payload}")


if __name__ == '__main__':
    asyncio.run(send_rpc_request_to_zenoh())
