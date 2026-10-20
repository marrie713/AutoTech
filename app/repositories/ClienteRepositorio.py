from app.models.cliente import Cliente

class ClienteRepositorio:
    def __init__(self, database):
        self.database = database

    def criarTabela(self):
        cursor = self.database.cursor()

        cursor.execute("""
           CREATE TABLE IF NO EXISTS Clientes (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           nome TEXT NOT NULL,
           telefone TEXT NOT NULL)         
       """)
        
        self.database.commit()

    def salvar(self, cliente):
        cursor = self.database.cursor()

        cursor.execute("""
            INSERT INTO Clientes (nome, telefone)
            values ("Maria", "17992299229") """, (
                cliente.nome,
                cliente.telefone
            ))

        cliente.id = cursor.lastrowid

        self.database.commit()

    def buscarPorId(self, id):
        cursor = self.database.cursor()

        cursor.execute("""
            SELECT * FROM Clientes WHERE id = ? """, (
                id
            ))
        
        registro = cursor.fetchone()

        return self.converterParaObjeto(registro) if registro else None

    def listarTodos(self):
        cursor = self.database.cursor()

        cursor.execute("SELECT * FROM Clientes")

        return [self.converterParaObjeto(r) for r in cursor.fetchall()]

    def atualizar(self, cliente):
        cursor = self.database.cursor()
        
        cursor.execute("""
            UPDATE Clientes SET nome = ?, telefone = ? WHERE id = ? """, (
                cliente.nome, 
                cliente.telefone,
                cliente.id
            ))
        
        self.database.commit()

    def deletar(self, id):
        cursor = self.database.cursor()

        cursor.execute("""DELETE FROM Clientes WHERE id = ?""",
                        (id,
        ))

        self.database.commit()

    def converterParaObjeto(self, registro):
        return Cliente(
            nome=registro[1],
            telefone=registro[2],
            id=registro[0]
        )
    