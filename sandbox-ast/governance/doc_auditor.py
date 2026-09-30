#!/usr/bin/env python3
import os
import re
import sys
import json

def audit_markdown_files(root_dir):
    issues = []
    # Padrões comuns a auditar em docs
    deprecated_terms = ["Gemini Code", "Continue.dev", "Roo Code"]
    
    for dirpath, _, filenames in os.walk(root_dir):
        if "node_modules" in dirpath or ".git" in dirpath or "sandbox-ast" in dirpath:
            continue
        for file in filenames:
            if file.endswith(".md"):
                full_path = os.path.join(dirpath, file)
                rel_path = os.path.relpath(full_path, root_dir)
                
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                        
                    for idx, line in enumerate(lines, 1):
                        # Verifica termos desatualizados mencionados na auditoria
                        for term in deprecated_terms:
                            if term in line:
                                issues.append({
                                    "file": rel_path,
                                    "line": idx,
                                    "type": "Deprecated Term Mention",
                                    "message": f"Termo legado encontrado: '{term}'. Deve ser atualizado conforme o plano de migração."
                                })
                                
                        # Verifica uso de travessões duplos (regra de ouro: apenas hífen simples)
                        if " -- " in line or line.strip().startswith("—") or " — " in line:
                            issues.append({
                                "file": rel_path,
                                "line": idx,
                                "type": "Formatting Violation (Em-dash)",
                                "message": "Uso de travessão detectado. Regra da casa exige apenas hífen simples."
                            })
                except Exception as e:
                    issues.append({
                        "file": rel_path,
                        "line": 0,
                        "type": "Read Error",
                        "message": str(e)
                    })
                    
    return {"audited_directory": root_dir, "total_issues": len(issues), "findings": issues}

if __name__ == "__main__":
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    result = audit_markdown_files(target_dir)
    print(json.dumps(result, indent=2))
