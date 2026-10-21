class OrdemDeServico:

    def __init__(self, cliente, veiculo, mecanico, status="Aberta", id=None):
        self.id = id
        self.cliente = cliente
        self.veiculo = veiculo
        self.mecanico = mecanico
        self.status = status
        
        self.servicos = []
        self.pecas = []


    def adicionar_servico(self, servico):
        self.servicos.append(servico)

    def adicionar_peca(self, peca):
        self.pecas.append(peca)

    def calcular_total(self):
        total_servicos = sum(servico.valor
        for servico in self.servicos
        )

        total_pecas = sum(
            peca.valor
            for peca in self.pecas)

        return total_servicos + total_pecas