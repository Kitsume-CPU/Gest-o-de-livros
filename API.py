from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

API = Flask(__name__)

# Environment variable approach (recommended)

# Direct configuration (optional)
API.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:suasenha@seuhost:porta/nomedobanco'

db = SQLAlchemy(API)

class Livro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    genero = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Livro %r>' % self.nome

    def json(self):
        return {'id': self.id, 'nome': self.nome, 'autor': self.autor, 'genero': self.genero}


@API.route('/livro', methods=['GET'])
def get_livros():
    livros = Livro.query.all() 
    return jsonify([livro.json() for livro in livros])

@API.route('/livro/<int:id>', methods=['GET'])
def get_livro(id):
    livro = Livro.query.get_or_404(id)
    return jsonify(livro.json())

@API.route('/livro', methods=['POST'])
def incluir_novo_livro():
    novo_livro = request.get_json()
    livro = Livro(nome=novo_livro['nome'], autor=novo_livro['autor'], genero=novo_livro['genero'])
    db.session.add(livro)
    db.session.commit()
    return jsonify(livro.json()), 201

@API.route('/livro/<int:id>', methods=['PUT'])
def editar_livro(id):
    livro = Livro.query.get_or_404(id)
    livro.nome = request.json['nome']
    livro.autor = request.json['autor']
    livro.genero = request.json['genero']
    db.session.commit()
    return jsonify(livro.json())

@API.route('/livro/<int:id>', methods=['DELETE'])
def deletar_livro(id):
    livro = Livro.query.get_or_404(id)
    db.session.delete(livro)
    db.session.commit()
    livros = Livro.query.all() 
    return jsonify([livro.json() for livro in livros])

if __name__ == '__main__':
    API.run(debug=True)