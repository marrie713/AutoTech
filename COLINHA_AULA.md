# Colinha — OficinaTech | Aula 1

## 1. Criar ambiente
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python --version
```

## 2. Clonar projeto
```bash
git clone URL_DO_REPOSITORIO
cd oficina-autotech
```

## 3. Executar
```bash
python main.py
```

## 4. Estrutura
```text
app/
├── models/
├── repositories/
├── services/
└── controllers/
```

- `models`: objetos do domínio
- `repositories`: persistência
- `services`: regras de negócio
- `controllers`: coordenação

## 5. Primeiras classes
```python
class Cliente:
    def __init__(self, nome, telefone):
        self.nome = nome
        self.telefone = telefone
```

```python
class Veiculo:
    def __init__(self, placa, modelo, ano):
        self.placa = placa
        self.modelo = modelo
        self.ano = ano
```

## 6. Criar objeto
```python
cliente = Cliente("Maria Oliveira", "34 98888-8888")
veiculo = Veiculo("DEF-5678", "Honda Civic", 2022)
```

## 7. Git
```bash
git status
git add .
git commit -m "feat: adiciona novos dados de teste"
git push
```

## 8. Se a rede cair
Continue localmente. O projeto não possui dependências externas nesta etapa.

### Pergunta-guia
> O que existe dentro de uma oficina?

Candidatos: `Cliente`, `Veículo`, `Serviço`, `Peça`, `OrdemDeServico`, `Mecânico`.
