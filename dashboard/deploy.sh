#!/bin/bash

echo "=========================================="
echo "🚀 EGC-Solana: Iniciando Deploy Automático"
echo "=========================================="

# 1. Verificar branch atual
CURRENT_BRANCH=$(git branch --show-current)
echo "📌 Branch atual: $CURRENT_BRANCH"

if [ "$CURRENT_BRANCH" != "solana-cockpit" ]; then
    echo "⚠️ AVISO: Não estás na branch solana-cockpit. A mudar de branch..."
    git checkout solana-cockpit || git checkout -b solana-cockpit
fi

# 2. Adicionar alterações pendentes se houver
git add .
if [ -n "$(git status --porcelain)" ]; then
    echo "📦 Detetadas alterações pendentes. A criar commit automático..."
    git commit -m "chore(deploy): automatic sync and build prep for vercel"
else
    echo "✨ Nenhuma alteração pendente no Git. Repositório limpo."
fi

# 3. Sincronizar com o repositório remoto
echo "🔄 A enviar alterações para o GitHub (origin solana-cockpit)..."
git push origin solana-cockpit

# 4. Executar o Deploy na Vercel com verificação de erros
echo "⚡ A disparar o deploy para a Vercel..."
if command -v vercel &> /dev/null; then
    if vercel --prod --yes; then
        echo "✅ Deploy concluído com sucesso!"
    else
        echo "❌ Erro no deploy da Vercel. Se esta for a primeira vez, faz login com: vercel login"
        exit 1
    fi
else
    echo "❌ Erro: Vercel CLI não encontrada."
    echo "💡 Instala a Vercel CLI globalmente executando: npm i -g vercel"
    exit 1
fi
echo "=========================================="
