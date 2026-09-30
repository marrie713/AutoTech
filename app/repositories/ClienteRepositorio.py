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
            values (?, ?) """, (
                cliente.nome,
                cliente.telefone
            ))

        cliente.id = cursor.lastrowid

        self.database.commit()

    def converterParaObjeto(self, registro):
        return Cliente(
            nome=registro[1],
            telefone=registro[2],
            id=registro[0]
        )
    