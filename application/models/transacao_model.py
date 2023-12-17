from ..db import db

from ..db import db

class TransacaoModel(db.Document):
    ticker = db.StringField(required=True)
    operacao = db.StringField(required=True)
    # data_operacao = db.DateTimeField(required=True, format="%Y-%m-%d")
    quantidade = db.FloatField(required=True)
    preco_unitario = db.FloatField(required=True)
    valor_operacao = db.FloatField(required=False, default=None)
