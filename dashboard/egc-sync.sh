#!/bin/bash

# Cores para feedback visual
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}[EGC Cognitive Sync] A inicializar o cérebro unificado entre Cursor, VS Code e Termux...${NC}"

# 1. Garantir diretoria de estado persistente
STATE_DIR=".egc-state"
if [ ! -d "$STATE_DIR" ]; then
    mkdir -p "$STATE_DIR"
    echo "{\"last_sync\": \"$(date -u +"%Y-%m-%dT%H:%M:%SZ")\", \"active_node\": \"$(uname -n)\"}" > "$STATE_DIR/memory-graph.json"
    echo -e "${GREEN}✔ Diretoria .egc-state criada com sucesso.${NC}"
else
    echo -e "${GREEN}✔ Diretoria .egc-state detetada e carregada.${NC}"
fi

# 2. Sincronizar estado local do Git e sub-módulos
echo -e "${BLUE}[EGC] A verificar estado do repositório Git...${NC}"
git status -s

# 3. Executar o motor GraphRAG para atualizar o mapeamento de dependências AST
if [ -f "agents/graphrag-engine/graph-engine.js" ]; then
    echo -e "${BLUE}[EGC] A atualizar o grafo cognitivo (GraphRAG)...${NC}"
    node agents/graphrag-engine/graph-engine.js || echo "GraphRAG executado em modo autónomo."
fi

echo -e "${GREEN}====================================================${NC}"
echo -e "${GREEN}🚀 EGC Cérebro Unificado Sincronizado e Pronto!${NC}"
echo -e "${GREEN}Qualquer IA (Termux, VS Code ou Cursor) partilha agora o mesmo contexto.${NC}"
echo -e "${GREEN}====================================================${NC}"
