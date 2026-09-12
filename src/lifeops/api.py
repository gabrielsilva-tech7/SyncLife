from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from pydantic import BaseModel
from lifeops.banco import (
    listar_tarefas,
    adicionar_tarefa,
    excluir_tarefa,
    concluir_tarefa,
    listar_compromissos,
    adicionar_compromisso,
    excluir_compromisso,
    listar_gastos,
    adicionar_gasto,
    excluir_gasto,
    criar_tabelas
)
app = FastAPI()
criar_tabelas()

class Tarefa(BaseModel):
    descricao: str


@app.get("/tarefas")
def obter_tarefas():
    tarefas = listar_tarefas()

    resultado = []

    for tarefa in tarefas:
        resultado.append({
            "id": tarefa[0],
            "descricao": tarefa[1],
            "concluido": bool(tarefa[2])
        })

    return resultado

@app.post("/tarefas")
def criar_tarefa(tarefa: Tarefa):
    adicionar_tarefa(tarefa.descricao)

    return {
        "mensagem": "Tarefa cadastrada com sucesso!"
    }


@app.delete("/tarefas/{id_tarefa}")
def deletar_tarefa(id_tarefa: int):
    if excluir_tarefa(id_tarefa):
        return {"mensagem": "Tarefa excluída com sucesso!"}

    return {"mensagem": "Tarefa não encontrada!"}

@app.patch("/tarefas/{id_tarefa}/concluir")
def marcar_tarefa_concluida(id_tarefa: int):
    if concluir_tarefa(id_tarefa):
        return{"mensagem": "Tarefa concluida!"}

    return {"mensagem": "Tarefa não encontrada!"}

class Compromisso(BaseModel):
    descricao: str


@app.get("/compromissos")
def obter_compromissos():
    compromissos = listar_compromissos()

    resultado = []

    for compromisso in compromissos:
        resultado.append({
            "id": compromisso[0],
            "descricao": compromisso[1]
        })

    return resultado


@app.post("/compromissos")
def criar_compromisso(compromisso: Compromisso):
    adicionar_compromisso(compromisso.descricao)

    return {"mensagem": "Compromisso cadastrado com sucesso!"}


@app.delete("/compromissos/{id_compromisso}")
def deletar_compromisso(id_compromisso: int):
    if excluir_compromisso(id_compromisso):
        return {"mensagem": "Compromisso excluído com sucesso!"}

    return {"mensagem": "Compromisso não encontrado!"}

class Gasto(BaseModel):
    nome: str
    valor: float


@app.get("/gastos")
def obter_gastos():
    gastos = listar_gastos()

    resultado = []

    for gasto in gastos:
        resultado.append({
            "id": gasto[0],
            "nome": gasto[1],
            "valor": gasto[2]
        })

    return resultado


@app.post("/gastos")
def criar_gasto(gasto: Gasto):
    adicionar_gasto(gasto.nome, gasto.valor)

    return {"mensagem": "Gasto cadastrado com sucesso!"}


@app.delete("/gastos/{id_gasto}")
def deletar_gasto(id_gasto: int):
    if excluir_gasto(id_gasto):
        return {"mensagem": "Gasto excluído com sucesso!"}

    return {"mensagem": "Gasto não encontrado!"}

@app.get("/resumo")
def obter_resumo():
    tarefas = listar_tarefas()
    compromissos = listar_compromissos()
    gastos = listar_gastos()

    pendentes = 0
    concluidas = 0

    for tarefa in tarefas:
        if tarefa[2] == 1:
            concluidas += 1
        else:
            pendentes += 1

    total_gastos = 0

    for gasto in gastos:
        total_gastos += gasto[2]

    return {
        "tarefas_pendentes": pendentes,
        "tarefas_concluidas": concluidas,
        "compromissos": len(compromissos),
        "total_gastos": total_gastos
    }

app.mount(
    "/",
    StaticFiles(directory="src/lifeops/static", html=True),
    name="static"
)