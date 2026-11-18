"""
APEX ERP: interface NiceGUI para o sistema da oficina.

Esta interface só USA os repositórios. Nada do que está em app/ muda.
O arquivo está dividido em 7 partes:
  1. Conexão e repositórios
  2. Constantes (cores, status, menu)
  3. Layout (menu lateral + cabeçalho), reaproveitado por todas as páginas
  4. Componentes pequenos (tabela, cartão de indicador, formulários)
  5. Dashboard
  6. Cadastros (clientes, veículos, mecânicos, serviços, peças)
  7. Ordens de Serviço
"""
import sqlite3
from contextlib import contextmanager

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


# ===============================================================
# 1. CONEXÃO E REPOSITÓRIOS
# ===============================================================
# Na classe Database use: sqlite3.connect("oficina.db", check_same_thread=False)
database = Database()
conexao = database.conexao 

# O SQLite só aplica chaves estrangeiras se pedirmos. Assim, excluir um cliente
# que está em uma OS gera erro (que tratamos), em vez de deixar a OS "órfã".
conexao.execute("PRAGMA foreign_keys = ON")

clienteRepo = ClienteRepositorio(conexao)
veiculoRepo = VeiculoRepositorio(conexao)
mecanicoRepo = MecanicoRepositorio(conexao)
servicoRepo = ServicoRepositorio(conexao)
pecaRepo = PecaRepositorio(conexao)
ordemRepo = OrdemservicoRepositorio(conexao)

# Ordem importa: tabelas referenciadas primeiro.
for repo in (clienteRepo, veiculoRepo, mecanicoRepo,
             servicoRepo, pecaRepo, ordemRepo):
    repo.criarTabela()


# ===============================================================
# 2. CONSTANTES
# ===============================================================
STATUS = ["Orçamento", "Aguardando Peça", "Em Execução", "Concluída", "Cancelada"]
STATUS_ATIVOS = ["Orçamento", "Aguardando Peça", "Em Execução"]

ESPECIALIDADES = [
    "Motor & Câmbio",
    "Injeção & Eletrônica",
    "Suspensão & Freios",
    "Revisão Geral",
    "Elétrica",
]

# (título da seção, [(ícone, texto, rota), ...])
MENU = [
    ("Operação & Pátio", [
        ("dashboard", "Dashboard Operacional", "/"),
        ("assignment", "Ordens de Serviço", "/os"),
    ]),
    ("Cadastros & Base", [
        ("people", "Clientes", "/clientes"),
        ("directions_car", "Veículos", "/veiculos"),
        ("engineering", "Mecânicos", "/mecanicos"),
    ]),
    ("Catálogo & Suprimentos", [
        ("build", "Serviços (Mão de Obra)", "/servicos"),
        ("inventory_2", "Peças", "/pecas"),
    ]),
]

FONTES = (
    '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700'
    '&family=Space+Grotesk:wght@600;700&display=swap" rel="stylesheet">'
)

# CSS próprio: usado onde as classes do Tailwind não vencem o tema do Quasar.
CSS = """
body, .q-page, .nicegui-content { background: #0F172A !important; }
body { font-family: 'Inter', sans-serif; }
.titulo { font-family: 'Space Grotesk', sans-serif; }
.q-drawer { background: #1E293B !important; }
.q-header { background: #1E293B !important; border-bottom: 1px solid #334155; }
.q-card { background: #1E293B !important; color: #F8FAFC; }
.q-card--bordered { border: 1px solid #334155 !important; }
"""

# Modelo (template) Vue da coluna "status": desenha a etiqueta colorida.
SLOT_STATUS = """
<q-td :props="props">
  <q-badge :color="{'Concluída':'positive','Em Execução':'primary',
                    'Aguardando Peça':'warning','Orçamento':'grey-7',
                    'Cancelada':'negative'}[props.value] || 'grey-7'">
    {{ props.value }}
  </q-badge>
</q-td>
"""

# Modelo da coluna de ações: dois botões que "emitem" eventos para o Python.
SLOT_ACOES = """
<q-td :props="props" class="text-right">
  <q-btn flat dense round icon="edit" color="primary"
         @click="() => $parent.$emit('editar', props.row)" />
  <q-btn flat dense round icon="delete" color="negative"
         @click="() => $parent.$emit('excluir', props.row)" />
</q-td>
"""


def brl(valor):
    """Formata número como moeda brasileira: 1234.5 -> R$ 1.234,50"""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


# ===============================================================
# 3. LAYOUT (menu lateral + cabeçalho)
# ===============================================================
def item_menu(icone, texto, rota, rota_atual):
    ativo = rota == rota_atual
    cores = ("bg-[#F97316] text-white shadow-md" if ativo
             else "text-[#94A3B8] hover:bg-[#0F172A] hover:text-white")
    with ui.link(target=rota).classes("w-full no-underline"):
        with ui.row().classes(
                f"w-full items-center gap-3 px-3.5 py-2.5 rounded-xl no-wrap {cores}"):
            ui.icon(icone).classes("text-lg")
            ui.label(texto).classes("text-sm font-medium")


@contextmanager
def layout(titulo, subtitulo, rota_atual):
    """
    Monta a "moldura" da página. Uso:

        with layout("Título", "Subtítulo", "/rota"):
            ...conteúdo da página...
    """
    ui.dark_mode().enable()
    ui.colors(primary="#F97316", positive="#34D399",
              negative="#EF4444", warning="#F59E0B")
    ui.add_head_html(FONTES)
    ui.add_css(CSS)

    # Menu lateral
    with ui.left_drawer(top_corner=True).props("width=270 bordered") as menu:
        with ui.row().classes("h-16 items-center gap-3 px-5 no-wrap"):
            with ui.element("div").classes(
                    "w-9 h-9 rounded-lg bg-[#F97316] flex items-center justify-center"):
                ui.icon("settings").classes("text-white text-xl")
            with ui.column().classes("gap-0"):
                with ui.row().classes("gap-1 no-wrap"):
                    ui.label("APEX").classes("titulo text-lg font-bold text-white")
                    ui.label("ERP").classes("titulo text-lg font-bold text-[#F97316]")
                ui.label("GESTÃO DE OFICINA").classes(
                    "text-[10px] tracking-widest text-[#94A3B8]")

        with ui.column().classes("w-full gap-1 p-3.5"):
            for secao, itens in MENU:
                ui.label(secao.upper()).classes(
                    "px-3 pt-4 pb-2 text-[10px] tracking-widest text-[#94A3B8]")
                for icone, texto, rota in itens:
                    item_menu(icone, texto, rota, rota_atual)

    # Cabeçalho
    with ui.header().classes("h-16 items-center justify-between px-6"):
        with ui.row().classes("items-center gap-3 no-wrap"):
            ui.button(icon="menu", on_click=menu.toggle) \
                .props("flat dense color=white").classes("lg:hidden")
            with ui.column().classes("gap-0"):
                ui.label(titulo).classes("titulo text-xl font-bold text-white")
                ui.label(subtitulo).classes("text-xs text-[#94A3B8] hidden sm:block")
        ui.button("Nova OS", icon="add",
                  on_click=lambda: ui.navigate.to("/os?nova=1")) \
            .props("no-caps unelevated").classes("rounded-xl font-semibold")

    # Área de conteúdo
    with ui.column().classes("w-full max-w-[1600px] mx-auto gap-6"):
        yield


# ===============================================================
# 4. COMPONENTES PEQUENOS
# ===============================================================
def kpi(titulo, valor, icone, classe_valor="text-white"):
    """Cartão de indicador (número grande com título e ícone)."""
    with ui.card().props("flat bordered").classes("flex-1 min-w-[220px] p-5 gap-1"):
        with ui.row().classes("w-full items-center justify-between no-wrap"):
            ui.label(titulo.upper()).classes(
                "text-xs font-semibold tracking-wider text-[#94A3B8]")
            ui.icon(icone).classes("text-[#F97316]")
        ui.label(valor).classes(f"text-3xl font-bold font-mono {classe_valor}")


def tabela_dados(colunas, linhas, ao_editar=None, ao_excluir=None):
    """
    Tabela padrão.
      colunas: [("campo", "Rótulo"), ...]
      linhas:  lista de dicionários (cada um com a chave "id")
    Se ao_editar/ao_excluir forem passados, aparece a coluna de ações.
    """
    definicao = [{"name": c, "label": r, "field": c, "align": "left"}
                 for c, r in colunas]
    com_acoes = ao_editar is not None or ao_excluir is not None
    if com_acoes:
        definicao.append({"name": "acoes", "label": "", "field": "acoes",
                          "align": "right"})

    tabela = ui.table(columns=definicao, rows=linhas, row_key="id", pagination=10) \
        .props('flat dark no-data-label="Nenhum registro encontrado"') \
        .classes("w-full")

    if any(c == "status" for c, _ in colunas):
        tabela.add_slot("body-cell-status", SLOT_STATUS)
    if com_acoes:
        tabela.add_slot("body-cell-acoes", SLOT_ACOES)
        if ao_editar:
            tabela.on("editar", lambda e: ao_editar(e.args))
        if ao_excluir:
            tabela.on("excluir", lambda e: ao_excluir(e.args))
    return tabela


def confirmar_exclusao(texto, ao_confirmar):
    with ui.dialog() as dialogo, ui.card().classes("gap-3"):
        ui.label(texto)
        with ui.row().classes("w-full justify-end"):
            ui.button("Cancelar", on_click=dialogo.close).props("flat no-caps")

            def confirmar():
                dialogo.close()
                ao_confirmar()

            ui.button("Excluir", color="negative", on_click=confirmar).props("no-caps")
    dialogo.open()


def campo(nome, rotulo, tipo="texto", opcoes=None):
    """Descreve um campo de formulário. tipo: texto | inteiro | dinheiro | select"""
    return {"nome": nome, "rotulo": rotulo, "tipo": tipo, "opcoes": opcoes}


def abrir_formulario(cfg, objeto, ao_concluir):
    """
    Formulário (janela) genérico de cadastro, montado a partir da lista
    de campos. objeto=None cria um registro novo; senão edita o existente.
    """
    editando = objeto is not None
    entradas = {}

    with ui.dialog() as dialogo, ui.card().classes("w-[460px] max-w-full gap-3"):
        ui.label(f"{'Editar' if editando else 'Novo'} {cfg['singular'].lower()}") \
            .classes("titulo text-lg font-bold")

        for c in cfg["campos"]:
            valor = getattr(objeto, c["nome"]) if editando else None
            if c["tipo"] == "texto":
                entrada = ui.input(c["rotulo"], value=valor or "")
            elif c["tipo"] == "select":
                entrada = ui.select(c["opcoes"], label=c["rotulo"], value=valor)
            elif c["tipo"] == "inteiro":
                entrada = ui.number(c["rotulo"], value=valor, min=0, format="%.0f")
            else:  # dinheiro
                entrada = ui.number(c["rotulo"], value=valor, min=0, format="%.2f")
            entrada.props("outlined dense").classes("w-full")
            entradas[c["nome"]] = entrada

        def salvar():
            valores = []
            for c in cfg["campos"]:
                v = entradas[c["nome"]].value
                if v is None or (isinstance(v, str) and not v.strip()):
                    ui.notify("Preencha todos os campos", type="warning")
                    return
                if c["tipo"] == "inteiro":
                    v = int(v)
                elif c["tipo"] == "dinheiro":
                    v = float(v)
                elif isinstance(v, str):
                    v = v.strip()
                valores.append(v)

            try:
                if editando:
                    for c, v in zip(cfg["campos"], valores):
                        setattr(objeto, c["nome"], v)
                    cfg["repo"].atualizar(objeto)
                else:
                    cfg["repo"].salvar(cfg["classe"](*valores))
            except sqlite3.Error as erro:
                conexao.rollback()
                ui.notify(f"Não foi possível salvar: {erro}", type="negative")
                return

            dialogo.close()
            ao_concluir()
            ui.notify("Registro salvo!", type="positive")

        with ui.row().classes("w-full justify-end"):
            ui.button("Cancelar", on_click=dialogo.close).props("flat no-caps")
            ui.button("Salvar", icon="save", on_click=salvar).props("no-caps")
    dialogo.open()


def linha_os(o):
    """Transforma uma OrdemDeServico em dicionário para a tabela."""
    return {
        "id": o.id,
        "cliente": o.cliente.nome,
        "veiculo": f"{o.veiculo.modelo} ({o.veiculo.placa})",
        "mecanico": o.mecanico.nome,
        "servicos": ", ".join(s.descricao for s in o.servicos),
        "pecas": ", ".join(p.descricao for p in o.pecas),
        "total": brl(o.calcular_total()),  # regra do domínio, não um valor fixo
        "status": o.status,
    }


# ===============================================================
# 5. DASHBOARD
# ===============================================================
@ui.page("/")
def pagina_dashboard():
    with layout("Dashboard Operacional",
                "Visão do pátio, faturamento e equipe", "/"):
        ordens = ordemRepo.listarTodos()
        ativas = [o for o in ordens if o.status in STATUS_ATIVOS]
        concluidas = [o for o in ordens if o.status == "Concluída"]
        faturamento = sum(o.calcular_total() for o in concluidas)
        ticket = faturamento / len(concluidas) if concluidas else 0

        with ui.row().classes("w-full gap-4"):
            kpi("OS ativas no pátio", str(len(ativas)), "assignment")
            kpi("Faturamento concluído", brl(faturamento), "payments",
                "text-emerald-400")
            kpi("Ticket médio / OS", brl(ticket), "receipt_long")
            kpi("Total de OS", str(len(ordens)), "folder_open")

        with ui.row().classes("w-full gap-4 items-start"):
            with ui.card().props("flat bordered").classes("flex-1 min-w-[320px] p-5"):
                ui.label("Veículos em atendimento").classes(
                    "titulo text-base font-bold")
                tabela_dados(
                    [("id", "OS"), ("veiculo", "Veículo"), ("cliente", "Cliente"),
                     ("mecanico", "Mecânico"), ("total", "Total"),
                     ("status", "Status")],
                    [linha_os(o) for o in ativas],
                )

            with ui.card().props("flat bordered").classes("w-80 p-5 gap-3"):
                ui.label("Produtividade da equipe").classes(
                    "titulo text-base font-bold")
                mecanicos = mecanicoRepo.listarTodos()
                if not mecanicos:
                    ui.label("Nenhum mecânico cadastrado.").classes(
                        "text-sm text-[#94A3B8]")
                for m in mecanicos:
                    qtd = sum(1 for o in concluidas if o.mecanico.id == m.id)
                    with ui.row().classes("w-full items-center justify-between"):
                        with ui.column().classes("gap-0"):
                            ui.label(m.nome).classes("text-sm font-semibold")
                            ui.label(m.especialidade).classes(
                                "text-xs text-[#94A3B8]")
                        ui.label(f"{qtd} concluída(s)").classes(
                            "text-xs text-emerald-400")


# ===============================================================
# 6. CADASTROS (uma configuração por entidade, uma página para todas)
# ===============================================================
CADASTROS = {
    "clientes": dict(
        rota="/clientes", singular="Cliente", repo=clienteRepo, classe=Cliente,
        titulo="Cadastro de Clientes", subtitulo="Base de clientes da oficina",
        campos=[campo("nome", "Nome"), campo("telefone", "Telefone")],
    ),
    "veiculos": dict(
        rota="/veiculos", singular="Veículo", repo=veiculoRepo, classe=Veiculo,
        titulo="Frota & Veículos", subtitulo="Consulta por placa, modelo e ano",
        campos=[campo("placa", "Placa"), campo("modelo", "Modelo"),
                campo("ano", "Ano", "inteiro")],
    ),
    "mecanicos": dict(
        rota="/mecanicos", singular="Mecânico", repo=mecanicoRepo, classe=Mecanico,
        titulo="Equipe Técnica & Mecânicos", subtitulo="Profissionais e especialidades",
        campos=[campo("nome", "Nome"),
                campo("especialidade", "Especialidade", "select", ESPECIALIDADES)],
    ),
    "servicos": dict(
        rota="/servicos", singular="Serviço", repo=servicoRepo, classe=Servico,
        titulo="Catálogo de Serviços", subtitulo="Serviços e valores de mão de obra",
        campos=[campo("descricao", "Descrição"), campo("valor", "Valor", "dinheiro")],
    ),
    "pecas": dict(
        rota="/pecas", singular="Peça", repo=pecaRepo, classe=Peca,
        titulo="Peças & Estoque", subtitulo="Peças, preços e quantidade em estoque",
        campos=[campo("descricao", "Descrição"), campo("valor", "Valor", "dinheiro"),
                campo("estoque", "Estoque", "inteiro")],
    ),
}


def montar_pagina_cadastro(chave):
    cfg = CADASTROS[chave]

    @ui.page(cfg["rota"])
    def pagina():
        with layout(cfg["titulo"], cfg["subtitulo"], cfg["rota"]):

            @ui.refreshable
            def tabela():
                linhas = []
                for obj in cfg["repo"].listarTodos():
                    linha = {"id": obj.id}
                    for c in cfg["campos"]:
                        v = getattr(obj, c["nome"])
                        linha[c["nome"]] = brl(v) if c["tipo"] == "dinheiro" else v
                    linhas.append(linha)

                colunas = [("id", "ID")] + [(c["nome"], c["rotulo"])
                                            for c in cfg["campos"]]

                def editar(row):
                    abrir_formulario(cfg, cfg["repo"].buscarPorId(row["id"]),
                                     tabela.refresh)

                def excluir(row):
                    def confirmado():
                        try:
                            cfg["repo"].deletar(row["id"])
                        except sqlite3.Error:
                            conexao.rollback()
                            ui.notify("Não é possível excluir: o registro está "
                                      "em uso em uma OS.", type="negative")
                            return
                        tabela.refresh()
                        ui.notify("Registro excluído", type="positive")

                    confirmar_exclusao("Excluir este registro?", confirmado)

                with ui.card().props("flat bordered").classes("w-full p-5"):
                    tabela_dados(colunas, linhas, editar, excluir)

            with ui.row().classes("w-full justify-end"):
                ui.button(f"Novo {cfg['singular'].lower()}", icon="add",
                          on_click=lambda: abrir_formulario(cfg, None, tabela.refresh)) \
                    .props("no-caps unelevated").classes("rounded-xl")
            tabela()


for _chave in CADASTROS:
    montar_pagina_cadastro(_chave)


# ===============================================================
# 7. ORDENS DE SERVIÇO
# ===============================================================
def abrir_formulario_os(ordem, ao_concluir):
    editando = ordem is not None

    # {id: texto}: o usuário vê o texto, o .value devolve o id
    clientes = {c.id: c.nome for c in clienteRepo.listarTodos()}
    veiculos = {v.id: f"{v.modelo} - {v.placa}" for v in veiculoRepo.listarTodos()}
    mecanicos = {m.id: m.nome for m in mecanicoRepo.listarTodos()}
    servicos = {s.id: f"{s.descricao} ({brl(s.valor)})"
                for s in servicoRepo.listarTodos()}
    pecas = {p.id: f"{p.descricao} ({brl(p.valor)})" for p in pecaRepo.listarTodos()}

    with ui.dialog() as dialogo, ui.card().classes("w-[560px] max-w-full gap-3"):
        ui.label("Editar ordem de serviço" if editando else "Nova ordem de serviço") \
            .classes("titulo text-lg font-bold")

        sel_cliente = ui.select(clientes, label="Cliente",
                                value=ordem.cliente.id if editando else None)
        sel_veiculo = ui.select(veiculos, label="Veículo",
                                value=ordem.veiculo.id if editando else None)
        sel_mecanico = ui.select(mecanicos, label="Mecânico responsável",
                                 value=ordem.mecanico.id if editando else None)
        sel_status = ui.select(STATUS, label="Status",
                               value=ordem.status if editando else "Orçamento")
        sel_servicos = ui.select(servicos, label="Serviços", multiple=True,
                                 value=[s.id for s in ordem.servicos] if editando else [])
        sel_pecas = ui.select(pecas, label="Peças", multiple=True,
                              value=[p.id for p in ordem.pecas] if editando else [])
        for s in (sel_cliente, sel_veiculo, sel_mecanico, sel_status,
                  sel_servicos, sel_pecas):
            s.props("outlined dense use-chips").classes("w-full")

        total = ui.label().classes("text-lg font-bold font-mono text-emerald-400")

        def atualizar_total():
            # Monta uma OS temporária só para pedir o total ao domínio.
            temporaria = OrdemDeServico(None, None, None)
            for i in sel_servicos.value:
                temporaria.adicionar_servico(servicoRepo.buscarPorId(i))
            for i in sel_pecas.value:
                temporaria.adicionar_peca(pecaRepo.buscarPorId(i))
            total.text = f"Total: {brl(temporaria.calcular_total())}"

        sel_servicos.on_value_change(lambda: atualizar_total())
        sel_pecas.on_value_change(lambda: atualizar_total())
        atualizar_total()

        def salvar():
            if not (sel_cliente.value and sel_veiculo.value and sel_mecanico.value):
                ui.notify("Escolha cliente, veículo e mecânico", type="warning")
                return

            cliente = clienteRepo.buscarPorId(sel_cliente.value)
            veiculo = veiculoRepo.buscarPorId(sel_veiculo.value)
            mecanico = mecanicoRepo.buscarPorId(sel_mecanico.value)

            if editando:
                o = ordem
                o.cliente, o.veiculo, o.mecanico = cliente, veiculo, mecanico
                o.status = sel_status.value
            else:
                o = OrdemDeServico(cliente, veiculo, mecanico,
                                   status=sel_status.value)

            o.servicos = []
            o.pecas = []
            for i in sel_servicos.value:
                o.adicionar_servico(servicoRepo.buscarPorId(i))
            for i in sel_pecas.value:
                o.adicionar_peca(pecaRepo.buscarPorId(i))

            try:
                if editando:
                    ordemRepo.atualizar(o)
                else:
                    ordemRepo.salvar(o)
            except sqlite3.Error as erro:
                conexao.rollback()
                ui.notify(f"Não foi possível salvar: {erro}", type="negative")
                return

            dialogo.close()
            ao_concluir()
            ui.notify(f"OS nº {o.id} salva!", type="positive")

        with ui.row().classes("w-full justify-end"):
            ui.button("Cancelar", on_click=dialogo.close).props("flat no-caps")
            ui.button("Salvar OS", icon="check", on_click=salvar).props("no-caps")
    dialogo.open()


@ui.page("/os")
def pagina_os(nova: int = 0):
    with layout("Ordens de Serviço (OS)",
                "Orçamentos, execução, peças e total", "/os"):

        filtro = ui.toggle(["Todas"] + STATUS, value="Todas",
                           on_change=lambda: tabela.refresh()) \
            .props("no-caps unelevated")

        @ui.refreshable
        def tabela():
            ordens = ordemRepo.listarTodos()
            if filtro.value != "Todas":
                ordens = [o for o in ordens if o.status == filtro.value]

            def editar(row):
                abrir_formulario_os(ordemRepo.buscarPorId(row["id"]), tabela.refresh)

            def excluir(row):
                def confirmado():
                    try:
                        ordemRepo.deletar(row["id"])
                    except sqlite3.Error as erro:
                        conexao.rollback()
                        ui.notify(f"Não foi possível excluir: {erro}", type="negative")
                        return
                    tabela.refresh()
                    ui.notify("OS excluída", type="positive")

                confirmar_exclusao(f"Excluir a OS nº {row['id']}?", confirmado)

            with ui.card().props("flat bordered").classes("w-full p-5"):
                tabela_dados(
                    [("id", "OS"), ("cliente", "Cliente"), ("veiculo", "Veículo"),
                     ("mecanico", "Mecânico"), ("servicos", "Serviços"),
                     ("pecas", "Peças"), ("total", "Total"), ("status", "Status")],
                    [linha_os(o) for o in ordens],
                    editar, excluir,
                )

        with ui.row().classes("w-full justify-end"):
            ui.button("Nova OS", icon="add",
                      on_click=lambda: abrir_formulario_os(None, tabela.refresh)) \
                .props("no-caps unelevated").classes("rounded-xl")
        tabela()

        if nova:  # veio do botão "Nova OS" do cabeçalho (/os?nova=1)
            abrir_formulario_os(None, tabela.refresh)


# ===============================================================
# EXECUÇÃO
# ===============================================================
if __name__ in {"__main__", "__mp_main__"}:
    ui.run(title="APEX ERP", favicon="🔧")