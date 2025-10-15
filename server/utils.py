from gitingest import ingest

def parse_repo_structure(repo_path = '.'):
    summary, tree, content = ingest(repo_path)
    return {"summary": summary, "tree": tree, "content": content}

if __name__ == "__main__":
    print(parse_repo_structure('.'))