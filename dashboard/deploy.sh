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
if ! git diff-cached --quiet; then
    echo "📦 Detetadas alterações pendentes. A criar commit automático..."
    git commit -m "chore(deploy): automatic sync and build prep for vercel"
else
    echo "✨ Nenhuma alteração pendente no Git. Repositório limpo."
fi

# 3. Sincronizar com o repositório remoto
echo "🔄 A enviar alterações para o GitHub (origin solana-cockpit)..."
git push origin solana-cockpit

# 4. Executar o Deploy na Vercel
echo "⚡ A disparar o deploy para a Vercel..."
if command -v vercel &> /dev/null; then
    vercel --prod --yes
    echo "✅ Deploy concluído com sucesso!"
else
    echo "❌ Erro: Vercel CLI não encontrada."
    echo "💡 Instala a Vercel CLI globalmente executando: npm i -g vercel"
    echo "💡 Ou executa 'npx vercel --prod' manualmente."
fi
echo "=========================================="
