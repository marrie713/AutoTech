from app.models.cliente import Cliente
from app.models.veiculo import Veiculo
from app.models.mecanica import Mecanico
from app.models.servico import Servico
from app.models.peca import Peca
from app.models.ordem_servico import OrdemServico


def main():
    cliente = Cliente("João da Silva", "34 99999-9999")
    veiculo = Veiculo("ABC-1234", "Toyota Corolla", 2020)
    mecanico = Mecanico("Régis", "Automotivo")
    servico = Servico("Motor fundido", "5.000")
    peca = Peca("Motor", "10.000", "1")
    ordemservico = OrdemServico("1", cliente, veiculo, mecanico, [], [])

    print("=== OficinaTech ===")
    print(f"Cliente: {cliente.nome}")
    print(f"Telefone: {cliente.telefone}")
    
    print(f"Veículo: {veiculo.modelo}")
    print(f"Placa: {veiculo.placa}")
    print(f"Ano: {veiculo.ano}")

    print(f"Mecânico: {mecanico.nome}")
    print(f"Especialidade: {mecanico.especialidade}")

    print(f"Serviço: {servico.descricao}")
    print(f"Valor: {servico.valor}")

    print(f"Peça: {peca.descricao}")
    print(f"Valor: {peca.valor}")
    print(f"Quantidade disponível: {peca.qntd_disponivel}")

    print(f"Nome cliente ordem de serviço: {ordemservico.cliente.nome}")
    print(f"Modelo do veiculo: {ordemservico.veiculo.modelo}")
    print(f"Placa veiculo: {ordemservico.veiculo.placa}")
    print(f"Nome mecânico: {ordemservico.mecanico.nome}")
    print(f"Especialidade Mecânico: {ordemservico.mecanico.especialidade}")

if __name__ == "__main__":
    main()

