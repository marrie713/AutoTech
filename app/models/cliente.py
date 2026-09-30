class Cliente:
    def __init__(self, nome, telefone, id=None):
        self.id = id
        self.nome = nome
        self.telefone = telefone

    def __str__(self):
        return f"{self.id} - {self.nome} - {self.telefone}"

