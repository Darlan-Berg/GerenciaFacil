from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)

caminho_dados = "dados.json"

def ler_dados():
    with open(caminho_dados, "r") as dados:
        informacoes_usuarios = json.load(dados)
        return informacoes_usuarios

def adicionar_usuario(nome, cpf, email, senha):
    novo_usuario = {
        "nome": nome,
        "cpf": cpf,
        "email": email,
        "senha": senha
    }
    novos_dados = ler_dados()
    novos_dados.append(novo_usuario)

    with open(caminho_dados, "w") as dados:
        json.dump(novos_dados, dados, indent=4)

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
                return "<h1>Senha ou Usuário incorretos</h1>"
    return render_template("tela_login.html")

@app.route('/cadastro', methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"]
        cpf = request.form["cpf"]
        email = request.form["email"]
        senha = request.form["senha"]
        dados = ler_dados()
        for usuario in dados:
            if usuario["email"] == email:
                return "<h1>Usuário já cadastrado</h1>"
        if nome and cpf and email and dados:
            adicionar_usuario(nome, cpf, email, senha)
            return redirect(url_for("relatorios"))
        else:
            return "<h1>Por favor preencha todos os campos</h1>"
    return render_template("tela_cadastro.html")
