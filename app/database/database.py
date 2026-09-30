import sqlite3

class Database:
    def __init__(self):
        self.conexao = sqlite3.connect("oficina.db")

    def cursor(self):
        return self.conexao.cursor()

    def commit(self):
        self.conexao.commit()

    def fechar(self):
            self.conexao.close()