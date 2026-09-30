from app.models.cliente import Cliente
from app.models.veiculo import Veiculo
from app.models.mecanico import Mecanico
from app.models.servico import Servico
from app.models.peca import Peca
from app.models.ordem_de_servico import OrdemDeServico


cliente = Cliente(
    "João da Silva",
    "34 99999-9999"
)

veiculo = Veiculo(
    "ABC-1234",
    "Toyota Corolla",
    2020
)

mecanico = Mecanico(
    "Carlos Oliveira",
    "Freios e suspensão"
)

servico1 = Servico(
    "Troca de pastilhas de freio",
    180.00
)

servico2 = Servico(
    "Alinhamento e balanceamento",
    120.00
)

peca1 = Peca(
    "Pastilha de freio",
    250.00,
    10
)

peca2 = Peca(
    "Filtro de óleo",
    45.00,
    5
)


ordem = OrdemDeServico(
    1,
    cliente,
    veiculo,
    mecanico
)


ordem.adicionar_servico(servico1)
ordem.adicionar_servico(servico2)

ordem.adicionar_peca(peca1)
ordem.adicionar_peca(peca2)


print(f"Cliente: {ordem.cliente.nome}")
print(f"Veículo: {ordem.veiculo.modelo}")
print(f"Placa: {ordem.veiculo.placa}")
print(f"Mecânico: {ordem.mecanico.nome}")
print(f"Especialidade: {ordem.mecanico.especialidade}")

print(f"Total: R$ {ordem.calcular_total():.2f}")