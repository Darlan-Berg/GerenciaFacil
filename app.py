from flask import Flask, render_template

app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/estoque")
def estoque():
    return render_template("estoque.html")

@app.route("/relatorios")
def estoque():
    return render_template("relatorios.html")

@app.route("/cadastrovendas")
def estoque():
    return render_template("cadastro_vendas.html")
