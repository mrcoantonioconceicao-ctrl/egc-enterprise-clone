import * as anchor from "@coral-xyz/anchor";
import { Program } from "@coral-xyz/anchor";
import { EgcAnchorCore } from "../target/types/egc_anchor_core";
import { assert } from "chai";

describe("egc-anchor-core", () => {
  // Configura o provider para a rede local/devnet configurada no Anchor.toml
  const provider = anchor.AnchorProvider.env();
  anchor.setProvider(provider);

  const program = anchor.workspace.EgcAnchorCore as Program<EgcAnchorCore>;

  it("Is initializes and records an AI consensus audit proof on-chain via PDA", async () => {
    const authority = provider.wallet;
    const sessionId = "session-egc-9942";
    
    // Simula um hash de auditoria de 32 bytes gerado pelo Auditório de Consenso
    const auditHashHex = "a1b2c3d4e5f678901234567890abcdef1234567890abcdef1234567890abcdef";
    const auditHash = Buffer.from(auditHashHex, "hex");
    const status = 1; // 1 = Aprovado / Conforme

    // Deriva a PDA exatamente como definido no contrato Rust (seeds: [b"audit", authority, session_id])
    const [auditAccountPda, bump] = await anchor.web3.PublicKey.findProgramAddressSync(
      [
        Buffer.from("audit"),
        authority.publicKey.toBuffer(),
        Buffer.from(sessionId),
      ],
      program.programId
    );

    console.log("PDA Derivada com Sucesso:", auditAccountPda.toBase58());

    // Executa a instrução record_consensus_audit no programa Anchor
    const tx = await program.methods
      .recordConsensusAudit(sessionId, Array.from(auditHash), status)
      .accounts({
        auditAccount: auditAccountPda,
        authority: authority.publicKey,
        systemProgram: anchor.web3.SystemProgram.programId,
      })
      .rpc();

    console.log("Transação de Auditoria enviada. Assinatura:", tx);

    // Busca a conta recém-criada na blockchain para verificar o estado
    const accountState = await program.account.auditRecord.fetch(auditAccountPda);

    // Validações assertivas (Garantindo 100% de verdade e mensurabilidade)
    assert.equal(accountState.authority.toBase58(), authority.publicKey.toBase58());
    assert.equal(accountState.sessionId, sessionId);
    assert.equal(accountState.status, status);
    assert.equal(Buffer.from(accountState.auditHash).toString("hex"), auditHashHex);
    
    console.log("Sucesso! Todos os testes de integração do EGC-Solana passaram com 100% de conformidade.");
  });
});
