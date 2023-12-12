from model.dao import DAO
from flask import Flask, request, jsonify, redirect, send_file
from flask_login import current_user, LoginManager, login_user, logout_user, login_required, UserMixin
from flask_cors import CORS
from io import BytesIO
from PIL import Image
from werkzeug.utils import secure_filename
import hashlib
import re
import datetime
import os
import base64

app = Flask(__name__)
app.secret_key = 'SubiNumPeDePeraPraArrancarUmaPera'
app.config['UPLOAD_FOLDER'] = 'files/'
app.config['MAX_CONTENT_LENGHT'] = 10 * 1024 * 1024
CORS(app, supports_credentials=True, resources={"/*": {"origins": "*"}}, methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
app.config['CORS_HEADERS'] = 'Content-Type'

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

def filtrar(tipo, status):
    dao = DAO("tb_ocorrencia")
    if status == None and tipo == None:
        lista = dao.readAll()
        json = []
        for i in lista:
            json.append({"id": i.idt_ocorrencia, "nome": i.nme_ocorrencia, "descricao": i.dsc_ocorrencia, "data": i.data_ocorrencia, "cep": i.cep_ocorrencia, "tipo": i.cod_tipo_ocorrencia, "status": i.cod_status_ocorrencia})

        return json
    
    elif status == None:
        lista = dao.readFiltros(f"tb_ocorrencia.cod_tipo_ocorrencia == {tipo}")
        json = []
        for i in lista:
            json.append({"id": i.idt_ocorrencia, "nome": i.nme_ocorrencia, "descricao": i.dsc_ocorrencia, "data": i.data_ocorrencia, "cep": i.cep_ocorrencia, "tipo": i.cod_tipo_ocorrencia, "status": i.cod_status_ocorrencia})

        return json
    
    elif tipo == None:
        lista = dao.readFiltros(f"tb_ocorrencia.cod_status_ocorrencia == {status}")
        json = []
        for i in lista:
            json.append({"id": i.idt_ocorrencia, "nome": i.nme_ocorrencia, "descricao": i.dsc_ocorrencia, "data": i.data_ocorrencia, "cep": i.cep_ocorrencia, "tipo": i.cod_tipo_ocorrencia, "status": i.cod_status_ocorrencia})

        return json

    else:
        lista = dao.readFiltros(f"tb_ocorrencia.cod_tipo_ocorrencia == {tipo}", f", tb_ocorrencia.cod_status_ocorrencia == {status}")
        json = []
        for i in lista:
            json.append({"id": i.idt_ocorrencia, "nome": i.nme_ocorrencia, "descricao": i.dsc_ocorrencia, "data": i.data_ocorrencia, "cep": i.cep_ocorrencia, "tipo": i.cod_tipo_ocorrencia, "status": i.cod_status_ocorrencia})   

        return json

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

@app.route("/login", methods=['POST'])
def login():

    data = request.json

    email = data['email'] # type: ignore
    senha = data['senha'] # type: ignore

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

        data = request.json

        nome = data["nome"] # type: ignore

        cpf = data["cpf"] # type: ignore
        if len(cpf) != 11:
            return jsonify("Cpf invalido. Padrao aceito: XXXXXXXXXXX")
        if len(dao.readBy("cpf_pessoa", "==", cpf)) != 0:
            return jsonify("cpf ja utilizado")

        email = data["email"] # type: ignore
        if not re.match(r".+@.+\..+", str(email)):
            return jsonify("Email invalido. Padrão aceito: x@y.z")

        senha = data["senha"] # type: ignore
        if len(str(senha)) < 4:
            return jsonify("Senha minima de 4 caracteres")

        senha_confirmada = data["senha_confirmada"] # type: ignore

        tipo = data["tipo"] # type: ignore

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
    
@app.route("/consultas/excel")
def confirmacao():
    
    dao = DAO("tb_ocorrencia")

    status = request.args.get("status")
    tipo = request.args.get("tipo")

    lista = filtrar(tipo, status)

    dao.exportToExcel("consultas.xlsx", lista)
    return send_file("consultas.xlsx")

@app.route('/logout', methods=['GET'])
def logout():
   logout_user()
   return jsonify(**{'result': 200,
                     'data': {'message': 'logout success'}})

@app.route("/consultas", methods=['GET']) # type: ignore
@login_required
def consultas():
    
    status = request.args.get("status")
    tipo = request.args.get("tipo")

    return jsonify(filtrar(tipo, status))
    

@app.route("/consultas/<int:idt>", methods=['GET'])
@login_required
def consulta(idt):
    
    dao = DAO("tb_ocorrencia")

    arquivos = []
    arq = dao.readArquivos(idt)

    for arquivo in arq:
        with open(arquivo.arquivo) as img:
            bin = img.read()

        base = base64.b64encode(bin).decode('utf-8') # type: ignore

        json = {
            "idt_arquivo": arquivo.idt_arquivo,
            "nme_arquivo": arquivo.nme_arquivo,
            "base_arquivo": base,
            "formato_arquivo": arquivo.formato_arquivo
        }

        arquivos.append(json)
        
    
    lista = dao.readOcorrencia(idt) 
    if lista[0][0] != None and lista[0][3] != None:
        return jsonify({
            "idt_ocorrencia": lista[0][0].idt_ocorrencia,
            "data_ocorrencia": lista[0][0].data_ocorrencia,
            "cep_ocorrencia": lista[0][0].cep_ocorrencia,
            "tipo_ocorrencia": lista[0][1].nme_tipo_ocorrencia,
            "dsc_ocorrencia": lista[0][0].dsc_ocorrencia,
            "arquivo": arquivos,
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
            "data_final_atendimento": lista[0][3].data_final_atendimento,
            "descricao_atendimento": lista[0][3].dsc_atendimento
        })
    elif lista[0][0] != None:
        return jsonify({
            "idt_ocorrencia": lista[0][0].idt_ocorrencia,
            "data_ocorrencia": lista[0][0].data_ocorrencia,
            "cep_ocorrencia": lista[0][0].cep_ocorrencia,
            "tipo_ocorrencia": lista[0][1].nme_tipo_ocorrencia,
            "dsc_ocorrencia": lista[0][0].dsc_ocorrencia,
            "arquivo": arquivos,
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

    data = request.json

    ocorrencia.nme_ocorrencia = data["nome"] # type: ignore

    ocorrencia.data_ocorrencia = datetime.datetime.now()
    
    ocorrencia.cep_ocorrencia = data["cep"] # type: ignore
    if len(str(ocorrencia.cep_ocorrencia)) != 8:
        return jsonify("Cep invalido. Padrao aceito: XXXXXXXX")

    ocorrencia.dsc_ocorrencia = data["descricao"] # type: ignore

    ocorrencia.cod_tipo_ocorrencia = data["tipo"] # type: ignore
    
    ocorrencia.cod_pessoa = current_user.idt_pessoa # type: ignore
    ocorrencia.cod_status_ocorrencia = 1
    
    daoOcorrecia.create(ocorrencia)

    files = data.get("files") # type: ignore
    if files:
        i = 1
        for file in files: # type: ignore
            # start = files[i].find('/')
            # end = files[i].find(';')
            # formato = files[i][start:end + 1]
            # file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"ocorrencia{ocorrencia.idt_ocorrencia}_{i + 1}.{formato}") # type: ignore
            # imagem = base64.b64decode(files[i])
            # with open(f"ocorrencia{ocorrencia.idt_ocorrencia}_{i + 1}.{formato}", 'wb') as img_file:
            #     img_file.write(imagem)
            
            starter = file.find(',')
            image_data = file[starter + 1:]
            image_data = bytes(image_data, encoding="ascii")
            start = file.find('/') + 1
            end = file.find(';')
            formato = file[start: end]
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"ocorrencia{ocorrencia.idt_ocorrencia}_{i}.{formato}") # type: ignore
            im = Image.open(BytesIO(base64.b64decode(image_data))).convert('RGB')
            im.save(file_path)


            daoArquivo = DAO("tb_arquivo")
            arquivo = daoArquivo.tb_arquivo()

            arquivo.nme_arquivo = f"ocorrencia{ocorrencia.idt_ocorrencia}.{i}"

            arquivo.arquivo = file_path

            arquivo.formato_arquivo = formato # type: ignore

            arquivo.cod_ocorrencia = ocorrencia.idt_ocorrencia

            daoArquivo.create(arquivo)

            i += 1

        return jsonify("arquivos criados")

            
    
    return jsonify("Sem arquivos")

@app.route("/atendimento/<int:idt>", methods=['PUT'])
@login_required
def atendimento(idt):

    daoOcorrencia = DAO("tb_ocorrencia")
    tem = daoOcorrencia.readById(idt) 
    if tem:
        data = request.json

        daoAtendimento = DAO("tb_atendimento")
        oc = daoOcorrencia.readById(idt)
        lista = daoAtendimento.readBy("cod_ocorrencia", "==", idt)
        if len(lista) == 0:
            atendimento = daoAtendimento.tb_atendimento()

            atendimento.cod_ocorrencia = idt
            atendimento.dsc_atendimento = data["descricao"] # type: ignore
            atendimento.cod_pessoa = current_user.idt_pessoa # type: ignore
            atendimento.data_inicial_atendimento = datetime.datetime.now()
            oc.cod_status_ocorrencia = data["status"] # type: ignore
            if data["status"] == 3: # type: ignore
                atendimento.data_final_atendimento = datetime.datetime.now()

            daoAtendimento.create(atendimento)
            daoOcorrencia.update()
            return jsonify(lista)
        else:
            lista[0].cod_pessoa = current_user.idt_pessoa # type: ignore
            atendimento.dsc_atendimento = data["descricao"] # type: ignore
            oc.cod_status_ocorrencia = data["status"] # type: ignore
            if data[status] == 3: # type: ignore
                atendimento.data_final_atendimento = datetime.datetime.now() # type: ignore

        daoOcorrencia.update()
        daoAtendimento.update()
        return jsonify("atendido")
    
    return jsonify(f"nao foi possivel encontra a ocorrencia: {idt}")

app.run(debug=True, port=5000)