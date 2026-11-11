from nicegui import ui

from app.database.database import Database

from app.models.cliente import Cliente
from app.models.veiculo import Veiculo
from app.models.mecanica import Mecanico
from app.models.servico import Servico
from app.models.peca import Peca
from app.models.ordem_servico import OrdemDeServico

from app.repositories.ClienteRepositorio import ClienteRepositorio
from app.repositories.veiculoRepositorio import VeiculoRepositorio
from app.repositories.mecanicoRepositorio import MecanicoRepositorio
from app.repositories.servicoRepositorio import ServicoRepositorio
from app.repositories.pecaRepositorio import PecaRepositorio
from app.repositories.ordemservicoRepositorio import OrdemservicoRepositorio


# ---------------------------------------------------------------
# Conexão e repositórios
# (na classe Database use: sqlite3.connect("oficina.db", check_same_thread=False))
# ---------------------------------------------------------------
database = Database()
conexao = database.conexao  # ajuste ao nome real do atributo na sua classe

clienteRepo = ClienteRepositorio(conexao)
veiculoRepo = VeiculoRepositorio(conexao)
mecanicoRepo = MecanicoRepositorio(conexao)
servicoRepo = ServicoRepositorio(conexao)
pecaRepo = PecaRepositorio(conexao)
ordemRepo = OrdemservicoRepositorio(conexao)

# ordem importa: tabelas referenciadas primeiro
for repo in (clienteRepo, veiculoRepo, mecanicoRepo,
             servicoRepo, pecaRepo, ordemRepo):
    repo.criarTabela()


# ---------------------------------------------------------------
# Menu
# ---------------------------------------------------------------
PAGINAS = [
    ("Clientes", "/clientes"),
    ("Veículos", "/veiculos"),
    ("Mecânicos", "/mecanicos"),
    ("Serviços", "/servicos"),
    ("Peças", "/pecas"),
    ("Ordens de Serviço", "/os"),
]


def menu():
    with ui.header().classes("bg-gray-700 items-center h-20 px-6"):
        # logo à esquerda
        with ui.link(target="/"):
            ui.icon("settings", size="3rem").classes("text-black")

        # navegação centralizada
        with ui.row().classes("absolute left-1/2 -translate-x-1/2 items-center gap-10"):
            ui.link("Home", "/").classes("text-white text-lg no-underline")

            with ui.button("Serviços").props("flat no-caps icon-right=expand_more") \
                    .classes("text-white text-lg"):
                with ui.menu():
                    for texto, rota in PAGINAS:
                        ui.menu_item(texto, on_click=lambda r=rota: ui.navigate.to(r))

            ui.link("Contato", "/contato").classes("text-white text-lg no-underline")


def imagem_placeholder():
    # quadrado com degradê (céu e grama); troque por ui.image("/static/foto.png")
    ui.element("div").classes(
        "w-40 h-40 rounded-lg bg-gradient-to-b from-sky-200 to-lime-600"
    )


# ---------------------------------------------------------------
# Início
# ---------------------------------------------------------------
@ui.page("/")
def inicio():
    menu()

    with ui.column().classes("w-full max-w-5xl mx-auto p-8 gap-16"):
        # linha 1: imagem à esquerda, texto ao lado
        with ui.row().classes("w-full items-start gap-6"):
            imagem_placeholder()
            ui.label("AutoTech: gestão completa da sua oficina mecânica.") \
                .classes("text-lg")

        # linha 2: texto à esquerda, imagem à direita
        with ui.row().classes("w-full items-center justify-between"):
            ui.label("Cadastre clientes, veículos e mecânicos e acompanhe cada ordem de serviço.") \
                .classes("text-lg max-w-md")
            imagem_placeholder()


@ui.page("/contato")
def pagina_contato():
    menu()
    with ui.column().classes("w-full max-w-5xl mx-auto p-8 gap-4"):
        ui.label("Contato").classes("text-2xl font-bold")
        ui.label("Telefone: (00) 00000-0000")
        ui.label("E-mail: contato@autotech.com")


# ---------------------------------------------------------------
# Clientes
# ---------------------------------------------------------------
@ui.page("/clientes")
def pagina_clientes():
    menu()

    @ui.refreshable
    def tabela():
        ui.table(
            columns=[
                {"name": "id", "label": "ID", "field": "id"},
                {"name": "nome", "label": "Nome", "field": "nome"},
                {"name": "telefone", "label": "Telefone", "field": "telefone"},
            ],
            rows=[{"id": c.id, "nome": c.nome, "telefone": c.telefone}
                  for c in clienteRepo.listarTodos()],
            row_key="id",
        )

    with ui.card().classes("m-4"):
        ui.label("Novo cliente").classes("text-lg")
        nome = ui.input("Nome")
        telefone = ui.input("Telefone")

        def salvar():
            if not nome.value or not telefone.value:
                ui.notify("Preencha todos os campos", type="warning")
                return
            clienteRepo.salvar(Cliente(nome.value, telefone.value))
            nome.value = ""
            telefone.value = ""
            tabela.refresh()
            ui.notify("Cliente salvo!", type="positive")

        ui.button("Salvar", on_click=salvar)

    with ui.column().classes("m-4"):
        tabela()


# ---------------------------------------------------------------
# Veículos
# ---------------------------------------------------------------
@ui.page("/veiculos")
def pagina_veiculos():
    menu()

    @ui.refreshable
    def tabela():
        ui.table(
            columns=[
                {"name": "id", "label": "ID", "field": "id"},
                {"name": "placa", "label": "Placa", "field": "placa"},
                {"name": "modelo", "label": "Modelo", "field": "modelo"},
                {"name": "ano", "label": "Ano", "field": "ano"},
            ],
            rows=[{"id": v.id, "placa": v.placa, "modelo": v.modelo, "ano": v.ano}
                  for v in veiculoRepo.listarTodos()],
            row_key="id",
        )

    with ui.card().classes("m-4"):
        ui.label("Novo veículo").classes("text-lg")
        placa = ui.input("Placa")
        modelo = ui.input("Modelo")
        ano = ui.number("Ano", format="%.0f")

        def salvar():
            if not placa.value or not modelo.value or not ano.value:
                ui.notify("Preencha todos os campos", type="warning")
                return
            try:
                veiculoRepo.salvar(Veiculo(placa.value, modelo.value, int(ano.value)))
            except Exception:
                ui.notify("Não foi possível salvar (placa já cadastrada?)", type="negative")
                return
            placa.value = ""
            modelo.value = ""
            ano.value = None
            tabela.refresh()
            ui.notify("Veículo salvo!", type="positive")

        ui.button("Salvar", on_click=salvar)

    with ui.column().classes("m-4"):
        tabela()


# ---------------------------------------------------------------
# Mecânicos
# ---------------------------------------------------------------
@ui.page("/mecanicos")
def pagina_mecanicos():
    menu()

    @ui.refreshable
    def tabela():
        ui.table(
            columns=[
                {"name": "id", "label": "ID", "field": "id"},
                {"name": "nome", "label": "Nome", "field": "nome"},
                {"name": "especialidade", "label": "Especialidade", "field": "especialidade"},
            ],
            rows=[{"id": m.id, "nome": m.nome, "especialidade": m.especialidade}
                  for m in mecanicoRepo.listarTodos()],
            row_key="id",
        )

    with ui.card().classes("m-4"):
        ui.label("Novo mecânico").classes("text-lg")
        nome = ui.input("Nome")
        especialidade = ui.input("Especialidade")

        def salvar():
            if not nome.value or not especialidade.value:
                ui.notify("Preencha todos os campos", type="warning")
                return
            mecanicoRepo.salvar(Mecanico(nome.value, especialidade.value))
            nome.value = ""
            especialidade.value = ""
            tabela.refresh()
            ui.notify("Mecânico salvo!", type="positive")

        ui.button("Salvar", on_click=salvar)

    with ui.column().classes("m-4"):
        tabela()


# ---------------------------------------------------------------
# Serviços
# ---------------------------------------------------------------
@ui.page("/servicos")
def pagina_servicos():
    menu()

    @ui.refreshable
    def tabela():
        ui.table(
            columns=[
                {"name": "id", "label": "ID", "field": "id"},
                {"name": "descricao", "label": "Descrição", "field": "descricao"},
                {"name": "valor", "label": "Valor", "field": "valor"},
            ],
            rows=[{"id": s.id, "descricao": s.descricao, "valor": f"R$ {s.valor:.2f}"}
                  for s in servicoRepo.listarTodos()],
            row_key="id",
        )

    with ui.card().classes("m-4"):
        ui.label("Novo serviço").classes("text-lg")
        descricao = ui.input("Descrição")
        valor = ui.number("Valor (R$)", format="%.2f", min=0)

        def salvar():
            if not descricao.value or valor.value is None:
                ui.notify("Preencha todos os campos", type="warning")
                return
            servicoRepo.salvar(Servico(descricao.value, float(valor.value)))
            descricao.value = ""
            valor.value = None
            tabela.refresh()
            ui.notify("Serviço salvo!", type="positive")

        ui.button("Salvar", on_click=salvar)

    with ui.column().classes("m-4"):
        tabela()


# ---------------------------------------------------------------
# Peças
# ---------------------------------------------------------------
@ui.page("/pecas")
def pagina_pecas():
    menu()

    @ui.refreshable
    def tabela():
        ui.table(
            columns=[
                {"name": "id", "label": "ID", "field": "id"},
                {"name": "nome", "label": "Nome", "field": "nome"},
                {"name": "preco", "label": "Preço", "field": "preco"},
                {"name": "estoque", "label": "Estoque", "field": "estoque"},
            ],
            rows=[{"id": p.id, "nome": p.descricao, "preco": f"R$ {p.valor:.2f}",
                   "estoque": p.qntd_disponivel}
                  for p in pecaRepo.listarTodos()],
            row_key="id",
        )

    with ui.card().classes("m-4"):
        ui.label("Nova peça").classes("text-lg")
        nome = ui.input("Nome")
        preco = ui.number("Preço (R$)", format="%.2f", min=0)
        estoque = ui.number("Estoque", format="%.0f", min=0)

        def salvar():
            if not nome.value or preco.value is None or estoque.value is None:
                ui.notify("Preencha todos os campos", type="warning")
                return
            pecaRepo.salvar(Peca(nome.value, float(preco.value), int(estoque.value)))
            nome.value = ""
            preco.value = None
            estoque.value = None
            tabela.refresh()
            ui.notify("Peça salva!", type="positive")

        ui.button("Salvar", on_click=salvar)

    with ui.column().classes("m-4"):
        tabela()


# ---------------------------------------------------------------
# Ordens de Serviço
# ---------------------------------------------------------------
@ui.page("/os")
def pagina_os():
    menu()

    # dicionários {id: texto} que alimentam os campos de seleção
    clientes = {c.id: c.nome for c in clienteRepo.listarTodos()}
    veiculos = {v.id: f"{v.modelo} - {v.placa}" for v in veiculoRepo.listarTodos()}
    mecanicos = {m.id: m.nome for m in mecanicoRepo.listarTodos()}
    servicos = {s.id: s.descricao for s in servicoRepo.listarTodos()}
    pecas = {p.id: p.descricao for p in pecaRepo.listarTodos()}

    @ui.refreshable
    def tabela():
        linhas = []
        for o in ordemRepo.listarTodos():
            linhas.append({
                "id": o.id,
                "cliente": o.cliente.nome,
                "veiculo": f"{o.veiculo.modelo} ({o.veiculo.placa})",
                "mecanico": o.mecanico.nome,
                "servicos": ", ".join(s.descricao for s in o.servicos),
                "pecas": ", ".join(p.descricao for p in o.pecas),
                "total": f"R$ {o.calcular_total():.2f}",  # regra do domínio
                "status": o.status,
            })
        ui.table(
            columns=[{"name": k, "label": k.capitalize(), "field": k}
                     for k in ("id", "cliente", "veiculo", "mecanico",
                               "servicos", "pecas", "total", "status")],
            rows=linhas,
            row_key="id",
        )

    with ui.card().classes("m-4"):
        ui.label("Nova ordem de serviço").classes("text-lg")
        sel_cliente = ui.select(clientes, label="Cliente").classes("w-64")
        sel_veiculo = ui.select(veiculos, label="Veículo").classes("w-64")
        sel_mecanico = ui.select(mecanicos, label="Mecânico").classes("w-64")
        sel_servicos = ui.select(servicos, label="Serviços", multiple=True).classes("w-64")
        sel_pecas = ui.select(pecas, label="Peças", multiple=True).classes("w-64")

        def criar():
            if not (sel_cliente.value and sel_veiculo.value and sel_mecanico.value):
                ui.notify("Escolha cliente, veículo e mecânico", type="warning")
                return

            ordem = OrdemDeServico(
                clienteRepo.buscarPorId(sel_cliente.value),
                veiculoRepo.buscarPorId(sel_veiculo.value),
                mecanicoRepo.buscarPorId(sel_mecanico.value),
            )
            for id_servico in sel_servicos.value:
                ordem.adicionar_servico(servicoRepo.buscarPorId(id_servico))
            for id_peca in sel_pecas.value:
                ordem.adicionar_peca(pecaRepo.buscarPorId(id_peca))

            ordemRepo.salvar(ordem)
            tabela.refresh()
            ui.notify(f"OS nº {ordem.id} criada!", type="positive")

        ui.button("Criar OS", on_click=criar)

    with ui.column().classes("m-4"):
        tabela()


# ---------------------------------------------------------------
# Execução
# ---------------------------------------------------------------
if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title="AutoTech")