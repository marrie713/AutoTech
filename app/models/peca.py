class Peca:
    def __init__(self, descricao, valor, qntd_disponivel, id=None):
        self.id = id
        self.descricao = descricao
        self.valor = valor
        self.qntd_disponivel = qntd_disponivel