from model.dao import DAO
from flask import Flask, request, jsonify, redirect
from flask_login import current_user, LoginManager, login_user, logout_user, login_required, UserMixin
from flask_cors import CORS
from werkzeug.utils import secure_filename
import hashlib
import re
import datetime
import os

app = Flask(__name__)
app.secret_key = 'SubiNumPeDePeraPraArrancarUmaPera'
app.config['UPLOAD_FOLDER'] = 'files/'
app.config['MAX_CONTENT_LENGHT'] = 10 * 1024 * 1024
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
    email = request.args.get('email', default="", type=str)
    senha = request.args.get('senha', default="", type=str)

    dao = DAO("tb_pessoa")

    lista = dao.readBy("email_pessoa", "==", email)
    compilacao = hashlib.sha1(senha.encode("utf-8")).hexdigest()

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

@app.route("/cadastro", methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        dao = DAO("tb_pessoa")

        nome = request.form.get("nome")

        cpf = str(request.form.get("cpf"))
        print(len(cpf))
        if len(cpf) != 11:
            return jsonify("Cpf invalido. Padrao aceito: XXXXXXXXXXX")
        if len(dao.readBy("cpf_pessoa", "==", cpf)) != 0:
            return jsonify("cpf ja utilizado")

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
    else:
        return jsonify("pomba")
    
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

@app.route("/consultas/<int:idt>", methods=['GET'])
@login_required
def consulta(idt):
    
    dao = DAO("tb_ocorrencia")
    
    lista = dao.readOcorrencia(idt) 
    print(lista)
    if lista[0][0] != None and lista[0][3] != None and lista[0][5] != None:
        return jsonify({
            "idt_ocorrencia": lista[0][0].idt_ocorrencia,
            "data_ocorrencia": lista[0][0].data_ocorrencia,
            "cep_ocorrencia": lista[0][0].cep_ocorrencia,
            "tipo_ocorrencia": lista[0][1].nme_tipo_ocorrencia,
            "dsc_ocorrencia": lista[0][0].dsc_ocorrencia,
            "arquivo": {
                "idt_arquivo": lista[0][5].idt_arquivo,
                "nme_arquivo": lista[0][5].nme_arquivo,
                "path_arquivo": lista[0][5].arquivo,
                "formato_arquivo": lista[0][5].formato_arquivo
            },
            "status_ocorrencia": lista[0][2].nme_status_ocorrencia,
            "data_inicio_atendimento": lista[0][3].data_inicial_atendimento,
            "data_inicio_atendimento": lista[0][3].data_final_atendimento,
            "descricao_atendimento": lista[0][3].dsc_atendimento
        })
    elif lista[0][0] != None and lista[0][3] != None:
        return jsonify({
            "idt_ocorrencia": lista[0][0].idt_ocorrencia,
            "data_ocorrencia": lista[0][0].data_ocorrencia,
            "cep_ocorrencia": lista[0][0].cep_ocorrencia,
            "tipo_ocorrencia": lista[0][1].nme_tipo_ocorrencia,
            "dsc_ocorrencia": lista[0][0].dsc_ocorrencia,
            "status_ocorrencia": lista[0][2].nme_status_ocorrencia,
            "data_inicio_atendimento": lista[0][3].data_inicial_atendimento,
            "data_inicio_atendimento": lista[0][3].data_final_atendimento,
            "descricao_atendimento": lista[0][3].dsc_atendimento
        })
    elif lista[0][0] != None and lista[0][5] != None:
        return jsonify({
            "idt_ocorrencia": lista[0][0].idt_ocorrencia,
            "data_ocorrencia": lista[0][0].data_ocorrencia,
            "cep_ocorrencia": lista[0][0].cep_ocorrencia,
            "tipo_ocorrencia": lista[0][1].nme_tipo_ocorrencia,
            "dsc_ocorrencia": lista[0][0].dsc_ocorrencia,
            "arquivo": {
                "idt_arquivo": lista[0][5].idt_arquivo,
                "nme_arquivo": lista[0][5].nme_arquivo,
                "path_arquivo": lista[0][5].arquivo,
                "formato_arquivo": lista[0][5].formato_arquivo,
            },
            "status_ocorrencia": lista[0][2].nme_status_ocorrencia
        })

    return jsonify(f"nao foi possivel encontra a ocorrencia: {idt}")

@app.route("/criar_ocorrencia", methods=['POST'])
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

    ocorrencia.nme_ocorrencia = request.form.get("nome")

    ocorrencia.data_ocorrencia = datetime.datetime.now()
    
    ocorrencia.cep_ocorrencia = request.form.get("cep")
    if len(str(ocorrencia.cep_ocorrencia)) != 8:
        return jsonify("Cep invalido. Padrao aceito: XXXXXXXX")

    ocorrencia.dsc_ocorrencia = request.form.get("descricao")

    ocorrencia.cod_tipo_ocorrencia = request.form.get("tipo")
    # if tipo not in tipos:
    #     return jsonify(f"Tipos aceitos: {tipos}")
    
    # ocorrencia.cod_tipo_ocorrencia = daoTipo.readByNme(tipo)[0].idt_tipo_ocorrencia
    ocorrencia.cod_pessoa = current_user.idt_pessoa # type: ignore
    ocorrencia.cod_status_ocorrencia = 1
    
    daoOcorrecia.create(ocorrencia)

    file = request.files["file"]
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)) # type: ignore
        file.save(file_path) 

        daoArquivo = DAO("tb_arquivo")
        arquivo = daoArquivo.tb_arquivo()

        arquivo.nme_arquivo = file.filename

        arquivo.arquivo = file_path

        arquivo.formato_arquivo = file.filename.rsplit('.', 1)[1] # type: ignore

        arquivo.cod_ocorrencia = ocorrencia.idt_ocorrencia

        daoArquivo.create(arquivo)

        return jsonify({
            "idt": arquivo.idt_arquivo,
            "nome": arquivo.nme_arquivo,
            "path": arquivo.arquivo,
            "formato": arquivo.formato_arquivo,
            "ocorrencia": arquivo.cod_ocorrencia
        })
    
    return jsonify("Sem arquivo")



app.run(debug=True, port=5000)