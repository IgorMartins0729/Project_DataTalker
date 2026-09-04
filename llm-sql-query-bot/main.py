from fastapi import FastAPI
import sqlite3

app = FastAPI()
db_path = "estoque.db"

def init_db():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS produtos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT, 
                    departamento TEXT,
                    data_fabri TEXT,
                    data_venci TEXT
                )""")

    if c.execute("SELECT COUNT(*) FROM produtos").fetchone()[0] == 0:
        c.executemany(
            "INSERT INTO produtos (nome, departamento, data_fabri, data_venci) VALUES (?, ?, ?, ?)", 
            [
                ("sabonete", "higiene", "2026-08-01", "2028-08-01"),
                ("agua", "bebidas", "2026-08-10", "2027-08-10"),
                ("coca-cola", "bebidas", "2026-08-15", "2027-02-15")
            ]
        )
        conn.commit()
    conn.close()

init_db()

@app.get("/")
def home():
    return {"mensagem": "API de Estoque está Rodando"}

@app.get("/produtos")
def listar_produtos():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM PRODUTOS")
    produtos = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return {"estoque": produtos}

@app.get("/produtos/{produto_id}")
def pegar_produto(produto_id: int):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM produtos WHERE id = ?", (produto_id,))
    produto = cursor.fetchone()
    conn.close()

    if produto:
        return dict(produto)
    return {"erro": "Produto não encontrado"}