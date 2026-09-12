from fastapi import FastAPI

app = FastAPI()

vendas = {
    1: {"item": "lata", "preco_unitario": 4, "quantidade": 5},
    2: {"item": "garrafa 2L", "preco_unitario": 4, "quantidade": 5},
    3: {"item": "leite", "preco_unitario": 4, "quantidade": 5},
    4: {"item": "chcocolate", "preco_unitario": 4, "quantidade": 5}
}

@app.get("/")
def home():
    return {"Vendas": len(vendas)}

@app.get("/vendas/{id_venda}")
def pegar_venda(id_venda: int):
    return vendas[id_venda]