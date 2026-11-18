class Peca:
    def __init__(self, descricao, valor, estoque, id=None):
        self.id = id
        self.descricao = descricao
        self.valor = valor
        self.estoque = estoque