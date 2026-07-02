from flask import Flask, request, jsonify, redirect
import sqlite3

app = Flask(__name__, static_folder="../frontend", static_url_path="")

conn = sqlite3.connect("animais.db", check_same_thread=False)
conn.execute("CREATE TABLE IF NOT EXISTS animais (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, especie TEXT, idade INTEGER)")
conn.commit()

@app.route("/")
def home():
    return redirect("/index.html")

@app.route("/animais", methods=["GET"])
def listar():
    linhas = conn.execute("SELECT * FROM animais").fetchall()
    return jsonify([{"id": l[0], "nome": l[1], "especie": l[2], "idade": l[3]} for l in linhas])

@app.route("/animais", methods=["POST"])
def criar():
    dados = request.json
    conn.execute("INSERT INTO animais (nome, especie, idade) VALUES (?, ?, ?)", (dados["nome"], dados["especie"], dados.get("idade")))
    conn.commit()
    return jsonify({"ok": True})

@app.route("/animais/<int:id>", methods=["PUT"])
def atualizar(id):
    dados = request.json
    conn.execute("UPDATE animais SET nome=?, especie=?, idade=? WHERE id=?", (dados["nome"], dados["especie"], dados.get("idade"), id))
    conn.commit()
    return jsonify({"ok": True})

@app.route("/animais/<int:id>", methods=["DELETE"])
def deletar(id):
    conn.execute("DELETE FROM animais WHERE id=?", (id,))
    conn.commit()
    return jsonify({"ok": True})

if __name__ == "__main__":
    app.run(debug=True, port=5000)