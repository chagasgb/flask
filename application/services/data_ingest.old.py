import json
from flask_restful import Resource, request
from ..models.ativos_model import AtivosModel
from ..models.transacao_model import TransacaoModel
from ..services.transacao_service import TransacaoService

class IngestData(Resource):
    def post(self, model_name):
        
        json_payload = request.get_data(as_text=True)

        if not json_payload:
            return {"message": "Dados JSON não fornecidos no payload"}, 400

        try:
            data = json.loads(json_payload)

            if model_name == 'ativos':
                tickers_existente_nao_adicionados = []
                tickers_adicionados = []
                tickers_no_mesmo_payload = set()

                for entry in data:
                    ticker = entry.get("ticker")
                    classe = entry.get("classe")
                    if not ticker or not classe:
                        print("Erro: Ticker ou classe não encontrados no objeto JSON.")
                        continue

                    existing_ativo = AtivosModel.objects(ticker=ticker).first()

                    if ticker in tickers_no_mesmo_payload:
                        continue

                    if existing_ativo:
                        tickers_existente_nao_adicionados.append(ticker)
                    else:
                        novo_ativo = AtivosModel(ticker=ticker, classe=classe)
                        try:
                            novo_ativo.save()
                            tickers_adicionados.append(ticker)
                            tickers_no_mesmo_payload.add(ticker)
                        except Exception as e:
                            print(f"Erro ao adicionar ativo {ticker}: {str(e)}")

                # Retorna a mensagem de sucesso ou os tickers que foram adicionados
                if tickers_adicionados:
                    return {"tickers_adicionados": tickers_adicionados}, 200
                else:
                    # Nenhum ativo foi adicionado ao modelo
                    return {"message": "Nenhum ativo foi adicionado ao modelo"}, 200

            elif model_name == 'transacoes':
                # Lista para armazenar os objetos TransacaoModel registrados
                transacoes_registradas = []

                for entry in data:
                    ticker = entry.get("ticker")
                    operacao = entry.get("operacao")
                    quantidade = entry.get("quantidade", 0)
                    preco_unitario = entry.get("preco_unitario", 0)
                    valor_operacao = entry.get("valor_operacao", 0) if entry.get("valor_operacao") is not None else None

                    # Cria um novo objeto TransacaoModel com os dados do JSON
                    nova_transacao = TransacaoModel(
                        ticker=ticker,
                        operacao=operacao,
                        quantidade=quantidade,
                        preco_unitario=preco_unitario,
                        valor_operacao=valor_operacao
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

                # Após o loop, processar as transações
                transacao_service = TransacaoService()
                respostas = []
                for transacao in transacoes_registradas:
                    oie = AtivosModel.objects(ticker=transacao["ticker"]).first()
                    resposta = transacao_service.processar_transacao(transacao, oie)
                    respostas.append(resposta)

                return {
                    "message": "Transações registradas com sucesso",
                    "transacoes_registradas": transacoes_registradas,
                    "respostas_processamento": respostas
                }, 201

            else:
                return {"message": "Tipo de dados inválido. Escolha entre 'ativos' e 'transacoes'"}, 400

        except ValueError:
            return {"message": "Erro: JSON inválido no payload"}, 400
        except Exception as e:
            return {"message": f"Erro ao ingerir dados: {str(e)}"}, 500
