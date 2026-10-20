from app.models.servico import Servico

class ServicoRepositorio:
    def __init__(self, database):
        self.database = database

    def criarTabela(self):
        cursor = self.database.cursor()

        cursor.execute("""
           CREATE TABLE IF NOT EXISTS Servicos (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           descricao TEXT NOT NULL,
           valor REAL NOT NULL)         
       """)
        
        self.database.commit()

    def salvar(self, servico):
        cursor = self.database.cursor()

        cursor.execute("""
            INSERT INTO Servicos (descricao, valor)
            values (?, ?) """, (
                servico.descricao,
                servico.valor
            ))

        servico.id = cursor.lastrowid
        self.database.commit()

    def buscarPorId(self, id):
        cursor = self.database.cursor()

        cursor.execute("""
            SELECT * FROM Servicos WHERE id = ? """, (
                id,
            ))
        
        registro = cursor.fetchone()

        return self.converterParaObjeto(registro) if registro else None

    def listarTodos(self):
        cursor = self.database.cursor()

        cursor.execute("SELECT * FROM Servicos")

        return [self.converterParaObjeto(r) for r in cursor.fetchall()]

    def atualizar(self, servico):
        cursor = self.database.cursor()

        cursor.execute("""
            UPDATE Servicos SET descricao = ?, valor = ? WHERE id = ? """, (
                servico.descricao, 
                servico.valor,
                servico.id
            ))
        
        self.database.commit()

    def deletar(self, id):
        cursor = self.database.cursor()

        cursor.execute("""DELETE FROM Servicos WHERE id = ?""", (id,))
        
        self.database.commit()

    def converterParaObjeto(self, registro):
        return Servico(
            descricao=registro[1],
            valor=registro[2],
            id=registro[0]
        )
    