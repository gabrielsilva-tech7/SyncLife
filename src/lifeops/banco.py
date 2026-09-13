import os
import sqlite3
import psycopg


DATABASE_URL = os.getenv("DATABASE_URL")


def usando_postgres():
    return DATABASE_URL is not None


def conectar():
    if usando_postgres():
        return psycopg.connect(DATABASE_URL)

    return sqlite3.connect("lifeops.db")


def executar(cursor, sql_sqlite, parametros=(), sql_postgres=None):
    if usando_postgres():
        cursor.execute(
            sql_postgres if sql_postgres else sql_sqlite.replace("?", "%s"),
            parametros
        )
    else:
        cursor.execute(sql_sqlite, parametros)


def criar_tabelas():
    conexao = conectar()
    cursor = conexao.cursor()

    if usando_postgres():
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tarefas (
                id SERIAL PRIMARY KEY,
                descricao TEXT NOT NULL,
                concluida INTEGER NOT NULL DEFAULT 0
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS compromissos (
                id SERIAL PRIMARY KEY,
                descricao TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS gastos (
                id SERIAL PRIMARY KEY,
                nome TEXT NOT NULL,
                valor REAL NOT NULL
            )
        """)

    else:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tarefas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descricao TEXT NOT NULL,
                concluida INTEGER NOT NULL DEFAULT 0
            )
        """)

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


# =========================
# TAREFAS
# =========================

def adicionar_tarefa(descricao):
    conexao = conectar()
    cursor = conexao.cursor()

    executar(
        cursor,
        "INSERT INTO tarefas (descricao) VALUES (?)",
        (descricao,)
    )

    conexao.commit()
    conexao.close()


def listar_tarefas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM tarefas ORDER BY id")

    tarefas = cursor.fetchall()

    conexao.close()

    return tarefas


def concluir_tarefa(id_tarefa):
    conexao = conectar()
    cursor = conexao.cursor()

    executar(
        cursor,
        "UPDATE tarefas SET concluida = 1 WHERE id = ?",
        (id_tarefa,)
    )

    encontrou = cursor.rowcount

    conexao.commit()
    conexao.close()

    return encontrou > 0


def excluir_tarefa(id_tarefa):
    conexao = conectar()
    cursor = conexao.cursor()

    executar(
        cursor,
        "DELETE FROM tarefas WHERE id = ?",
        (id_tarefa,)
    )

    encontrou = cursor.rowcount

    conexao.commit()
    conexao.close()

    return encontrou > 0


# =========================
# COMPROMISSOS
# =========================

def adicionar_compromisso(descricao):
    conexao = conectar()
    cursor = conexao.cursor()

    executar(
        cursor,
        "INSERT INTO compromissos (descricao) VALUES (?)",
        (descricao,)
    )

    conexao.commit()
    conexao.close()


def listar_compromissos():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT * FROM compromissos ORDER BY id"
    )

    compromissos = cursor.fetchall()

    conexao.close()

    return compromissos


def excluir_compromisso(id_compromisso):
    conexao = conectar()
    cursor = conexao.cursor()

    executar(
        cursor,
        "DELETE FROM compromissos WHERE id = ?",
        (id_compromisso,)
    )

    encontrou = cursor.rowcount

    conexao.commit()
    conexao.close()

    return encontrou > 0


# =========================
# GASTOS
# =========================

def adicionar_gasto(nome, valor):
    conexao = conectar()
    cursor = conexao.cursor()

    executar(
        cursor,
        "INSERT INTO gastos (nome, valor) VALUES (?, ?)",
        (nome, valor)
    )

    conexao.commit()
    conexao.close()


def listar_gastos():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM gastos ORDER BY id")

    gastos = cursor.fetchall()

    conexao.close()

    return gastos


def excluir_gasto(id_gasto):
    conexao = conectar()
    cursor = conexao.cursor()

    executar(
        cursor,
        "DELETE FROM gastos WHERE id = ?",
        (id_gasto,)
    )

    encontrou = cursor.rowcount

    conexao.commit()
    conexao.close()

    return encontrou > 0