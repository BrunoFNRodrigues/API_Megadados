from tkinter import RADIOBUTTON
from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

class Produto(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

fake_db = {}

app = FastAPI()


@app.get("/produtos/{id_produto}")
async def read_produto(id_produto:str):
    return fake_db[id_produto]

@app.put("/produtos/{id_produto}")
async def edit_produto(id_produto:str, produto: Produto):
    fake_db[id_produto] = jsonable_encoder(produto)
    return produto

@app.get("/produtos/")
async def read_all_produtos():
    return fake_db

@app.post("/produtos/")
async def create_produto(produto: Produto):
    fake_db[produto.name] = (jsonable_encoder(produto))
    return produto

@app.delete("/produtos/{id_produto}")
async def remove_produto(id_produto:str):
    fake_db.pop(id_produto)
    return {"message": id_produto}