from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from resources import Printing

app = Flask(__name__)
CORS(app)
api = Api(app)

api.add_resource(Printing, '/print')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
