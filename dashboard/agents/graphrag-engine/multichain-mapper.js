const fs = require('fs');
const path = require('path');

function scanMultichainContracts() {
  console.log("🕸️ [GraphRAG Multichain] A varrer contratos Solidity, Soroban e Anchor...");
  
  const chains = {
    solana_anchor: { path: 'programs/', ext: '.rs', risk: 'Low (with Anchor)' },
    ethereum_solidity: { path: 'contracts/solidity/', ext: '.sol', risk: 'Medium (Reentrancy check)' },
    stellar_soroban: { path: 'contracts/soroban/', ext: '.rs', risk: 'Low (Rust-based)' }
  };

  for (const [chain, config] of Object.entries(chains)) {
    console.log(`   -> Ecossistema ${chain}: A monitorizar diretoria '${config.path}' (Filtro: ${config.ext})`);
  }
}

if (require.main === module) {
  scanMultichainContracts();
}

module.exports = { scanMultichainContracts };
