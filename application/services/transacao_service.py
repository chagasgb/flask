from decimal import Decimal
import json
from ..models.transacao_model import TransacaoModel

class TransacaoService:
    def processar_transacao(self, nova_transacao, ticker_existente=None):
        if nova_transacao.get('operacao') == 'Compra':

            quantidade = Decimal(str(nova_transacao.get('quantidade', 0)))
            preco_unitario = Decimal(str(nova_transacao.get('preco_unitario', 0)))
            
            valor_operacao = quantidade * preco_unitario

            response = TransacaoModel(
                ticker=nova_transacao.get('ticker'),
                operacao=nova_transacao.get('operacao'),
                quantidade=quantidade,
                preco_unitario=preco_unitario,
                valor_operacao=valor_operacao
            ).save()

            ticker_existente.qtd_atual += quantidade
            ticker_existente.qtd_compras_total += quantidade
            ticker_existente.custo_total += valor_operacao
            ticker_existente.save()

            ticker_existente.preco_medio = ticker_existente.custo_total / ticker_existente.qtd_compras_total
            ticker_existente.save()

            mensagem = f"Transação de compra criada com sucesso, ID: {response.id}"
            return {"message": mensagem}, 201

        elif nova_transacao.get('operacao') == 'Venda':
            quantidade = Decimal(str(nova_transacao.get('quantidade', 0)))
            response = TransacaoModel(
                ticker=nova_transacao.get('ticker'),
                operacao=nova_transacao.get('operacao'),
                quantidade=quantidade,
                preco_unitario=Decimal(str(nova_transacao.get('preco_unitario', 0))),
                valor_operacao=quantidade * Decimal(str(nova_transacao.get('preco_unitario', 0)))
            ).save()

            ticker_existente.qtd_atual -= quantidade
            ticker_existente.save()

            mensagem = f"Transação de venda criada com sucesso, ID: {response.id}"
            return {"message": mensagem}, 201

        else:
            mensagem = "Tipo de operação não reconhecido"
            return {"message": mensagem}, 400
