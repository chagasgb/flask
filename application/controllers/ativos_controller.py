from flask import jsonify, request
from flask_restful import Resource

from ..models.transacao_model import TransacaoModel
from ..models.ativos_model import AtivosModel

class AtivosController(Resource):
    def get(self):
        return jsonify(AtivosModel.objects())

    def post(self):
        novo_ativo = request.get_json()
        if AtivosModel.objects(ticker=novo_ativo['ticker']):
            return {"message": f"Já existe um ativo com o ticker {novo_ativo['ticker']}"}, 400

        response = AtivosModel(**novo_ativo).save()
        return {"message": "ATIVO CRIADO COM SUCESSO", "id_ativo": str(response.id)}, 201

    def delete(self):
        AtivosModel.objects().delete()
        return {"message": "Dados do modelo AtivosModel deletados"}, 200