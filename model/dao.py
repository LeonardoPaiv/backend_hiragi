from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

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
        lista = self.ses.query(self.tb_ocorrencia, self.tb_tipo_ocorrencia, self.tb_status_ocorrencia, self.tb_atendimento, self.tb_pessoa, self.tb_arquivo)\
                       .outerjoin(self.tb_atendimento, self.tabela.idt_ocorrencia == self.tb_atendimento.cod_ocorrencia)\
                       .outerjoin(self.tb_arquivo, self.tb_arquivo.cod_ocorrencia == self.tb_ocorrencia.idt_ocorrencia)\
                       .outerjoin(self.tb_status_ocorrencia, self.tb_ocorrencia.cod_status_ocorrencia == self.tb_status_ocorrencia.idt_status_ocorrencia)\
                       .outerjoin(self.tb_tipo_ocorrencia, self.tb_ocorrencia.cod_tipo_ocorrencia == self.tb_tipo_ocorrencia.idt_tipo_ocorrencia)\
                       .outerjoin(self.tb_pessoa, self.tb_atendimento.cod_pessoa == self.tb_pessoa.idt_pessoa)\
                       .filter(eval(exp))\
                       .all()
        return lista # 0 3 5

   def update(self):
       self.ses.commit()

   def delete(self, obj):
       self.ses.delete(obj)
       self.ses.commit()

   def getSes(self):
       return self.ses

   def __del__(self):
       self.ses.close()