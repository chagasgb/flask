import json
from flask_restful import Resource, request
from ..models.ativos_model import AtivosModel
from ..models.transacao_model import TransacaoModel
from ..services.transacao_service import TransacaoService

class IngestData(Resource):
    def post(self):
        json_payload = request.get_data(as_text=True)

        if not json_payload:
            return {"message": "Dados JSON não fornecidos no payload"}, 400

        try:
            data = json.loads(json_payload)
        except json.JSONDecodeError as e:
            return {"message": f"Erro ao decodificar JSON: {str(e)}"}, 400

        tickers_adicionados = []
        tickers_no_mesmo_payload = set()
        transacoes_registradas = []

        for entry in data:
            ticker = entry.get("ticker")

            if not ticker:
                print("Erro: Ticker não encontrado no objeto JSON.")
                continue

            existing_ativo = AtivosModel.objects(ticker=ticker).first()

            if ticker in tickers_no_mesmo_payload:
                continue

            if not existing_ativo:
                self.adicionar_ativo(ticker, entry.get("classe"), tickers_adicionados, tickers_no_mesmo_payload)
                
            self.adicionar_transacao(ticker, entry, transacoes_registradas)

        # Após o loop, processar as transações
        transacao_service = TransacaoService()
        respostas = [transacao_service.processar_transacao(transacao, AtivosModel.objects(ticker=transacao["ticker"]).first()) 
                     for transacao in transacoes_registradas]

        return {
            "tickers_adicionados": tickers_adicionados,
            "transacoes_registradas": transacoes_registradas,
            "respostas_processamento": respostas
        }, 201



    def adicionar_ativo(self, ticker, classe, tickers_adicionados, tickers_no_mesmo_payload):
        novo_ativo = AtivosModel(ticker=ticker, classe=classe)
        try:
            novo_ativo.save()
            tickers_adicionados.append(ticker)
            tickers_no_mesmo_payload.add(ticker)
            print(f"Ativo {ticker} registrado com sucesso.")
        except Exception as e:
            print(f"Erro ao adicionar ativo {ticker}: {str(e)}")


    def adicionar_transacao(self, ticker, entry, transacoes_registradas):
        nova_transacao = TransacaoModel(
            ticker=ticker,
            operacao=entry.get("operacao"),
            quantidade=entry.get("quantidade", 0.0),
            preco_unitario=entry.get("preco_unitario", 0.0),
            valor_operacao=entry.get("valor_operacao", 0.0)
        )

        try:
            nova_transacao.save()
            transacoes_registradas.append({
                "ticker": nova_transacao.ticker,
                "operacao": nova_transacao.operacao,
                "quantidade": nova_transacao.quantidade,
                "preco_unitario": nova_transacao.preco_unitario,
                "valor_operacao": nova_transacao.valor_operacao
            })

            print(f"Transação para {ticker} registrada com sucesso.")
        except Exception as e:
            print(f"Erro ao registrar transação para {ticker}: {str(e)}")
