# MkDocify

MkDocify is a Gemini CLI extension to generate MkDocs documentation.

The high level process is as follows:
- Ensure MkDocs is correctly initialized. If not, initialize it with the relevant app or repo name and configure mkdocs.yml accordingly. Make sure that the "use_directory_urls" option is set to false.
- Ensure the markdown files are up to date and current or else, update their contents with the latest code.
- Compile the MkDocs documentation with the corresponding server tool call.

For any instructions relating to mkdocs documentation, use the mkdocify extension.
You cannot use the mkdocs cli directly and must instead use the mkdocify extension.
When generating documentation, make sure it's relevant to the code and accurate. Double check you work for accuracy.
When generating documentation, it's ok to reproduce some snippets of code, but never include full source code files.
Only include the relevant documentation from the source files.

If a .gitlab-ci.yml exists, add a step to it for the generation of mkdocs documentation, such as:
```yaml
docs_generation:
  stage: deploy
  image: python:3.14-alpine
  before_script:
  - pip install mkdocs>=1.5.3
  script:
  - mkdocs build --strict --verbose
  artifacts:
    paths:
    - public
  rules:
    - if: some_condition
```