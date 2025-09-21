from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Lista de agendamentos (em produção usaria banco de dados)
agendamentos = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/servicos')
def servicos():
    lista_servicos = [
        {"nome": "Cabine Secreta", "descricao": "Ambiente reservado e relaxante."},
        {"nome": "Massagem Tântrica", "descricao": "Experiência sensorial e terapêutica."}
    ]
    return render_template('servicos.html', servicos=lista_servicos)

@app.route('/agendamento', methods=["GET", "POST"])
def agendamento():
    if request.method == "POST":
        nome = request.form["nome"]
        telefone = request.form["telefone"]
        servico = request.form["servico"]
        agendamentos.append({"nome": nome, "telefone": telefone, "servico": servico})
        return "Agendamento enviado com sucesso!"
    return render_template('agendamento.html')

@app.route('/contato')
def contato():
    return render_template('contato.html')

if __name__ == '__main__':
    app.run(debug=True)
