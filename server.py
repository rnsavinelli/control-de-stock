from flask import Flask
from flask_restful import Api
from flask_cors import CORS
import markdown

from retirar import Retirar
from productos import Producto, Productos

app = Flask(__name__)
CORS(app)
api = Api(app)


@app.route("/")
def index():
    with open('README.md', 'r') as markdown_file:
        content = markdown_file.read()
        return markdown.markdown(content)


api.add_resource(Producto, '/producto/<string:identifier>')

# 2 - Exponer un endpoint para poder retirar productos de una ubicación.
# Se nos indicará el depósito, producto, cantidad y ubicación de donde sacarla.
api.add_resource(
    Retirar,
    '/retirar/<string:deposito>/<string:ubicacion>/<int:producto>/<int:cantidad>'
)

# 3 - Exponer un endpoint de lectura. Se nos indica un depósito y una ubicación, y este
# liste los productos y cantidad que hay en el mismo.
api.add_resource(Productos, '/productos/<string:deposito>/<string:ubicacion>')

app.run(host='0.0.0.0', port=5000, debug=True)
