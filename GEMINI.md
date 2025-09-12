# MkDocify

MkDocify is a Gemini CLI extension to generate MkDocs documentation.

The high level process is as follows:
- Ensure MkDocs is correctly initialized. If not, initialize it with the corresponding tool call.
- Ensure the markdown files are up to date and current or else, update their contents.
- Serve the documentation locally for review.
- Compile the MkDocs documentation with the corresponding tool call.