# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from fastmcp import Client
import pytest


@pytest.mark.asyncio
async def test_connection(client: Client) -> None:
    assert client.is_connected()


@pytest.mark.asyncio
async def test_get_prompts(client: Client) -> None:
    async with client as client:
        prompts = await client.list_prompts()
        assert len(prompts) > 0


@pytest.mark.asyncio
async def test_get_tools(client: Client) -> None:
    async with client as client:
        tools = await client.list_tools()
        assert len(tools) > 0
