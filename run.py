from flask import Flask,  url_for, redirect
from flask import Blueprint
from flask_restful import Api
from models.baseModel import db
from resources.check import Hello
from resources.housesResource import HouseResource, HouseResourceCount
from resources.usersResource import UserResource
from resources.matchesResource import MatchResource
from resources.cnnResource import CNNResource
from resources.predictionsResource import PredResource
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
app.config.from_object('config')
api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)

SWAGGER_URL='/swagger'
API_URL='/static/swagger.json'

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config ={
        'app-name':'is-swagger-useful'
    }
)

# routes 
@app.route('/')
def landing_page(): 
    return 'Welcome to the ZenDen Backend API. Use /swagger for documentation.'
api.add_resource(Hello,'/Hello')
api.add_resource(HouseResource, '/Houses')
api.add_resource(HouseResourceCount, '/Houses/<count>')
api.add_resource(UserResource, '/Users')
api.add_resource(MatchResource, '/Matches')
api.add_resource(CNNResource,'/CNN')
api.add_resource(PredResource, '/Predictions')
print(api.endpoints)

app.register_blueprint(api_blueprint, url_prefix='/api')
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

db.init_app(app)


if __name__ == "__main__": 
    app.run()