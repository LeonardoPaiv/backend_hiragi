from model.dao import DAO
from flask import Flask, request, jsonify, redirect
from flask_login import current_user, LoginManager, login_user, logout_user, login_required, UserMixin
from flask_cors import CORS
import hashlib
import re
import datetime
import os

app = Flask(__name__)
app.secret_key = 'SubiNumPeDePeraPraArrancarUmaPera'
app.config['UPLOAD_FOLDER'] = './uploads'
CORS(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # type: ignore

class User(UserMixin):
   idt_pessoa = 0
   nme_pessoa = ''
   cpf_pessoa = ''
   email_pessoa = ''
   tipo_pessoa = -1

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
       usr.email_pessoa = str(lista[0].email_pessoa)
       usr.tipo_pessoa = lista[0].tipo_pessoa
       return usr
   else:
       return None


@app.route("/")
def index():
    if current_user.is_authenticated: # type: ignore
        return redirect("/consultas")
    else:
        return redirect("/login")

@app.route("/login", methods=['GET'])
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
        usr.email_pessoa = str(lista[0].email_pessoa)
        usr.tipo_pessoa = lista[0].tipo_pessoa
        login_user(usr, remember=True)

        if current_user.is_authenticated: # type: ignore
            return jsonify("usuario encontrado")
        else:
            return jsonify("usuario nao encontrado")
    else:
        return jsonify("login ou senha incorretos")

@app.route("/cadastro", methods=['PUT'])
def cadastro():

    dao = DAO("tb_pessoa")

    nome = request.args.get("nome")

    cpf = request.args.get("cpf")
    if len(str(cpf)) != 11:
        return jsonify("Cpf invalido. Padrao aceito: XXXXXXXXXXX")
    if len(dao.readBy("cpf_pessoa", "==", cpf)) != 0:
        return jsonify("cpf ja utilizado")

    email = request.args.get("email")
    if not re.match(r".+@.+\..+", str(email)):
        return jsonify("Email invalido. Padrão aceito: x@y.z")
    
    senha = request.args.get("senha")
    if len(str(senha)) < 4:
        return jsonify("Senha minima de 4 caracteres")
    
    senha_confirmada = request.args.get("senha_confirmada")

    tipo = request.args.get("tipo")

    if senha == senha_confirmada:
        compilacao = hashlib.sha1(str(senha).encode("utf-8")).hexdigest()
        dao = DAO("tb_pessoa")
        pessoa = dao.tb_pessoa()
        pessoa.nme_pessoa = nome
        pessoa.cpf_pessoa = cpf
        pessoa.email_pessoa = email
        pessoa.senha_pessoa = compilacao
        pessoa.tipo_pessoa = tipo
        dao.create(pessoa)
        return jsonify("Deu bom")
    else: 
        return jsonify("Senhas nao coincidem.")
    
@app.route("/confirmacao")
def confirmacao():
    dao = DAO("tb_tipo_ocorrencia")
    lista = dao.readAll()
    for i in lista:
        print(i.nme_tipo_ocorrencia)
    return jsonify("Confirmado")

@app.route('/logout', methods=['GET'])
def logout():
   logout_user()
   return jsonify(**{'result': 200,
                     'data': {'message': 'logout success'}})

@app.route("/consultas", methods=['GET'])
@login_required
def consultas():
    dao = DAO("tb_ocorrencia")
    usuario = current_user
    if usuario.tipo_pessoa == 1: # type: ignore
        lista = dao.readAll()
        json = []
        for i in lista:
            json.append({"id": i.idt_ocorrencia, "nome": i.nme_ocorrencia, "descricao": i.dsc_ocorrencia, "data": i.data_ocorrencia, "cep": i.cep_ocorrencia, "Tipo": i.cod_tipo_ocorrencia, "status": i.cod_status_ocorrencia})
        return jsonify(json)
    else:
        lista = dao.readBy("cod_pessoa", "==", usuario.idt_pessoa) # type: ignore
        json = []
        for i in lista:
            json.append({"id": i.idt_ocorrencia, "nome": i.nme_ocorrencia, "descricao": i.dsc_ocorrencia, "data": i.data_ocorrencia, "cep": i.cep_ocorrencia, "Tipo": i.cod_tipo_ocorrencia, "status": i.cod_status_ocorrencia})
        return jsonify(json)

@app.route("/criar_ocorrencia", methods=['PUT'])
@login_required
def criar_ocorrencia():

    daoOcorrecia = DAO("tb_ocorrencia")
    ocorrencia = daoOcorrecia.tb_ocorrencia()

    daoTipo = DAO("tb_tipo_ocorrencia")
    lista = daoTipo.readAll()
    tipos = []
    for i in lista:
        tipos.append(i.nme_tipo_ocorrencia)

    # ocorrencia.data_ocorrencia = request.args.get("data")
    # if not re.match(r"(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})", str(ocorrencia.data_ocorrencia)):
    #     return jsonify("Data invalida. Padrão aceito: AAAA-MM-DD HH:MM:SS")

    ocorrencia.nme_ocorrencia = request.args.get("nome")

    ocorrencia.data_ocorrencia = datetime.datetime.now()
    
    ocorrencia.cep_ocorrencia = request.args.get("cep")
    if len(str(ocorrencia.cep_ocorrencia)) != 8:
        return jsonify("Cep invalido. Padrao aceito: XXXXXXXX")

    ocorrencia.dsc_ocorrencia = request.args.get("descricao")

    tipo = request.args.get("tipo")
    if tipo not in tipos:
        return jsonify(f"Tipos aceitos: {tipos}")
    
    ocorrencia.cod_tipo_ocorrencia = daoTipo.readByNme(tipo)[0].idt_tipo_ocorrencia
    ocorrencia.cod_pessoa = current_user.idt_pessoa # type: ignore
    ocorrencia.cod_status_ocorrencia = 1
    
    daoOcorrecia.create(ocorrencia)

    return jsonify({
        "nome": ocorrencia.nme_ocorrencia,
        "data": ocorrencia.data_ocorrencia,
        "cep":  ocorrencia.cep_ocorrencia,
        "descricao": ocorrencia.dsc_ocorrencia,
        "tipo": tipo,
        "pessoa": ocorrencia.cod_pessoa,
        "status": ocorrencia.cod_status_ocorrencia
    })


    # file = request.files["file"]
    # file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename)) # type: ignore
    # return 'File uploaded successfully'

app.run(debug=True, port=5000)