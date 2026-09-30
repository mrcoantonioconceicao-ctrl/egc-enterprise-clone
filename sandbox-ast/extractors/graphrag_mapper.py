#!/usr/bin/env python3
import os
import ast
import json
import sys

def extract_imports(file_path):
    imports = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=file_path)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
    except Exception:
        pass
    return imports

def build_dependency_graph(root_dir):
    graph = {
        "nodes": [],
        "edges": []
    }
    
    file_map = {}
    node_id = 0
    
    for dirpath, _, filenames in os.walk(root_dir):
        if "node_modules" in dirpath or ".git" in dirpath or "sandbox-ast" in dirpath:
            continue
        for file in filenames:
            if file.endswith(".py"):
                full_path = os.path.join(dirpath, file)
                rel_path = os.path.relpath(full_path, root_dir)
                file_map[rel_path] = node_id
                graph["nodes"].append({"id": node_id, "file": rel_path})
                node_id += 1

    for rel_path, src_id in file_map.items():
        full_path = os.path.join(root_dir, rel_path)
        imports = extract_imports(full_path)
        for imp in imports:
            # Tenta mapear importações locais se coincidirem com arquivos do projeto
            for target_path, target_id in file_map.items():
                module_name = target_path.replace("/", ".").replace(".py", "")
                if imp == module_name or imp in module_name:
                    if src_id != target_id:
                        edge = {"source": src_id, "target": target_id, "imported_module": imp}
                        if edge not in graph["edges"]:
                            graph["edges"].append(edge)
                            
    return graph

if __name__ == "__main__":
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    result = build_dependency_graph(target_dir)
    print(json.dumps(result, indent=2))
