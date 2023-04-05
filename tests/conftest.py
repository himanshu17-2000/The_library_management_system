import pytest
from flask import jsonify
from init_app import createApp

import json
@pytest.fixture()
def app():
    testing = True
    app  = createApp(testing = True) 
    # app.config.update({
    #     "TESTING": True,
    # })
    return app 

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

# @pytest.fixture()
# def create_member(client):
#     Member()
#     # data1 = {"name": "Bhakti", "email": "Bhakti@gmail.com", "phone": 9562518475}
#     # res = client.post('/register' , data=json.dumps(data1))
#     print('=======Response====' , res )
#     yield res

# @pytest.fixture()
# def delete_member(client ):
#     data = {"name": "Bhakti", "email": "Bhakti@gmail.com", "phone": 9562518475}
#     mem = Member.selectBy(name=data['name'] ,email = data['email'],phone=data['phone'])
#     id = list(mem)[0].id
#     mem = Member.get(id)
#     mem.delete(id)
   