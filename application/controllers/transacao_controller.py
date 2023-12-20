from flask import jsonify, request
from flask_restful import Resource
from ..models.transacao_model import TransacaoModel
from ..models.ativos_model import AtivosModel
from ..services.transacao_service import TransacaoService

class TransacaoController(Resource):
    def get(self):
        return jsonify(TransacaoModel.objects())

    def post(self):
        self.nova_transacao = request.get_json()

        if not AtivosModel.objects(ticker=self.nova_transacao.get('ticker')).first():
            return {"message": f"O ticker {self.nova_transacao.get('ticker')} não existe na classe ativos. Registre primeiro para adicionar uma operação"}, 400

        try:
            transacao_service = TransacaoService(self.nova_transacao)
            # Verifica a operação e executa lógicas correspondentes
            if self.nova_transacao.get('operacao') == 'compra':
                resposta = transacao_service.processar_compra()

            elif self.nova_transacao.get('operacao') == 'venda':
                resposta = transacao_service.processar_venda()

            else:
                return {"message": "Tipo de operação não reconhecido"}, 400
            return resposta

        except Exception as e:
            mensagem_erro = f"Erro ao criar a transação: {str(e)}"
            return {"message": mensagem_erro}, 500

    def delete(self):
        TransacaoModel.objects().delete()
        return {"message": "Dados do modelo TransacaoModel deletados"}, 200
