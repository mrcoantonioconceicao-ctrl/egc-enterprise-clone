class ProcessadorFinanceiro:
    def __init__(self, token: str):
        self.token = token

    def calcular_taxa(self, valor: float, percentual: float) -> float:
        return valor * (percentual / 100.0)

    def validar_transacao(self, id_transacao: str) -> bool:
        return len(id_transacao) > 0

def funcao_global_isolada(codigo_pais: str, ativo: bool):
    pass
