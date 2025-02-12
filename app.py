from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import json
import os
import mysql.connector

app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)

caminho_historico_compras = os.path.join(os.path.dirname(os.path.abspath(__file__)), "historico_compras.json")

# carregar o historico de compras
def carregar_historico_compras():
    try:
        with open('historico_compras.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# salvar o historico de compras
def salvar_historico_compras(historico):
    with open('historico_compras.json', 'w') as f:
        json.dump(historico, f, indent=4)

def carregar_estoque():
    try:
        with open("estoque.json", "r") as estoque:
            return json.load(estoque)
    except FileNotFoundError:
        return []

def salvar_estoque(estoque):
    with open('estoque.json', 'w') as antigo_etoque:
        json.dump(estoque, antigo_etoque, indent=4)
palavra = "asdfghjklç"
try:
    conexao = mysql.connector.connect(
        host = "Dharllan.mysql.pythonanywhere-services.com",
        user = "Dharllan",
        password = "mysqlroot",
        database = "Dharllan$default"
    )
    msg = "CONEXÃO ESTABELECIDA COM A BASE DE DADOS"
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM Produtos;")
    estoque_produtos = cursor.fetchall()
except:
    msg = "ERRO DE CONEXÃO COM A BASE DE DADOS"
    estoque = ["O banco de dados está vazio ou a conexão falhou"]

def adicionar_produto(id, nome, marca, data_validade, estoque, valor_compra, valor_venda):
    'query = f"INSERT INTO Produtos (id, nome, marca, data_validade, estoque, valor_compra, valor_venda) VALUES ({id}, {nome}, {marca}, {data_validade}, {estoque}, {valor_compra}, {valor_venda});"'
    'values = (id, nome, marca, data_validade, estoque, valor_compra, valor_venda)'
    'cursor.execute(query, values)'
    cursor.execute("INSERT INTO Produtos (id, nome, marca, data_validade, estoque, valor_compra, valor_venda) VALUES (%s, %s, %s, %s, %s, %s, %s)", (str(id), str(nome), str(marca), str(data_validade), str(estoque), str(valor_compra), str(valor_venda)))
    conexao.commit()

@app.route("/")
@app.route("/dashboard")
def main():
    if 'username' in session:
        return render_template("dashboard.html", username=session['username'])
    else:
        return render_template("dashboard.html")

@app.route("/estoque")
def estoque():
    return render_template("estoque.html", msg=msg, estoque_produtos=estoque_produtos)

@app.route("/cadastro-vendas")
def cadastro_vendas():
    return render_template("cadastro_vendas.html")

@app.route('/confirmar-compra', methods=['POST'])
def confirmar_compra():
    # recebe o JSON enviado pelo javascript
    nova_compra = request.get_json()

    # acessando os dados dos produtos enviados pelo formulário
    id = nova_compra['cod']
    nome = request.form.get('nome')
    marca = request.form.get('marca')
    data_validade = request.form.get('data_validade')
    estoque = request.form.get('quantidade')
    valor_venda = request.form.get('valor_venda')
    valor_compra = request.form.get('valor_compra')

    #Enviar informaçoes da nova compra para o banco de dados
    adicionar_produto(id, nome, marca, data_validade, estoque, valor_compra, valor_venda)

    estoque = carregar_estoque()


    for produto_compra in nova_compra["produtos"]:

        produto_existente = False
        indice = 0

        for produto_estoque in estoque:
            if produto_compra["nome"] == produto_estoque["nome"] and produto_compra["marca"] == produto_estoque["marca"]:

                produto_para_ser_adicionado = estoque[indice]
                produto_para_ser_adicionado["qtd"] += produto_compra["quantidade"]
                produto_existente = True
                break

            indice += 1

        if not produto_existente:
            estoque.append({
                "nome": produto_compra["nome"],
                "marca": produto_compra["marca"],
                "valor": produto_compra["valor"],
                "qtd": produto_compra["quantidade"],
                "data_validade": produto_compra["data_validade"]
            })

    salvar_estoque(estoque)

    print(nova_compra)

    # carrega o historico atual de compras
    historico = carregar_historico_compras()

    # adiciona a nova compra ao historico
    historico.append(nova_compra)

    # salva o historico atualizado no arquivo
    salvar_historico_compras(historico)
    return redirect(url_for("cadastro_compras"))



@app.route("/cadastro-compras", methods=["GET", "POST"])
def cadastro_compras():
    if request.method == "GET":
        with open(caminho_historico_compras, "r", encoding="utf-8") as arq_json:
            historico_compras = json.load(arq_json)
        return render_template("compras.html", lista_compras=historico_compras)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            username = request.form['email']
            pwd = request.form['senha']
            cursor = conexao.cursor()
            cursor.execute("SELECT Email, Senha FROM Usuarios WHERE Email = %s", (username,))
            user = cursor.fetchone()
            cursor.close()
            if user[0] == username and user[1] == pwd:

                return render_template('dashboard.html', username = username)
        except:
            return render_template('login.html')
    return render_template('login.html')

@app.route('/cadastro', methods=["GET", "POST"])
def cadastro():
    if request.method == 'POST':
        try:
            nome = request.form['nome']
            email = request.form['email']
            pwd = request.form['senha']
            cursor = conexao.cursor()
            cursor.execute("INSERT INTO Usuarios(Nome, Email, Senha) VALUES(%s, %s, %s)", (str(nome), str(email), str(pwd),))
            conexao.commit()
            cursor.close()
            return redirect(url_for('login'))
        except:
            return redirect(url_for('estoque'))

    return render_template("cadastro_usuarios.html")

@app.route("/recuperar-senha")
def recuperar_senha():
    return render_template("recuperar_senha.html")

@app.route('/excluir-compra', methods=['POST'])
def excluir_compra():
    compra_id = request.json.get('id')

    # Carrega os dados do JSON
    with open('./historico_compras.json') as f:
        compras = json.load(f)

    # Filtra as compras para excluir a que tem o ID especificado
    compras = [compra for compra in compras if compra['cod'] != compra_id]

    # Salva de volta no arquivo JSON
    with open('./historico_compras.json', 'w') as f:
        json.dump(compras, f)

    return jsonify({'message': 'Compra excluída com sucesso!'})