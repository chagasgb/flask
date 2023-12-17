from flask import jsonify, request
from flask_restful import Resource

from ..models.transacao_model import TransacaoModel
from ..models.ativos_model import AtivosModel
from ..services.transacao_service import TransacaoService 

class TransacaoController(Resource):
    def get(self):
        return jsonify(TransacaoModel.objects())

    def post(self):
        nova_transacao = request.get_json()

        # Verifica se o ticker existe na classe AtivosModel
        ticker_existente = AtivosModel.objects(ticker=nova_transacao.get('ticker')).first()

        if not ticker_existente:
            return {"message": f"O ticker {nova_transacao.get('ticker')} não existe na classe ativos. Registre primeiro para adicionar uma operação"}, 400

        try:
            # Cria uma instância do serviço e chama o método de instância
            transacao_service = TransacaoService()
            resposta = transacao_service.processar_transacao(nova_transacao, ticker_existente)
            return resposta
        
        except Exception as e:
            mensagem_erro = f"Erro ao criar a transação: {str(e)}"
            return {"message": mensagem_erro}, 500
        
    def delete(self):
        TransacaoModel.objects().delete()
        return {"message": "Dados do modelo TransacaoModel deletados"}, 200
