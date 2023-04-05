from flask import Flask
import os
from api.api_routes import api 
# from auth.routes import auth

from init_packages import jwt, db ,migrate

def createApp(testing):
    
    app = Flask(__name__)
    if(testing == False): 
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///testDB.sqlite3"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET')if(os.getenv('JWT_SECRET'))else"omjaijagdhishivhare"
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app,db)
    # app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(api)
    with app.app_context(): 
        db.create_all()
    return app
