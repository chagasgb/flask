from flask import Flask
from flask_restful import Api, Resource
from .db import init_db
from .controllers.transacao_controller import TransacaoController
from .controllers.ativos_controller import AtivosController
from .services.data_ingest import IngestData


class ConnectionResource(Resource):
    def get(self):
        return {'message': 'Conexão bem-sucedida!'}, 200

def create_app(config):
    app = Flask(__name__)
    api = Api(app)
    app.config.from_object(config)
    init_db(app)

    api.add_resource(TransacaoController, '/transacao')
    api.add_resource(AtivosController, '/ativos')
    
    # Adicione o novo recurso à rota raiz ("/")
    api.add_resource(ConnectionResource, '/'), 200
    api.add_resource(IngestData, '/ingest')

    #api.add_resource(IngestData, '/oie')

    return app
