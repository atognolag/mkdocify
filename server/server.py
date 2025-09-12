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
def modify_docstrings(docstring: str, file_path: str, line_range: tuple[int, int]) -> str:
    """Modifies the code files to ensure the docstrings are MkDocs compliant."""
    return f"""MkDocs requires docstrings to be in the Markdown format. You will be provided with a docstring and you will need to modify it to be MkDocs compliant.
    You will also need to write the modified docstring back to the file.
    The provided docstring is:
    {docstring}
    And it is coming from file: {file_path} and lines: {line_range}
    """


@mcp.tool
async def compile_mkdocs(name: str) -> None:
    """Compiles the MkDocs documentation for the repo."""
    subprocess.run(["~/.gemini/extensions/mkdocify/venv/bin/python", "-m", "mkdocs", "build"]) 


@mcp.prompt
def ensure_mkdocs_is_initialized() -> str:
    """Ensures that MkDocs is initialized for the repo."""
    return """Verify that MkDocs is initialized for the repo. If not, initialize it.
    You can have a look at MkDocs documentation in https://www.mkdocs.org/getting-started/#adding-pages.
    For a quick reference, please be aware that the following folders are important: `docs/` for markdown files inclusive of an index.md file and `mkdocs.yml` for configuration at the root path."""


@mcp.prompt
def generate_mkdocs() -> str:
    """Prompts the agent with the process to generate MkDocs compliant documentation"""
    return """The high level process for generating MkDocs compatible docuemntation is:
1.Parse the repo's structure
2.Extract all docstrings
3.Ensure all docstrings are MkDocs compliant (or modify them and write them into the source file)
4.Ensure MkDocs is correctly initialized.
5.Generate (or update) the MkDocs documentation"""


@mcp.prompt
def ensure_docstring_is_mkdocs_compliant() -> str:
    """Ensures that a docstring is MkDocs compliant or not."""
    return """You    """


@mcp.resource("file://documents/{path}")
async def read_document_by_path(path: str) -> str:
    """Read a document by name."""
    # This would normally read from disk
    with open(path, "r") as f:
        return f.read()


@mcp.resource("mkdocify://cwd")
async def get_cwd() -> str:
    """Get the current working directory."""
    return os.getcwd()


if __name__ == "__main__":
    mcp.run()
