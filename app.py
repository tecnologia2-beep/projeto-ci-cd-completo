import os
from typing import Tuple

import mysql.connector
from flask import Flask, jsonify, request


DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "12345678")
DB_NAME = os.getenv("DB_NAME", "db_produtos")

app = Flask(__name__)


def conectar():
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
    )


def validar_parametros(grupo: str, tipo_alimento: str, pais: str) -> None:
    if not grupo or not tipo_alimento or not pais:
        raise ValueError("Parâmetros inválidos")

    if len(pais) != 2:
        raise ValueError("Pais deve ter 2 caracteres")

    if len(grupo) != 1 or len(tipo_alimento) != 1:
        raise ValueError("Grupo e Tipo_Alimento devem ter 1 caractere")


def gerar_codigo(grupo: str, tipo_alimento: str, pais: str) -> Tuple[str, int]:
    validar_parametros(grupo, tipo_alimento, pais)

    grupo = grupo.upper()
    tipo_alimento = tipo_alimento.upper()
    pais = pais.upper()

    conn = conectar()
    cursor = conn.cursor()

    query = "SELECT MAX(sec) FROM produtos WHERE Grupo = %s"
    cursor.execute(query, (grupo,))
    resultado = cursor.fetchone()

    sec = 1 if resultado[0] is None else resultado[0] + 1
    sequencia = str(sec).zfill(4)
    codigo = f"{pais}{grupo}{sequencia}{tipo_alimento}"

    cursor.close()
    conn.close()

    return codigo, sec


def inserir_produto(grupo: str, tipo_alimento: str, pais: str) -> dict:
    codigo, sec = gerar_codigo(grupo, tipo_alimento, pais)

    conn = conectar()
    cursor = conn.cursor()

    sql = """
    INSERT INTO produtos (codigo, sec, Grupo, Tipo_Alimento, Pais)
    VALUES (%s,%s,%s,%s,%s)
    """

    cursor.execute(sql, (codigo, sec, grupo.upper(), tipo_alimento.upper(), pais.upper()))
    conn.commit()

    cursor.close()
    conn.close()

    return {
        "codigo": codigo,
        "sec": sec,
        "grupo": grupo.upper(),
        "tipo_alimento": tipo_alimento.upper(),
        "pais": pais.upper(),
    }


@app.get("/health")
def healthcheck():
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        cursor.close()
        conn.close()
        return jsonify({"status": "ok"}), 200
    except mysql.connector.Error as exc:
        return jsonify({"status": "erro", "detalhe": str(exc)}), 500


@app.post("/produtos")
def criar_produto():
    payload = request.get_json(silent=True) or {}

    try:
        produto = inserir_produto(
            grupo=str(payload.get("grupo", "")),
            tipo_alimento=str(payload.get("tipo_alimento", "")),
            pais=str(payload.get("pais", "")),
        )
        return jsonify(produto), 201
    except ValueError as exc:
        return jsonify({"erro": str(exc)}), 400
    except mysql.connector.Error as exc:
        return jsonify({"erro": str(exc)}), 500


@app.get("/")
def index():
    return jsonify(
        {
            "projeto": "CI/CD - Geração de Código Sequencial",
            "endpoints": {
                "health": "/health",
                "criar_produto": "POST /produtos",
            },
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
