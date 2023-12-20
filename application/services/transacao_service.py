from decimal import Decimal
from ..models.transacao_model import TransacaoModel
from ..models.ativos_model import AtivosModel

class TransacaoService:
    def __init__(self, nova_transacao):
        self.nova_transacao = nova_transacao

    @staticmethod
    def _processar_transacao(nova_transacao, operacao):
        quantidade = Decimal(nova_transacao.get('quantidade', 0))
        preco_unitario = Decimal(nova_transacao.get('preco_unitario', 0))
        valor_operacao = quantidade * preco_unitario

        response = TransacaoModel(
            ticker=nova_transacao.get('ticker'),
            operacao=operacao,
            quantidade=quantidade,
            preco_unitario=preco_unitario,
            valor_operacao=valor_operacao
        ).save()

        return response

    def processar_compra(self):
        response = self._processar_transacao(self.nova_transacao, 'compra')

        ticker_existente = AtivosModel.objects(ticker=self.nova_transacao.get('ticker')).first()

        ticker_existente.qtd_atual += response.quantidade
        ticker_existente.qtd_compras_total += response.quantidade
        ticker_existente.custo_total += response.valor_operacao
        ticker_existente.save()

        ticker_existente.preco_medio = ticker_existente.custo_total / ticker_existente.qtd_compras_total
        ticker_existente.save()

        mensagem = f"Transação de compra criada com sucesso, ID: {response.id}"
        return {"message": mensagem}, 201
    
    def processar_venda(self):
        response = self._processar_transacao(self.nova_transacao, 'venda')

        ticker_existente = AtivosModel.objects(ticker=self.nova_transacao.get('ticker')).first()

        ticker_existente.qtd_atual -= response.quantidade
        ticker_existente.save()

        mensagem = f"Transação de venda criada com sucesso, ID: {response.id}"
        return {"message": mensagem}, 201
