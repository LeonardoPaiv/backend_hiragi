import json
from flask import Flask, request, jsonify, redirect
from model.dao import DAO
from flask_login import current_user, LoginManager, login_user, logout_user, login_required, UserMixin
import hashlib
import re

app = Flask(__name__)
app.secret_key = 'SubiNumPeDePeraPraArrancarUmaPera'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # type: ignore

class User(UserMixin):
   idt_pessoa = 0
   nme_pessoa = ''
   cpf_pessoa = ''
   email_pessoa = ''

   def to_json(self):
       return {
           "idt_guardiao": self.idt_pessoa,
           "nme_pessoa": self.nme_pessoa,
           "cpf_pessoa": self.cpf_pessoa,
           "email_guardiao": self.email_pessoa}

   def get_id(self):
       return str(self.idt_pessoa)

@login_manager.user_loader
def load_user(user_id):
   dao = DAO('tb_pessoa')
   lista = dao.readBy('idt_pessoa', '==', user_id)
   if len(lista) == 1:
       usr = User()
       usr.idt_pessoa = lista[0].idt_pessoa
       usr.nme_pessoa = str(lista[0].nme_pessoa)
       usr.cpf_pessoa = str(lista[0].cpf_pessoa)
       usr.email_pessoa = str(lista[0].email_guardiao)
       return usr
   else:
       return None


@app.route("/")
def index():
    if current_user.is_authenticated: # type: ignore
        return redirect("/api/v0/consultas")
    else:
        return redirect("/api/v0/login")

@app.route("/api/v0/login", methods=['GET'])
def login():
    email = request.args.get('email')
    senha = request.args.get('senha')

    dao = DAO("tb_pessoa")

    lista = dao.readBy("email_pessoa", "==", email)
    compilacao = hashlib.sha1(str(senha).encode("utf-8")).hexdigest()

    if len(lista) == 1 and lista[0].senha_pessoa == compilacao:
        usr = User()
        usr.idt_pessoa = lista[0].idt_pessoa
        usr.nme_pessoa = str(lista[0].nme_pessoa)
        usr.cpf_pessoa = str(lista[0].cpf_pessoa)
        usr.email_pessoa = str(lista[0].email_guardiao)
        login_user(usr, remember=True)

        if current_user.is_authenticated: # type: ignore
            return redirect("/api/v0/consultas")
        else:
            return jsonify("carlos")
    else:
        return jsonify("carlos")

@app.route("/api/v0/cadastrar", methods=['POST'])
def cadastrar():

    nome = request.form.get("nome")

    cpf = request.form.get("cpf")
    if len(str(cpf)) != 11:
        return jsonify("Cpf invalido. Padrao aceito: XXXXXXXXXXX")

    email = request.form.get("email")
    if not re.match(r".+@.+\..+", str(email)):
        return jsonify("Email invalido. Padrão aceito: x@y.z")
    
    senha = request.form.get("senha")
    if len(str(senha)) < 4:
        return jsonify("Senha minima de 4 caracteres")
    
    senha_confirmada = request.form.get("senha_confirmada")

    tipo = request.form.get("tipo")

    if senha == senha_confirmada:
        compilacao = hashlib.sha1(str(senha).encode("utf-8")).hexdigest()
        dao = DAO("tb_pessoa")
        pessoa = dao.tb_pessoa
        pessoa.nme_pessoa = nome
        pessoa.cpf_pessoa = cpf
        pessoa.email_pessoa = email
        pessoa.senha_pessoa = compilacao
        pessoa.tipo_pessoa = tipo
        dao.create(pessoa)
        return jsonify("Deu bom")
    else: 
        return jsonify("Deu ruim")
    
@app.route("/api/v0/confirmaocao")
def confirmacao():
    return jsonify("Boa")

@app.route('/api/v0/logout', methods=['GET'])
def logout():
   logout_user()
   return jsonify(**{'result': 200,
                     'data': {'message': 'logout success'}})

@app.route("/api/v0/consultas", methods=['GET'])
@login_required
def consultas():
    dao = DAO("tb_ocorrencias")
    return jsonify("bakugan")

app.run(debug=True)

