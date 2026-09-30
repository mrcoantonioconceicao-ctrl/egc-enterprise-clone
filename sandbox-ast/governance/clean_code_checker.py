#!/usr/bin/env python3
import ast
import sys
import json

class CleanCodeAuditor(ast.NodeVisitor):
    def __init__(self, filepath):
        self.filepath = filepath
        self.warnings = []
        self.max_args = 5
        self.max_function_lines = 50

    def visit_FunctionDef(self, node):
        # Verifica número excessivo de argumentos (Clean Code violation)
        arg_count = len(node.args.args)
        if arg_count > self.max_args:
            self.warnings.append({
                "type": "Excessive Parameters",
                "target": node.name,
                "line": node.lineno,
                "message": f"A função '{node.name}' possui {arg_count} argumentos (máximo recomendado: {self.max_args}). Considere usar um objeto de parâmetro (Data Transfer Object)."
            })

        # Verifica tamanho da função (linhas)
        if node.body:
            start_line = node.lineno
            end_line = node.end_lineno if hasattr(node, 'end_lineno') else start_line
            length = end_line - start_line
            if length > self.max_function_lines:
                self.warnings.append({
                    "type": "Long Function",
                    "target": node.name,
                    "line": start_line,
                    "message": f"A função '{node.name}' é muito longa ({length} linhas, máximo recomendado: {self.max_function_lines}). Extraia responsabilidades."
                })

        self.generic_visit(node)

def audit_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            code_content = f.read()
        tree = ast.parse(code_content, filename=filepath)
        auditor = CleanCodeAuditor(filepath)
        auditor.visit(tree)
        return {"file": filepath, "violations": auditor.warnings}
    except Exception as e:
        return {"file": filepath, "error": str(e)}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        result = audit_file(sys.argv[1])
        print(json.dumps(result, indent=2))
    else:
        print("Usage: python3 clean_code_checker.py <source_file>")
