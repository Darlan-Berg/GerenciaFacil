from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)

caminho_historico_compras = os.path.join(os.path.dirname(os.path.abspath(__file__)), "historico_compras.json")

@app.route("/")
@app.route("/dashboard")
def main():
    return render_template("dashboard.html")

@app.route("/estoque")
def estoque():
    return render_template("estoque.html")

@app.route("/cadastro-vendas")
def cadastro_vendas():
    return render_template("cadastro_vendas.html")

@app.route("/cadastro-compras", methods=["GET", "POST"])
def cadastro_compras():
    if request.method == "GET":
        with open(caminho_historico_compras, "r", encoding="utf-8") as arq_json:
            historico_compras = json.load(arq_json)
        return render_template("compras.html", lista_produtos=historico_compras)

    nome = request.form.get("nome_produto")
    marca = request.form.get("marca")
    valor = request.form.get("valor")
    preco = request.form.get("preco")
    quantidade = request.form.get("quantidade")
    data_compra = request.form.get("data-compra")
    data_validade = request.form.get("data-validade")

    # ler arquivo estoque.json
    with open(caminho_historico_compras, "r", encoding="utf-8") as arq_json:
        estoque = json.load(arq_json)

    # sobrescrever estoque.json
    with open(caminho_historico_compras, "w", encoding="utf-8") as arq_json:
        novo_produto = {
            "nome": nome,
            "marca": marca,
            "valor": valor,
            "preco": preco,
            "quantidade": quantidade,
            "data_compra": data_compra,
            "data_validade": data_validade
        }
        estoque_atualizado = estoque
        estoque_atualizado.append(novo_produto)

        # sobrescrever estoque.json com as informacoes atuais
        json.dump(estoque_atualizado, arq_json, indent=4)

        return redirect(url_for("cadastro_compras"))

@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")

@app.route('/cadastro', methods=["GET", "POST"])
def cadastro():
    return render_template("cadastro_usuarios.html")

@app.route("/recuperar-senha")
def recuperar_senha():
    return render_template("recuperar_senha.html")
