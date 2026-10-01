use anchor_lang::prelude::*;

declare_id!("EgcGov1111111111111111111111111111111111111");

#[program]
pub mod egc_anchor_core {
    use super::*;

    /// Regista uma prova de auditoria cognitiva gerada pelo Auditório de Consenso do EGC
    pub fn record_consensus_audit(
        ctx: Context<RecordAudit>,
        session_id: String,
        audit_hash: [u8; 32],
        status: u8,
    ) -> Result<()> {
        let audit_account = &mut ctx.accounts.audit_account;
        audit_account.authority = ctx.accounts.authority.key();
        audit_account.session_id = session_id;
        audit_account.audit_hash = audit_hash;
        audit_account.status = status;
        audit_account.timestamp = Clock::get()?.unix_timestamp;
        
        msg!("EGC-Solana: Audit record successfully committed on-chain via PDA.");
        Ok(())
    }
}

#[derive(Accounts)]
#[instruction(session_id: String)]
pub struct RecordAudit<'info> {
    #[account(
        init,
        payer = authority,
        space = 8 + 32 + 4 + session_id.len() + 32 + 1 + 8,
        seeds = [b"audit", authority.key().as_ref(), session_id.as_bytes()],
        bump
    )]
    pub audit_account: Account<'info, AuditRecord>,
    
    #[account(mut)]
    pub authority: Signer<'info>,
    
    pub system_program: Program<'info, System>,
}

#[account]
pub struct AuditRecord {
    pub authority: Pubkey,
    pub session_id: String,
    pub audit_hash: [u8; 32],
    pub status: u8, // 1 = Aprovado / Conforme, 2 = Fricção / Corrigido pelo Sistema
    pub timestamp: i64,
}
