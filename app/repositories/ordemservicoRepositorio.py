from app.models.ordem_servico import OrdemDeServico
from app.repositories.ClienteRepositorio import ClienteRepositorio
from app.repositories.veiculoRepositorio import VeiculoRepositorio
from app.repositories.mecanicoRepositorio import MecanicoRepositorio
from app.repositories.servicoRepositorio import ServicoRepositorio
from app.repositories.pecaRepositorio import PecaRepositorio

class OrdemservicoRepositorio:
    def __init__(self, database):
        self.database = database
        self.clienteRepositorio = ClienteRepositorio(database)
        self.veiculoRepositorio = VeiculoRepositorio(database)
        self.mecanicoRepositorio = MecanicoRepositorio(database)
        self.servicoRepositorio = ServicoRepositorio(database)
        self.pecaRepositorio = PecaRepositorio(database)

    def criarTabela(self):
        cursor = self.database.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS OrdensDeServico (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER NOT NULL,
                veiculo_id INTEGER NOT NULL,
                mecanico_id INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'Aberta',
                FOREIGN KEY (cliente_id) REFERENCES Clientes(id),
                FOREIGN KEY (veiculo_id) REFERENCES Veiculos(id),
                FOREIGN KEY (mecanico_id) REFERENCES Mecanicos(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS OS_Servicos (
                os_id INTEGER NOT NULL,
                servico_id INTEGER NOT NULL,
                PRIMARY KEY (os_id, servico_id),
                FOREIGN KEY (os_id) REFERENCES OrdensDeServico(id),
                FOREIGN KEY (servico_id) REFERENCES Servicos(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS OS_Pecas (
                os_id INTEGER NOT NULL,
                peca_id INTEGER NOT NULL,
                PRIMARY KEY (os_id, peca_id),
                FOREIGN KEY (os_id) REFERENCES OrdensDeServico(id),
                FOREIGN KEY (peca_id) REFERENCES Pecas(id)
            )
        """)

        self.database.commit()

    def salvar(self, ordem):
        cursor = self.database.cursor()

        cursor.execute("""
            INSERT INTO OrdensDeServico (cliente_id, veiculo_id, mecanico_id, status)
            VALUES (?, ?, ?, ?)
        """, (ordem.cliente.id, ordem.veiculo.id, ordem.mecanico.id, ordem.status))

        ordem.id = cursor.lastrowid

        self._salvarItens(cursor, ordem)

        self.database.commit()

    def _salvarItens(self, cursor, ordem):
        for servico in ordem.servicos: 
            cursor.execute(
                "INSERT INTO OS_Servicos (os_id, servico_id) VALUES (?, ?)",
                (ordem.id, servico.id)
            )

        for peca in ordem.pecas:       
            cursor.execute(
                "INSERT INTO OS_Pecas (os_id, peca_id) VALUES (?, ?)",
                (ordem.id, peca.id)
            )

    def buscarPorId(self, id):
        cursor = self.database.cursor()

        cursor.execute("SELECT * FROM OrdensDeServico WHERE id = ?", (id,))

        registro = cursor.fetchone()

        return self.converterParaObjeto(registro) if registro else None

    def listarTodos(self):
        cursor = self.database.cursor()

        cursor.execute("SELECT * FROM OrdensDeServico")

        return [self.converterParaObjeto(r) for r in cursor.fetchall()]

    def atualizar(self, ordem):
        cursor = self.database.cursor()

        cursor.execute("""
            UPDATE OrdensDeServico
            SET cliente_id = ?, veiculo_id = ?, mecanico_id = ?, status = ? 
            WHERE id = ?
        """, (ordem.cliente.id, ordem.veiculo.id, ordem.mecanico.id, ordem.status, ordem.id))

        cursor.execute("DELETE FROM OS_Servicos WHERE os_id = ?", (ordem.id,))
        cursor.execute("DELETE FROM OS_Pecas WHERE os_id = ?", (ordem.id,))
        self._salvarItens(cursor, ordem)

        self.database.commit()

    def deletar(self, id):
        cursor = self.database.cursor()

        cursor.execute("DELETE FROM OS_Servicos WHERE os_id = ?", (id,))
        cursor.execute("DELETE FROM OS_Pecas WHERE os_id = ?", (id,))
        cursor.execute("DELETE FROM OrdensDeServico WHERE id = ?", (id,))

        self.database.commit()

    def converterParaObjeto(self, registro):
        ordem = OrdemDeServico(
            id=registro[0],
            cliente=self.clienteRepositorio.buscarPorId(registro[1]),
            veiculo=self.veiculoRepositorio.buscarPorId(registro[2]),
            mecanico=self.mecanicoRepositorio.buscarPorId(registro[3]),
            status=registro[4]
        )

        cursor = self.database.cursor()

        cursor.execute("SELECT servico_id FROM OS_Servicos WHERE os_id = ?", (ordem.id,))
        for linha in cursor.fetchall():
            ordem.adicionar_servico(self.servicoRepositorio.buscarPorId(linha[0]))

        cursor.execute("SELECT peca_id FROM OS_Pecas WHERE os_id = ?", (ordem.id,))
        for linha in cursor.fetchall():
            ordem.adicionar_peca(self.pecaRepositorio.buscarPorId(linha[0]))

        return ordem