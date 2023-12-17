from ..db import db

class AtivosModel(db.Document):

    ticker = db.StringField(required=True, unique=True)
    classe = db.StringField(required=True)

    ##
    qtd_atual = db.IntField(required=False, default=0)
    qtd_compras_total = db.IntField(required=False, default=0)
    custo_total = db.DecimalField(required=False, precision=2, default=0.0)
    preco_medio = db.DecimalField(required=False, precision=2, default=0.0)