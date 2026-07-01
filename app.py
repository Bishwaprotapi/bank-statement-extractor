import logging
import sys
from flask import Flask
from flask_cors import CORS
from flasgger import Swagger
from flask import redirect
from src.routes.bank_statement import bank_statement_blueprint


def create_app():
    app = Flask(__name__)  # flask app object
    app.config.from_object('config')  # Configuring from Python Files
    CORS(app)  # Enabling CORS

    logging.basicConfig(filename='app.log', level=logging.DEBUG)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logging.getLogger().addHandler(console_handler)

    app.register_blueprint(bank_statement_blueprint, url_prefix='/api')

    return app


# Creating the app
app = create_app()

swagger = Swagger(app, template_file='apidocs/swagger.yaml')


@app.route('/')
def root():
    return redirect('/apidocs/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
