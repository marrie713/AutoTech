from app.models.cliente import Cliente
from app.models.veiculo import Veiculo
from app.models.mecanica import Mecanico
from app.models.servico import Servico
from app.models.peca import Peca
from app.models.ordem_servico import OrdemDeServico
from app.database.database import Database

from app.repositories.ClienteRepositorio import ClienteRepositorio
from app.repositories.veiculoRepositorio import VeiculoRepositorio
from app.repositories.mecanicoRepositorio import MecanicoRepositorio
from app.repositories.servicoRepositorio import ServicoRepositorio
from app.repositories.pecaRepositorio import PecaRepositorio
from app.repositories.ordemservicoRepositorio import OrdemservicoRepositorio

import os

def main():

    # Para não dar erro de tabela já criada
    if os.path.exists("oficina.db"):
        os.remove("oficina.db") 

    database = Database()
    conexao = database.conexao

    clienteRepo = ClienteRepositorio(conexao)
    veiculoRepo = VeiculoRepositorio(conexao)
    mecanicoRepo = MecanicoRepositorio(conexao)
    servicoRepo = ServicoRepositorio(conexao)
    pecaRepo = PecaRepositorio(conexao)
    ordemRepo = OrdemservicoRepositorio(conexao)

    clienteRepo.criarTabela()
    veiculoRepo.criarTabela()
    mecanicoRepo.criarTabela()
    servicoRepo.criarTabela()
    pecaRepo.criarTabela()
    ordemRepo.criarTabela()

    cliente = Cliente("João da Silva", "34 99999-9999")
    veiculo = Veiculo("ABC-1234", "Toyota Corolla", 2020)
    mecanico = Mecanico("Carlos Oliveira", "Mecânica Geral")
    servico1 = Servico("Troca de pastilhas de freio", 180.00)
    servico2 = Servico("Alinhamento e balanceamento", 120.00)
    peca1 = Peca("Pastilha de freio", 250.00, 10)
    peca2 = Peca("Filtro de óleo", 45.00, 5)

    clienteRepo.salvar(cliente)
    veiculoRepo.salvar(veiculo)
    mecanicoRepo.salvar(mecanico)
    servicoRepo.salvar(servico1)
    servicoRepo.salvar(servico2)
    pecaRepo.salvar(peca1)
    pecaRepo.salvar(peca2)

    ordem = OrdemDeServico(cliente, veiculo, mecanico)
    ordem.adicionar_servico(servico1)
    ordem.adicionar_servico(servico2)
    ordem.adicionar_peca(peca1)
    ordem.adicionar_peca(peca2)

    ordemRepo.salvar(ordem)

    #atualiza o status
    ordem.status = "Em andamento"
    ordemRepo.atualizar(ordem)

    os_ = ordemRepo.buscarPorId(ordem.id)


    print(f"OS nº {os_.id}")
    print(f"Cliente: {os_.cliente.nome} ({os_.cliente.telefone})")
    print(f"Veículo: {os_.veiculo.modelo} - {os_.veiculo.placa}")
    print(f"Mecânico: {os_.mecanico.nome} ({os_.mecanico.especialidade})")

    print("Serviços:")
    print(f"  - {servico1.descricao}: R$ {servico1.valor:.2f}")
    print(f"  - {servico2.descricao}: R$ {servico2.valor:.2f}")

    print("Peças:")
    print(f"  - {peca1.descricao}: R$ {peca1.valor:.2f}")
    print(f"  - {peca2.descricao}: R$ {peca2.valor:.2f}")

    print(f"Total: R$ {os_.calcular_total():.2f}")
    print(f"Status: {os_.status}")

    database.fechar()


if __name__ == "__main__":
    main()