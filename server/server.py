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

from fastmcp import FastMCP

mcp = FastMCP("MkDocify 🚀")


@mcp.tool
def hello_tool(name: str) -> str:
    return f"Hello, {name}!"


@mcp.prompt
def hello_prompt() -> list[str]:
    return ["hello"]


if __name__ == "__main__":
    mcp.run()
