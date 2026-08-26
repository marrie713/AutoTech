from app.models.cliente import Cliente
from app.models.veiculo import Veiculo


def main():
    cliente = Cliente("João da Silva", "34 99999-9999")
    veiculo = Veiculo("ABC-1234", "Toyota Corolla", 2020)

    print("=== OficinaTech ===")
    print(f"Cliente: {cliente.nome}")
    print(f"Telefone: {cliente.telefone}")
    print(f"Veículo: {veiculo.modelo}")
    print(f"Placa: {veiculo.placa}")
    print(f"Ano: {veiculo.ano}")


if __name__ == "__main__":
    main()

