from ..db import db

from mongoengine import Document, StringField, DecimalField

class TransacaoModel(Document):
    ticker = StringField(required=True)
    operacao = StringField(required=True)
    # data_operacao = DateTimeField(required=True, format="%Y-%m-%d")
    quantidade = DecimalField(required=True, precision=2)  # Ajuste a precisão conforme necessário
    preco_unitario = DecimalField(required=True, precision=2)  # Ajuste a precisão conforme necessário
    valor_operacao = DecimalField(required=False, default=None, precision=2)  # Ajuste a precisão conforme necessário
