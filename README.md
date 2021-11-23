# Aplicación Control de Stock

## Uso

Todas las respuesta tienen la forma:

```json
{
    "mensaje": "Description de lo sucedido",
    "data": "Contenido de la respuesta"
}
```

Por defecto, para los errores `505` y `404`, el campo `data`, devuelve `{}`.

## 2- Retirar cierta cantidad de un producto dado un id de producto, un depósito, una cantidad y una ubicación

`GET /retirar/<string:deposito>/<string:ubicacion>/<int:producto>/<int:cantidad>`

**Respuesta**

- `505 Internal Server Error` Si se produjo un error durante el proceso de consulta a la base de datos.
- `406 Not Acceptable` Si se intentó descontar una cantidad negativa del producto.
- `406 Not Acceptable` Si no hay stock suficiente del producto.
- `404 Not Found` Si el producto no fue encontrado.
- `200 OK` Si el stock fue actualizado.

200 e.g.
`curl localhost:5000/retirar/AR01/AL-04-02-DE/4/1`

```json
{
    "mensaje": "El stock fue actualizado",
    "data": {}
}
```

## 3- Listar todos los productos dado un depósito y una ubicación

**Definición**

`GET /leer/<string:deposito>/<string:ubicacion>`

**Respuesta**

- `505 Internal Server Error` Si se produjo un error durante el proceso de consulta a la base de datos.
- `404 Not Found` Si ningún producto fue encontrado.
- `200 OK` Productos encontrados.

200 e.g.
`curl localhost:5000/leer/AR01/AL-04-02-DE`

```json
{
    "mensaje": "Productos encontrados",
    "data": [
        {
            "ID_PRODUCTO": 1,
            "ID_DEPOSITO": "AR01",
            "AREA": "AL",
            "PASILLO": 4,
            "FILA": 2,
            "CARA": "DE",
            "CANTIDAD": 50
        },
        {
            "ID_PRODUCTO": 2,
            "ID_DEPOSITO": "AR01",
            "AREA": "AL",
            "PASILLO": 4,
            "FILA": 2,
            "CARA": "DE",
            "CANTIDAD": 0
        },
        {
            "ID_PRODUCTO": 4,
            "ID_DEPOSITO": "AR01",
            "AREA": "AL",
            "PASILLO": 4,
            "FILA": 2,
            "CARA": "DE",
            "CANTIDAD": 31
        }
    ]
}
```

## 4- Encontrar ubicaciones y cantidades de un producto dado un deposito y un id de producto

`GET /buscar/<string:deposito>/<int:identifier>`

- `505 Internal Server Error` Si se produjo un error durante el proceso de consulta a la base de datos.
- `404 Not Found` Si el producto no fue encontrado en el deposito.
- `200 OK` Si el producto fue encontrado en el depósito.

200 e.g.
`curl localhost:5000/buscar/AR01/1`

```json
{
    "mensaje": "Productos encontrados",
    "data": [
        {
            "ID_PRODUCTO": 1,
            "ID_DEPOSITO": "AR01",
            "AREA": "AL",
            "PASILLO": 4,
            "FILA": 2,
            "CARA": "DE",
            "CANTIDAD": 50
        },
        {
            "ID_PRODUCTO": 1,
            "ID_DEPOSITO": "AR01",
            "AREA": "AL",
            "PASILLO": 4,
            "FILA": 1,
            "CARA": "IZ",
            "CANTIDAD": 42
        }
    ]
}
```