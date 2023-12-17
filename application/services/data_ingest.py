import json
from flask_restful import Resource, request
from ..models.ativos_model import AtivosModel
from ..models.transacao_model import TransacaoModel
from ..services.transacao_service import TransacaoService

class IngestData(Resource):
    def post(self):
        try:
            # Use request.get_json() para obter diretamente o JSON do corpo da solicitação
            data = request.get_json()

            if not data:
                return {"message": "Dados JSON não fornecidos no payload"}, 400

            tickers_adicionados = set()
            transacoes_registradas = []

            for entry in data:
                if not isinstance(entry, dict):
                    print(f"Erro: Entrada inválida no objeto JSON: {entry}")
                    continue

                ticker = entry.get("ticker")
                classe = entry.get("classe")

                if not ticker:
                    print("Erro: Ticker não encontrado no objeto JSON.")
                    continue

                existing_ativo = AtivosModel.objects(ticker=ticker).first()

                if not existing_ativo and ticker not in tickers_adicionados:
                    self.adicionar_ativo(ticker, classe, tickers_adicionados)

                transacao = self.adicionar_transacao(ticker, entry)

                if transacao:
                    transacoes_registradas.append(transacao)

            # Após o loop, processar as transações
            transacao_service = TransacaoService()
            respostas = [transacao_service.processar_transacao(
                transacao, 
                AtivosModel.objects(ticker=transacao["ticker"]).first() if "ticker" in transacao else None
            ) for transacao in transacoes_registradas]

            return {
                "tickers_adicionados": list(tickers_adicionados),
                "transacoes_registradas": transacoes_registradas,
                "respostas_processamento": respostas
            }, 201

        except ValueError:
            return {"message": "Erro: JSON inválido no payload"}, 400
        except Exception as e:
            return {"message": f"Erro ao ingerir dados: {str(e)}"}, 500

    def adicionar_ativo(self, ticker, classe, tickers_adicionados):
        novo_ativo = AtivosModel(ticker=ticker, classe=classe)
        try:
            novo_ativo.save()
            tickers_adicionados.add(ticker)
            print(f"Ativo {ticker} registrado com sucesso.")
        except Exception as e:
            print(f"Erro ao adicionar ativo {ticker}: {str(e)}")

    def adicionar_transacao(self, ticker, entry):
        try:
            nova_transacao = TransacaoModel(
                ticker=ticker,
                operacao=entry.get("operacao"),
                quantidade=entry.get("quantidade", 0.0),
                preco_unitario=entry.get("preco_unitario", 0.0),
                valor_operacao=entry.get("valor_operacao", 0.0)
            )

            nova_transacao.save()

            return {
                "ticker": nova_transacao.ticker,
                "operacao": nova_transacao.operacao,
                "quantidade": float(nova_transacao.quantidade),
                "preco_unitario": float(nova_transacao.preco_unitario),
                "valor_operacao": float(nova_transacao.valor_operacao)
            }

        except Exception as e:
            print(f"Erro ao registrar transação para {ticker}: {str(e)}")
            return None
