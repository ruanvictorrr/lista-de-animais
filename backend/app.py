from flask import Flask, request, jsonify, redirect
import sqlite3

app = Flask(__name__, static_folder="../frontend", static_url_path="")

def get_conn():
    return sqlite3.connect("animais.db")

conn = get_conn()
conn.execute("CREATE TABLE IF NOT EXISTS animais (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, especie TEXT, idade INTEGER)")
conn.commit()
conn.close()

@app.route("/")
def home():
    return redirect("/index.html")

@app.route("/animais", methods=["POST"])
def criar():
    dados = request.json
    conn = get_conn()
    conn.execute("INSERT INTO animais (nome, especie, idade) VALUES (?, ?, ?)", (dados["nome"], dados["especie"], dados.get("idade")))
    conn.commit()
    conn.close()
    return jsonify({"ok": True})

@app.route("/animais", methods=["GET"])
def listar():
    conn = get_conn()
    linhas = conn.execute("SELECT * FROM animais").fetchall()
    conn.close()
    return jsonify([{"id": l[0], "nome": l[1], "especie": l[2], "idade": l[3]} for l in linhas])

@app.route("/animais/<int:id>", methods=["PUT"])
def atualizar(id):
    dados = request.json
    conn = get_conn()
    conn.execute("UPDATE animais SET nome=?, especie=?, idade=? WHERE id=?", (dados["nome"], dados["especie"], dados.get("idade"), id))
    conn.commit()
    conn.close()
    return jsonify({"ok": True})

@app.route("/animais/<int:id>", methods=["DELETE"])
def deletar(id):
    conn = get_conn()
    conn.execute("DELETE FROM animais WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(port=5000)