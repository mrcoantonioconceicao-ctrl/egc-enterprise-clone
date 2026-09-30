#!/usr/bin/env python3
import subprocess
import sys
import os

def run_cmd(description, cmd):
    print(f"\n[*] {description}...")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[X] Falha em: {description}")
        print(result.stderr)
        return False
    print(f"[OK] {description} passou com sucesso.")
    if result.stdout.strip():
        print(result.stdout)
    return True

def main():
    print("==================================================")
    print("=== INICIANDO VARREDURA COMPLETA DO SANDBOX EGC ===")
    print("==================================================")
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    target_file = os.path.join(base_dir, "tests", "sample_target.py")
    root_dir = os.path.abspath(os.path.join(base_dir, ".."))

    checks = [
        ("Executando AST Scanner (Rigor Micro)", f"python3 {base_dir}/extractors/ast_scanner.py {target_file}"),
        ("Executando GraphRAG Mapper (Visão Macro & Dependências)", f"python3 {base_dir}/extractors/graphrag_mapper.py {root_dir}"),
        ("Executando Clean Code Auditor (Qualidade Semântica)", f"python3 {base_dir}/governance/clean_code_checker.py {target_file}"),
        ("Executando Doc Auditor (Conformidade Markdown & Regras da Casa)", f"python3 {base_dir}/governance/doc_auditor.py {root_dir}")
    ]

    success = True
    for desc, cmd in checks:
        if not run_cmd(desc, cmd):
            success = False

    print("\n==================================================")
    if success:
        print("=== STATUS: TODAS AS VERIFICAÇÕES PASSARAM (VERDE) ===")
        print("==================================================")
        sys.exit(0)
    else:
        print("=== STATUS: HOUVE FALHAS NA AUDITORIA DO SANDBOX ===")
        print("==================================================")
        sys.exit(1)

if __name__ == "__main__":
    main()
