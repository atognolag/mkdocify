# Copyright 2025 Google LLC
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

import os
import sys
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug(f"System path is: {sys.path}")

from fastmcp import FastMCP
try:
    from server.utils import parse_repo_structure, get_all_docstrings
except ImportError:
    from utils import parse_repo_structure, get_all_docstrings
import subprocess

mcp = FastMCP("MkDocify 📖")


@mcp.resource("mkdocify://repo_tree/{path}")
async def parse_repo(path: str = '.') -> str:
    """Repo's code structure. The path is '.' by default."""
    return parse_repo_structure(path)[0]


@mcp.resource("mkdocify://all_docstrings/{path}")
async def parse_docstrings(path: str = '.') -> list[str]:
    """The entire code base's docstrings."""
    return get_all_docstrings('.')


@mcp.tool
async def initialize_mkdocs() -> None:
    """Use this tool to initialize MkDocs."""
    if not os.path.exists("./docs") or not os.path.exists("./mkdocs.yml"):
        subprocess.run(["~/.gemini/extensions/mkdocify/venv/bin/python", "-m", "mkdocs", "new","."])
    else:
        raise Exception("MkDocs is already initialized.")
    

@mcp.tool
async def preview_mkdocs(theme: str = 'readthedocs') -> None:
    """Use this tool to preview the MkDocs documentation after having ensured MkDocs is initialized."""
    if os.path.exists("./docs") and os.path.exists("./mkdocs.yml"):
        subprocess.run(["~/.gemini/extensions/mkdocify/venv/bin/python", "-m", "mkdocs", "serve","-t", theme])
    else:
        raise Exception("MkDocs is not initialized. Please initialize it first and the re-attempt this step.")


@mcp.tool
async def build_mkdocs(theme: str = 'readthedocs') -> None:
    """Use this tool to build the MkDocs documentation after having ensured previewed the docs."""
    if os.path.exists("./docs") and os.path.exists("./mkdocs.yml"):
        subprocess.run(["~/.gemini/extensions/mkdocify/venv/bin/python", "-m", "mkdocs", "build","-t", theme])
    else:
        raise Exception("MkDocs is not initialized. Please initialize it first and the re-attempt this step.")


@mcp.prompt
def ensure_mkdocs_is_initialized() -> str:
    """Use this prompt to ensure that MkDocs is initialized for the repo."""
    return """Verify that MkDocs is initialized for the repo. If not, initialize it.
    You can have a look at MkDocs documentation in https://www.mkdocs.org/getting-started/#adding-pages.
    For a quick reference, please be aware that the following folders/files are needed:
    1.A `mkdocs.yml` file for configuration at the root path.
    2.A `docs/` folder for markdown files inclusive of an index.md file to server as the index, which points to all the markdown files.
    3.As many as necessary markdown files for each module, class, function or etc. that needs to be documented."""


@mcp.prompt
def generate_mkdocs() -> str:
    """This prompt explains to the agent the process to generate MkDocs compliant documentation"""
    return """The high level process for generating MkDocs compatible documentation is:
1.Ensure MkDocs is correctly initialized.
2.Verify all the markdown files in `docs/` are current and up to date and that the `.docs/index.md` is up to date with the repo's structure. 
3.Compile the markdown files into the MkDocs documentation.
"""


@mcp.resource("file://docs/{path}")
async def read_document_by_path(path: str) -> str:
    """Read a document by it's path."""
    # This would normally read from disk
    with open(path, "r") as f:
        return f.read()


@mcp.resource("mkdocify://cwd")
async def get_cwd() -> str:
    """Get the current working directory."""
    return os.getcwd()


if __name__ == "__main__":
    mcp.run()
