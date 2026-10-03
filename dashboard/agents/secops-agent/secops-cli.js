#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { Octokit } = require("@octokit/rest");

const args = process.argv.slice(2);
const command = args[0] || 'help';

// Inicializar cliente do GitHub se o token estiver configurado
const octokit = new Octokit({
  auth: process.env.GITHUB_TOKEN || ''
});

const REPO_OWNER = process.env.GITHUB_OWNER || 'mrcoantonioconceicao-ctrl';
const REPO_NAME = process.env.GITHUB_REPO || 'egc-enterprise-clone';

async function auditLocalCode() {
  console.log("🛡️ [SecOps Agent] A iniciar auditoria estática local de código (Anchor/Rust)...");
  const targetDir = path.join(__dirname, '../../programs/egc-gov-core/src');
  
  if (!fs.existsSync(targetDir)) {
    console.error("❌ Diretoria de programas não encontrada:", targetDir);
    return;
  }

  let vulnerabilitiesFound = 0;
  const files = fs.readdirSync(targetDir);

  files.forEach(file => {
    if (file.endsWith('.rs')) {
      const filePath = path.join(targetDir, file);
      const content = fs.readFileSync(filePath, 'utf8');
      
      console.log(`📄 A analisar ficheiro: ${file}`);
      
      // Verificar uso de unwrap inseguro
      if (content.includes('.unwrap()')) {
        console.warn(`   ⚠️  [AVISO] Uso de '.unwrap()' detetado em ${file}. Recomenda-se tratamento de erro com 'Result'.`);
        vulnerabilitiesFound++;
      }

      // Verificar validação de Signer / PDAs
      if (content.includes('#[account(mut)]') && !content.includes('Signer')) {
        console.warn(`   ⚠️  [ALERTA DE SEGURANÇA] Conta mutável sem restrição evidente de Signer em ${file}.`);
        vulnerabilitiesFound++;
      }
    }
  });

  if (vulnerabilitiesFound === 0) {
    console.log("✨ [SecOps Agent] Auditoria concluída: Nenhuma vulnerabilidade crítica óbvia detetada.");
  } else {
    console.log(`🔍 [SecOps Agent] Auditoria concluída com ${vulnerabilitiesFound} alertas a rever.`);
  }
}

async function scanGitHubPRs() {
  console.log(`🐙 [SecOps Agent] A varrer Pull Requests e falhas de CI em ${REPO_OWNER}/${REPO_NAME}...`);
  if (!process.env.GITHUB_TOKEN) {
    console.log("ℹ️  [Modo Simulação/Sandbox]: GITHUB_TOKEN não configurado. A simular varredura de CI...");
    console.log("   -> PR #1717: Testes intermitentes detetados (worktrees / gitdir e EBUSY no Windows). Resolvido via patch de auto-remediação.");
    return;
  }

  try {
    const { data: prs } = await octokit.pulls.list({
      owner: REPO_OWNER,
      repo: REPO_NAME,
      state: 'open'
    });

    console.log(`📦 Encontrados ${prs.length} Pull Requests abertos.`);
    prs.forEach(pr => {
      console.log(`   - PR #${pr.number}: ${pr.title} (Branch: ${pr.head.ref})`);
    });
  } catch (error) {
    console.error("❌ Erro ao contactar a API do GitHub:", error.message);
  }
}

function showHelp() {
  console.log(`
🛡️ SecOps Agent - Termux CLI Interface (EGC Ecosystem)
Comandos disponíveis:
  node agents/secops-agent/secops-cli.js audit      - Executa auditoria estática local (Rust/Anchor)
  node agents/secops-agent/secops-cli.js prs        - Varre PRs e estado de CI no GitHub via Octokit
  node agents/secops-agent/secops-cli.js status     - Mostra o estado atual do cérebro EGC (.egc-state)
  node agents/secops-agent/secops-cli.js help       - Mostra esta mensagem de ajuda
  `);
}

async function main() {
  switch (command) {
    case 'audit':
      await auditLocalCode();
      break;
    case 'prs':
    case 'scan-github':
      await scanGitHubPRs();
      break;
    case 'status':
      const statePath = path.join(__dirname, '../../.egc-state/memory-graph.json');
      if (fs.existsSync(statePath)) {
        console.log("🧠 Estado do Cérebro EGC:", fs.readFileSync(statePath, 'utf8'));
      } else {
        console.log("⚠️ Estado não inicializado. Corre primeiro './egc-sync.sh'.");
      }
      break;
    case 'help':
    default:
      showHelp();
      break;
  }
}

main();
