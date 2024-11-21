from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tarefas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Tarefa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    concluida = db.Column(db.Boolean, default=False)
    categoria = db.Column(db.String(50), nullable=True, default="Pessoal")

@app.route('/', methods=["GET"])
def index():
    filtro_categoria = request.args.get("filtro_categoria", "")
    if filtro_categoria:
        tarefas = Tarefa.query.filter_by(categoria=filtro_categoria).order_by(Tarefa.id.desc()).all()
    else:
        tarefas = Tarefa.query.order_by(Tarefa.id.desc()).all()
    return render_template('index.html', tarefas=tarefas, categoria_atual=filtro_categoria)

@app.route('/adicionar', methods=['POST'])
def adicionar_tarefa():
    nome_tarefa = request.form.get('tarefa', '').strip()
    if not nome_tarefa:
        return jsonify({'status': 'error', 'message': 'Nome da tarefa não pode estar vazio'}), 400
    
    categoria = request.form.get('categoria', 'Pessoal')
    nova_tarefa = Tarefa(nome=nome_tarefa, categoria=categoria)
    
    try:
        db.session.add(nova_tarefa)
        db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': 'Erro ao adicionar tarefa'}), 500

@app.route('/concluir/<int:tarefa_id>', methods=['POST'])
def concluir_tarefa(tarefa_id):
    try:
        tarefa = Tarefa.query.get_or_404(tarefa_id)
        tarefa.concluida = not tarefa.concluida  # Toggle do status
        db.session.commit()
        return jsonify({'status': 'success', 'concluida': tarefa.concluida})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': 'Erro ao atualizar tarefa'}), 500

@app.route('/remover/<int:tarefa_id>', methods=['POST'])
def remover_tarefa(tarefa_id):
    try:
        tarefa = Tarefa.query.get_or_404(tarefa_id)
        db.session.delete(tarefa)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Tarefa removida com sucesso!'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': 'Erro ao remover tarefa'}), 500

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)