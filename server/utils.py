import ast
import astor
import os
import re
import concurrent.futures

COMMON_FOLDER_EXCLUSIONS = r"(^|\/)(docs|node_modules|vendor|dist|build|out|target|\.vscode|\.idea|\.vs|\.pytest_cache|\.mypy_cache|__pycache__|coverage|logs|tmp|env|venv|\.git|\.github|\.svn|\.tox)(\/|$)"
COMMON_FILE_INCLUSIONS = r".*\.(py|pyc|pyo|pyi|pyw|ipynb)$"
MAX_THREADS = 10

def parse_repo_structure(repo_path = '.'):
    source_tree = ''
    all_files = []
    for cur, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if not re.match(COMMON_FOLDER_EXCLUSIONS, d)]
        files[:] = [f for f in files if re.match(COMMON_FILE_INCLUSIONS, f)]
        all_files += [os.path.join(cur, f) for f in files]
        pref = ''
        head, tail = os.path.split(cur)
        while head:
            pref += '---'
            head, _tail = os.path.split(head)
        source_tree += pref+tail+'\n'
        for f in files:
            source_tree += pref+'---'+f+'\n'
    return source_tree, all_files


def get_docstrings(file_path):
    with open(file_path, 'r') as f:
        tree = ast.parse(f.read())
    docstrings = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Module)):
            docstring = ast.get_docstring(node)
            if docstring:
                docstrings.append({"doc":docstring, "lines":(node.lineno, node.end_lineno)})
    return {"file":file_path, "docstrings":docstrings}


def get_all_docstrings(repo_path = '.'):
    all_files = parse_repo_structure(repo_path)[1]
    pool = concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS)
    futures = []
    for file_path in all_files:
        futures.append(pool.submit(get_docstrings,file_path))
    docstrings = []
    for future in concurrent.futures.as_completed(futures):
        docstrings.append(future.result())
    pool.shutdown(wait=True)
    return docstrings

if __name__ == "__main__":
    print(get_all_docstrings())