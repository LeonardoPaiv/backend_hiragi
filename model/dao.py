from sqlalchemy import create_engine, and_
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
import pandas as pd

class DAO:

    def __init__(self, tab):
       # Ligação com o esquema de banco de dados
       engine = create_engine("mysql+mysqlconnector://root:uniceub@localhost/real?charset=utf8mb4")

       # Mapeamento Objeto Relacional com o SQLAlchemy
       db = automap_base()
       db.prepare(autoload_with=engine)
       self.tb_arquivo = db.classes.tb_arquivo
       self.tb_atendimento = db.classes.tb_atendimento
       self.tb_ocorrencia = db.classes.tb_ocorrencia
       self.tb_pessoa = db.classes.tb_pessoa
       self.tb_status_ocorrencia = db.classes.tb_status_ocorrencia
       self.tb_tipo_ocorrencia = db.classes.tb_tipo_ocorrencia

       self.tabela = eval("db.classes." + tab)
       self.idt = "idt_" + tab[3:len(tab)]
       self.nme = "nme_" + tab[3:len(tab)]

       # Trabalho com sessões da base Objeto-Relacional
       session_factory = sessionmaker(bind=engine)
       self.ses = session_factory()
       # -------------------------------------------------------------------------------------------------

    def create(self, obj):
       self.ses.add(obj)
       self.ses.commit()

    def readAll(self):
       lista = self.ses.query(self.tabela).all()
       return lista

    def readById(self, id):
       exp = "self.tabela." + self.idt + "== id"
       obj = self.ses.query(self.tabela).filter(eval(exp)).first() # type: ignore
       return obj

    def readByNme(self, nm):
       exp = "self.tabela." + self.nme + ".ilike('%' + nm + '%')"
       lista = self.ses.query(self.tabela).filter(eval(exp)).all() # type: ignore
       return lista

    def readBy(self, campo, oper, valor):

       if oper == "==":
           exp = "self.tabela." + campo + "==valor"
       elif oper == "ilike":
           exp = "self.tabela." + campo + ".ilike('%' + valor + '%')"
       else:
           exp = "self.tabela." + campo + oper + "valor"

       lista = self.ses.query(self.tabela).filter(eval(exp)).all() # type: ignore
       return lista
   
    def readOcorrencia(self, idt):
        exp = "self.tabela." + self.idt + "== idt"
        lista = self.ses.query(self.tb_ocorrencia, self.tb_tipo_ocorrencia, self.tb_status_ocorrencia, self.tb_atendimento, self.tb_pessoa)\
                       .outerjoin(self.tb_atendimento, self.tabela.idt_ocorrencia == self.tb_atendimento.cod_ocorrencia)\
                       .outerjoin(self.tb_status_ocorrencia, self.tb_ocorrencia.cod_status_ocorrencia == self.tb_status_ocorrencia.idt_status_ocorrencia)\
                       .outerjoin(self.tb_tipo_ocorrencia, self.tb_ocorrencia.cod_tipo_ocorrencia == self.tb_tipo_ocorrencia.idt_tipo_ocorrencia)\
                       .outerjoin(self.tb_pessoa, self.tb_atendimento.cod_pessoa == self.tb_pessoa.idt_pessoa)\
                       .filter(eval(exp))\
                       .all()
        return lista
   
    def readArquivos(self, idt):
       lista = self.ses.query(self.tb_arquivo).filter(self.tb_arquivo.cod_ocorrencia == idt).all() # type: ignore
       return lista
   
    def readFiltros(self, status, tipo):
       
        if status == None and tipo == None:
            lista = self.ses.query(self.tabela, self.tb_status_ocorrencia, self.tb_tipo_ocorrencia).outerjoin(self.tb_status_ocorrencia, self.tb_ocorrencia.cod_status_ocorrencia == self.tb_status_ocorrencia.idt_status_ocorrencia).outerjoin(self.tb_tipo_ocorrencia, self.tb_ocorrencia.cod_tipo_ocorrencia == self.tb_tipo_ocorrencia.idt_tipo_ocorrencia).all()
            return lista
    
        elif status == None:
            tipos = [int(t) for t in tipo.split(',')]
            lista = self.ses.query(self.tabela, self.tb_status_ocorrencia, self.tb_tipo_ocorrencia).outerjoin(self.tb_status_ocorrencia, self.tb_ocorrencia.cod_status_ocorrencia == self.tb_status_ocorrencia.idt_status_ocorrencia).outerjoin(self.tb_tipo_ocorrencia, self.tb_ocorrencia.cod_tipo_ocorrencia == self.tb_tipo_ocorrencia.idt_tipo_ocorrencia).filter(self.tabela.cod_tipo_ocorrencia.in_(tipos)).all() # type: ignore
            return lista
    
        elif tipo == None:
            lista = self.ses.query(self.tabela, self.tb_status_ocorrencia, self.tb_tipo_ocorrencia).outerjoin(self.tb_status_ocorrencia, self.tb_ocorrencia.cod_status_ocorrencia == self.tb_status_ocorrencia.idt_status_ocorrencia).outerjoin(self.tb_tipo_ocorrencia, self.tb_ocorrencia.cod_tipo_ocorrencia == self.tb_tipo_ocorrencia.idt_tipo_ocorrencia).filter(self.tabela.cod_status_ocorrencia == status).all() # type: ignore
            return lista

        else:
            tipos = [int(t) for t in tipo.split(',')]
            lista = self.ses.query(self.tabela, self.tb_status_ocorrencia, self.tb_tipo_ocorrencia).outerjoin(self.tb_status_ocorrencia, self.tb_ocorrencia.cod_status_ocorrencia == self.tb_status_ocorrencia.idt_status_ocorrencia).outerjoin(self.tb_tipo_ocorrencia, self.tb_ocorrencia.cod_tipo_ocorrencia == self.tb_tipo_ocorrencia.idt_tipo_ocorrencia).filter(and_(self.tabela.cod_tipo_ocorrencia.in_(tipos), self.tabela.cod_status_ocorrencia == status)).all() # type: ignore
            return lista

    def update(self):
        self.ses.commit()

    def delete(self, obj):
       self.ses.delete(obj)
       self.ses.commit()

    def getSes(self):
       return self.ses
   
    def exportToExcel(self, filename, data):
        # Lê todos os dados da tabela

        # Converte os dados para um DataFrame do pandas
        df = pd.DataFrame(data)

        # Cria um arquivo Excel usando o openpyxl
        writer = pd.ExcelWriter(filename, engine='openpyxl')
        df.to_excel(writer, index=False)
        writer.close() # type: ignore

    def __del__(self):
       self.ses.close()
