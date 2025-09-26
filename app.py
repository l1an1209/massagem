from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime, timedelta
import re

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'  # Em produção, use uma chave segura

# Lista de agendamentos (em produção usaria banco de dados)
agendamentos = []

def validar_telefone(telefone):
    """Valida formato de telefone brasileiro"""
    telefone_limpo = re.sub(r'\D', '', telefone)
    return len(telefone_limpo) >= 10 and len(telefone_limpo) <= 11

def validar_data(data):
    """Valida se a data não é no passado"""
    try:
        data_agendamento = datetime.strptime(data, '%Y-%m-%d').date()
        return data_agendamento >= datetime.now().date()
    except:
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/servicos')
def servicos():
    lista_servicos = [
        {"nome": "Cabine Exótica", "descricao": "Ambiente reservado e relaxante.", "preco": "R$ 150/hora"},
        {"nome": "Massagem Tântrica", "descricao": "Experiência sensorial e terapêutica.", "preco": "R$ 200/hora"},
        {"nome": "Massagem Relaxante", "descricao": "Massagem clássica para alívio de tensões.", "preco": "R$ 120/hora"},
        {"nome": "Tratamento Facial", "descricao": "Tratamento facial completo com produtos naturais.", "preco": "R$ 100/hora"}
    ]
    return render_template('servicos.html', servicos=lista_servicos)

@app.route('/agendamento', methods=["GET", "POST"])
def agendamento():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        telefone = request.form.get("telefone", "").strip()
        email = request.form.get("email", "").strip()
        servico = request.form.get("servico", "").strip()
        data = request.form.get("data", "").strip()
        horario = request.form.get("horario", "").strip()
        observacoes = request.form.get("observacoes", "").strip()
        
        # Validações
        erros = []
        
        if not nome or len(nome) < 2:
            erros.append("Nome deve ter pelo menos 2 caracteres")
        
        if not telefone or not validar_telefone(telefone):
            erros.append("Telefone deve ter formato válido (ex: (69) 99999-9999)")
        
        if email and not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            erros.append("E-mail deve ter formato válido")
        
        if not servico:
            erros.append("Selecione um serviço")
        
        if not data or not validar_data(data):
            erros.append("Data deve ser válida e não pode ser no passado")
        
        if not horario:
            erros.append("Selecione um horário")
        
        if erros:
            flash("Por favor, corrija os seguintes erros:", "error")
            for erro in erros:
                flash(erro, "error")
        else:
            # Criar agendamento
            agendamento = {
                "id": len(agendamentos) + 1,
                "nome": nome,
                "telefone": telefone,
                "email": email,
                "servico": servico,
                "data": data,
                "horario": horario,
                "observacoes": observacoes,
                "status": "pendente",
                "data_criacao": datetime.now().strftime("%d/%m/%Y %H:%M")
            }
            
            agendamentos.append(agendamento)
            flash(f"Agendamento realizado com sucesso! Seu número de protocolo é #{agendamento['id']}", "success")
            
            # Em produção, aqui você enviaria um e-mail de confirmação
            # e salvaria no banco de dados
    
    return render_template('agendamento.html')

@app.route('/contato', methods=["GET", "POST"])
def contato():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip()
        telefone = request.form.get("telefone", "").strip()
        assunto = request.form.get("assunto", "").strip()
        mensagem = request.form.get("mensagem", "").strip()
        
        # Validações básicas
        if not nome or not email or not mensagem:
            flash("Por favor, preencha todos os campos obrigatórios", "error")
        else:
            # Em produção, aqui você processaria o formulário de contato
            flash("Mensagem enviada com sucesso! Entraremos em contato em breve.", "success")
    
    return render_template('contato.html')

@app.route('/api/agendamentos')
def api_agendamentos():
    """API para listar agendamentos (para administração)"""
    return jsonify(agendamentos)

@app.route('/api/agendamento/<int:agendamento_id>')
def api_agendamento(agendamento_id):
    """API para buscar agendamento específico"""
    agendamento = next((a for a in agendamentos if a['id'] == agendamento_id), None)
    if agendamento:
        return jsonify(agendamento)
    return jsonify({"erro": "Agendamento não encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True)
