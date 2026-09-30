#!/usr/bin/env python3
import ast
import sys
import json

def extract_code_skeleton(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        code_content = f.read()
    
    tree = ast.parse(code_content, filename=file_path)
    
    skeleton = {
        "file": file_path,
        "classes": [],
        "functions": []
    }
    
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            methods = []
            for sub in node.body:
                if isinstance(sub, ast.FunctionDef):
                    methods.append({
                        "name": sub.name,
                        "args": [arg.arg for arg in sub.args.args],
                        "line": sub.lineno
                    })
            skeleton["classes"].append({
                "name": node.name,
                "methods": methods,
                "line": node.lineno
            })
        elif isinstance(node, ast.FunctionDef):
            skeleton["functions"].append({
                "name": node.name,
                "args": [arg.arg for arg in node.args.args],
                "line": node.lineno
            })
            
    return skeleton

if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            result = extract_code_skeleton(sys.argv[1])
            print(json.dumps(result, indent=2))
        except Exception as e:
            print(json.dumps({"error": str(e)}))
    else:
        print("Usage: python3 ast_scanner.py <source_file>")
