import sqlite3

def conectar():
    conexao = sqlite3.connect("lifeops.db")
    return conexao

def criar_tabelas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS tarefas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descricao TEXT NOT NULL,
        concluida INTEGER NOT NULL DEFAULT 0
        )"""
    )

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS compromissos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descricao TEXT NOT NULL
        )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS gastos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        valor REAL NOT NULL
        )
    """)

    conexao.commit()
    conexao.close()

def adicionar_tarefa(descricao):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "INSERT INTO tarefas (descricao) VALUES (?)",
        (descricao,)
    )

    conexao.commit()
    conexao.close()


def listar_tarefas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM tarefas")
    tarefas = cursor.fetchall()

    conexao.close()
    return tarefas


def concluir_tarefa(id_tarefa):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "UPDATE tarefas SET concluida = 1 WHERE id = ?",
        (id_tarefa,)
    )

    conexao.commit()
    conexao.close()


def excluir_tarefa(id_tarefa):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "DELETE FROM tarefas WHERE id = ?",
        (id_tarefa,)
    )

    encontrou = cursor.rowcount

    conexao.commit()
    conexao.close()

    return encontrou > 0


def adicionar_compromisso(descricao):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "INSERT INTO compromissos (descricao) VALUES (?)",
        (descricao,)
    )

    conexao.commit()
    conexao.close()


def listar_compromissos():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM compromissos")
    compromissos = cursor.fetchall()

    conexao.close()
    return compromissos


def excluir_compromisso(id_compromisso):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "DELETE FROM compromissos WHERE id = ?",
        (id_compromisso,)
    )

    encontrou = cursor.rowcount

    conexao.commit()
    conexao.close()

    return encontrou > 0


def adicionar_gasto(nome, valor):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "INSERT INTO gastos (nome, valor) VALUES (?, ?)",
        (nome, valor)
    )

    conexao.commit()
    conexao.close()


def listar_gastos():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM gastos")
    gastos = cursor.fetchall()

    conexao.close()
    return gastos


def excluir_gasto(id_gasto):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "DELETE FROM gastos WHERE id = ?",
        (id_gasto,)
    )
    encontrou = cursor.rowcount

    conexao.commit()
    conexao.close()

    return encontrou > 0