import os
import markdown

from server.core import app, api

from server.routes.buscar import Buscar
from server.routes.agregar import Agregar
from server.routes.retirar import Retirar
from server.routes.productos import Productos


@app.route("/")
def index():
    with open(os.path.dirname(app.root_path) + "/README.md", "r") as markdown_file:
        content = markdown_file.read()
        return markdown.markdown(content)


# 1 - Exponer un endpoint REST para agregar productos en una ubicación.
#   a. Se nos indicará el Depósito, producto, cantidad y ubicación donde quiere colocar.
#   b. Validar que la dirección tenga el patrón correcto.
#   c. Que el producto/item sea almacenado en nuestros depósitos.
#   d. No se pueden colocar más de 3 productos distintos en una ubicación.
#   e. La suma de las cantidades de los productos que hubiera en una ubicación no puede ser mayor a 100 unidades.
# e.g. curl -X POST -F 'producto=4' -F 'deposito=AR01' -F 'ubicacion=AL-04-02-DE' -F 'cantidad=0' localhost:5000/agregar
api.add_resource(
    Agregar,
    "/agregar",
)

# 2 - Exponer un endpoint para poder retirar productos de una ubicación.
# Se nos indicará el depósito, producto, cantidad y ubicación de donde sacarla.
# e.g. curl localhost:5000/retirar/AR01/AL-04-02-DE/2/7
api.add_resource(
    Retirar,
    "/retirar/<string:deposito>/<string:ubicacion>/<int:producto>/<int:cantidad>",
)

# 3 - Exponer un endpoint de lectura. Se nos indica un depósito y una ubicación, y este
# liste los productos y cantidad que hay en el mismo.
# e.g. curl localhost:5000/productos/AR01/AL-04-02-DE
api.add_resource(Productos, "/productos/<string:deposito>/<string:ubicacion>")

# 4 - Exponer un endpoint de búsqueda. Se nos indica el depósito y producto, y este nos
# devuelva las posibles ubicaciones y cantidad en las mismas.
# e.g. curl localhost:5000/buscar/AR01/1
api.add_resource(Buscar, "/buscar/<string:deposito>/<int:identifier>")
