from app.models.mecanica import Mecanico

class MecanicoRepositorio:
    def __init__(self, database):
        self.database = database

    def criarTabela(self):
        cursor = self.database.cursor()

        cursor.execute("""
           CREATE TABLE IF NOT EXISTS Mecanicos (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           nome TEXT NOT NULL,
           especialidade TEXT NOT NULL)         
       """)
        
        self.database.commit()

    def salvar(self, mecanico):
        cursor = self.database.cursor()

        cursor.execute("""
            INSERT INTO Mecanicos (nome, especialidade)
            VALUES (?, ?) """, (
                mecanico.nome,
                mecanico.especialidade
            ))

        mecanico.id = cursor.lastrowid
        self.database.commit()

    def buscarPorId(self, id):
        cursor = self.database.cursor()

        cursor.execute("""
            SELECT * FROM Mecanicos WHERE id = ? """, (
                id,
            ))
        
        registro = cursor.fetchone()

        return self.converterParaObjeto(registro) if registro else None

    def listarTodos(self):
        cursor = self.database.cursor()

        cursor.execute("SELECT * FROM Mecanicos")

        return [self.converterParaObjeto(r) for r in cursor.fetchall()]

    def atualizar(self, mecanico):
        cursor = self.database.cursor()

        cursor.execute("""
            UPDATE Mecanicos SET nome = ?, especialidade = ? WHERE id = ? """, (
                mecanico.nome, 
                mecanico.especialidade,
                mecanico.id
            ))
        
        self.database.commit()

    def deletar(self, id):
        cursor = self.database.cursor()

        cursor.execute("""DELETE FROM Mecanicos WHERE id = ?""", (id,))

        self.database.commit()

    def converterParaObjeto(self, registro):
        return Mecanico(
            nome=registro[1],
            especialidade=registro[2],
            id=registro[0]
        )
    