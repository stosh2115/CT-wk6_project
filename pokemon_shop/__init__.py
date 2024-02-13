from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from config import Config
from .blueprints.site.routes import site
from .blueprints.auth.routes import auth
from .blueprints.api.routes import api
from .models import login_manager, db
from .helpers import JSONEncoder


app = Flask(__name__)
app.config.from_object(Config)
jwt = JWTManager(app)



app.register_blueprint(site)
app.register_blueprint(auth)


login_manager.init_app(app)
login_manager.login_view = 'auth.sign_in'
login_manager.login_message = "Hello Please Log in"
login_manager.login_message_category = 'warning'



db.init_app(app)
migrate = Migrate(app,db)
app.json_encoder = JSONEncoder
cors = CORS(app)
