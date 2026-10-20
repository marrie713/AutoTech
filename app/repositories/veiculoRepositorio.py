from app.models.veiculo import Veiculo

class VeiculoRepositorio:
    def __init__(self, database):
        self.database = database

    def criarTabela(self):
        cursor = self.database.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Veiculos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            placa TEXT NOT NULL UNIQUE,
            modelo TEXT NOT NULL,
            ano INTEGER NOT NULL )
        """)

        self.database.commit()

    def salvar(self, veiculo):
        cursor = self.database.cursor()

        cursor.execute("""
            INSERT INTO Veiculos (placa, modelo, ano) 
            VALUES (?, ?, ?) """, (
                veiculo.placa, 
                veiculo.modelo, 
                veiculo.ano, 
             ))
        
        veiculo.id = cursor.lastrowid
        self.database.commit()

    def buscarPorId(self, id):
            cursor = self.database.cursor()
        
            cursor.execute("""
                SELECT * FROM Veiculos WHERE id = ? """, (
                    id,
                ))
                
            registro = cursor.fetchone()
        
            return self.converterParaObjeto(registro) if registro else None
        
    def listarTodos(self):
        cursor = self.database.cursor()
        
        cursor.execute("SELECT * FROM Veiculos")
        
        return [self.converterParaObjeto(r) for r in cursor.fetchall()]
        
    def atualizar(self, cliente):
        cursor = self.database.cursor()
        
        cursor.execute("""
            UPDATE Veiculos SET nome = ?, telefone = ? WHERE id = ? """, (
                cliente.nome, 
                cliente.telefone,
                cliente.id
            ))
                
        self.database.commit()
        
    def deletar(self, id):
        cursor = self.database.cursor()
        
        cursor.execute("""DELETE FROM Veiculos WHERE id = ?""", (id,))
                            
        self.database.commit()

    def converterParaObjeto(self, registro):
        return Veiculo(
            placa=registro[1], 
            modelo=registro[2],
            ano=registro[3], 
            id=registro[0])