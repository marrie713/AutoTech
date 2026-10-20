from app.models.peca import Peca

class PecaRepositorio:
    def __init__(self, database):
        self.database = database

    def criarTabela(self):
        cursor = self.database.cursor()

        cursor.execute("""
           CREATE TABLE IF NOT EXISTS Pecas (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           descricao TEXT NOT NULL,
           valor REAL NOT NULL,
           qntd_disponivel TEXT NOT NULL )         
       """)
        
        self.database.commit()

    def salvar(self, peca):
        cursor = self.database.cursor()

        cursor.execute("""
            INSERT INTO Pecas (descricao, valor, qntd_disponivel)
            VALUES (?, ?, ?) """, (
                peca.descricao,
                peca.valor,
                peca.qntd_disponivel
            ))

        peca.id = cursor.lastrowid
        self.database.commit()

    def buscarPorId(self, id):
        cursor = self.database.cursor()

        cursor.execute("""
            SELECT * FROM Pecas WHERE id = ? """, (
                id,
            ))
        
        registro = cursor.fetchone()

        return self.converterParaObjeto(registro) if registro else None

    def listarTodos(self):
        cursor = self.database.cursor()

        cursor.execute("SELECT * FROM Pecas")

        return [self.converterParaObjeto(r) for r in cursor.fetchall()]

    def atualizar(self, peca):
        cursor = self.database.cursor()

        cursor.execute("""
            UPDATE Pecas SET descricao = ?, valor = ?, qntd_disponivel = ? WHERE id = ? """, (
                peca.nome, 
                peca.valor,
                peca.qntd_disponivel,
                peca.id
            ))
        
        self.database.commit()

    def deletar(self, id):
        cursor = self.database.cursor()

        cursor.execute(""" DELETE FROM Pecas WHERE id = ? """, (id,))

        self.database.commit()

    def converterParaObjeto(self, registro):
        return Peca(
            descricao=registro[1],
            valor=registro[2],
            qntd_disponivel=registro[3],
            id=registro[0]
        )
    