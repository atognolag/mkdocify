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
logger.debug(f"Cwd is: {os.getcwd()}")

from fastmcp import FastMCP
try:
    from server.utils import parse_repo_structure
except ImportError:
    from utils import parse_repo_structure
import subprocess


mcp = FastMCP("MkDocify 📖")


@mcp.resource("mkdocify://repo_tree/{path}")
async def parse_repo(path: str = '.') -> dict[str,str]:
    """Repo's code structure. The path is '.' by default."""
    return parse_repo_structure(path)


@mcp.prompt
async def generate_application_docs() -> str:
    """Use this prompt to generate markdown files for a generic application."""
    if not os.path.exists("docs") or not os.path.exists("mkdocs.yml"):
        return """Initialize mkdocs by creating a `mkdocs.yml` file (give it a meaningful app name) and a `docs/` folder that contains that contains at least a `index.md` file.
        Make sure that the "use_directory_urls" option is set to false and that the `nav` section is properly configured as well as the titles for each page are relevant to the code."""
    else:
        raise Exception("MkDocs is already initialized.")

@mcp.prompt
async def initialize_mkdocs() -> str:
    """Use this prompt to initialize MkDocs and configure it."""
    if not os.path.exists("docs") or not os.path.exists("mkdocs.yml"):
        return """Initialize mkdocs by creating a `mkdocs.yml` file (give it a meaningful app name) and a `docs/` folder that contains that contains at least a `index.md` file.
        Make sure that the "use_directory_urls" option is set to false and that the `nav` section is properly configured as well as the titles for each page are relevant to the code."""
    else:
        raise Exception("MkDocs is already initialized.")
    

@mcp.tool
async def build_mkdocs(path: str, theme: str = 'readthedocs') -> None:
    """Use this tool to build the MkDocs documentation after having ensured that MkDocs is initalized and that the markdown files are up to date.
    You must specify the current working directory as the path argument."""
    if os.path.exists(path+"/docs") and os.path.exists(path+"/mkdocs.yml"):
        subprocess.Popen([sys.executable, "-m", "mkdocs", "build", "-t", theme], cwd=path)
    else:
        raise Exception(f"""MkDocs is not initialized. Please initialize it first and the re-attempt this step.
                        These are the files and folders in the current directory: {os.listdir(path)}""")


@mcp.prompt
def ensure_docs_are_current() -> str:
    """Use this prompt to ensure that MkDocs is initialized and the markdown files are up to date."""
    return """Verify that MkDocs is initialized for the repo. If not, initialize it.
    For a quick reference, please be aware that the following folders/files are needed:
    1.A `mkdocs.yml` file for configuration at the root path, containing the app's name.
    2.A `docs/` folder for markdown files inclusive of an index.md file to serve as the documentation's index, which points to all the markdown files.
    3.As many as necessary markdown files for each module, class, function or etc. that needs to be documented."""


@mcp.prompt
def generate_mkdocs() -> str:
    """Provides an explanation to the agent on the process to generate MkDocs compliant documentation"""
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
