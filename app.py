from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)

caminho_dados = 'dados.json'

def ler_dados():
    with open(caminho_dados, 'r') as dados:
        informacoes_usuarios = json.load(dados)
        return informacoes_usuarios

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/estoque")
def estoque():
    return render_template("estoque.html")

@app.route("/relatorios")
def relatorios():
    return render_template("relatorios.html")

@app.route("/cadastrovendas")
def cadastro_vendas():
    return render_template("cadastro_vendas.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]
        dados = ler_dados()
        for usuario in dados:
            if usuario["email"] == email and usuario["senha"] == senha:
                return redirect(url_for("relatorios"))
            else:
                return ""
    return render_template("tela_login.html")

