from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import getpass

# Configuração do Banco de Dados
user = 'postgres'
password = getpass.getpass('Digite a senha do banco de dados: ')
host = 'localhost'
database = 'tarefas'
# Conexão com o Banco de Dados
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{host}/{database}'
db = SQLAlchemy(app)


# Criação de classe Tarefa como modelo para mapear a tabela tarefas do BD
class Tarefa(db.Model):
    __tablename__ = 'tarefas'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255), nullable=True)
    status = db.Column(db.Boolean, default=False)
    data_criacao = db.Column(db.DateTime, default=db.func.current_timestamp())


# Método HTTP utilizando GET -> Responsável por exibir todas as tarefas pendentes
@app.route('/tarefas', methods=['GET'])
def get_tarefas():
    tarefas = Tarefa.query.all()
    return jsonify([{'id': t.id,
                     'titulo': t.titulo,
                     'descricao': t.descricao,
                     'status': t.status,
                     'data_criacao': t.data_criacao.strftime('%Y-%m-%d %H:%M:%S')} for t in tarefas])


# Método HTTP utilizando POST com Stored Procedure ⇾ Responsável por adicionar uma nova tarefa
@app.route('/tarefas', methods=['POST'])
def add_tarefa():
    data = request.json
    titulo = data.get('titulo')
    descricao = data.get('descricao', '')
    db.session.execute(text('CALL adicionar_tarefa(:titulo, :descricao)'),
                       {'titulo': titulo, 'descricao': descricao})
    db.session.commit()
    return jsonify({'message': 'Tarefa criada com sucesso!'}), 201


# Método HTTP utilizando PUT ⇾ Responsável por atualizar o título de uma tarefa e também alterar o seu status.
# Aqui existe um ‘Trigger’ que, assim que uma tarefa atualiza o status para TRUE (concluída), ele remove da tabela
# Tarefas e move para tabela tarefas_concluidas_log.
@app.route('/tarefas/<int:id>', methods=['PUT'])
def update_tarefa(id):
    tarefa = Tarefa.query.get(id)
    if tarefa:
        data = request.json
        tarefa.titulo = data.get('titulo', tarefa.titulo)
        tarefa.status = data.get('status', tarefa.status)
        db.session.commit()
        return jsonify({'message': 'Tarefa atualizada!'})
    return jsonify({'message': 'Tarefa não encontrada.'}), 404


# Método HTTP utilizando DELETE ⇾ Responsável por deletar uma tarefa
@app.route('/tarefas/<int:id>', methods=['DELETE'])
def delete_tarefa(id):
    tarefa = Tarefa.query.get(id)
    if tarefa:
        db.session.delete(tarefa)
        db.session.commit()
        return jsonify({'message': 'Tarefa deletada com sucesso.'})
    return jsonify({'message': 'Tarefa não encontrada.'}), 404


# Método HTTP utilizando GET com VIEW ⇾ Responsável por visualizar as tarefas já concluidas
@app.route('/tarefas/concluidas', methods=['GET'])
def get_tarefas_concluidas():
    tarefas_concluidas = db.session.execute(text('SELECT * FROM view_tarefas_concluidas')).fetchall()
    resultado = [
        {
            'id': tarefa[0],
            'titulo': tarefa[1],
            'descricao': tarefa[2],
            'data_criacao': tarefa[3].strftime('%Y-%m-%d %H:%M:%S'),
            'data_movimentacao': tarefa[4].strftime('%Y-%m-%d %H:%M:%S')
        }
        for tarefa in tarefas_concluidas
    ]
    return jsonify(resultado)


# Método HTTP utilizando GET com Função Simples ⇾ Conta quantas tarefas pendentes ainda existem
@app.route('/tarefas/contar', methods=['GET'])
def contar_tarefas():
    result = db.session.execute(text('SELECT contar_tarefas()')).scalar()
    return jsonify({'total de tarefas pendentes': result})


# Método HTTP utilizando GET com Função PL/pgSQL ⇾ Responsável por mostrar as tarefas que foram criadas há 7 dias.
@app.route('/tarefas/atrasadas', methods=['GET'])
def listar_tarefas_atrasadas():
    tarefas_atrasadas = db.session.execute(text('SELECT * FROM contar_tarefas_atrasadas()')).fetchall()
    resultado = [
        {
            'id': tarefa[0],
            'titulo': tarefa[1],
            'descricao': tarefa[2],
            'data_criacao': tarefa[3].strftime('%Y-%m-%d %H:%M:%S')
        }
        for tarefa in tarefas_atrasadas
    ]
    return jsonify(resultado)


if __name__ == '__main__':
    app.run(debug=True)
