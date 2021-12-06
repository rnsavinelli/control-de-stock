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

## 1- Agregar cierta cantidad de un producto dado un id de producto, un depósito, una cantidad y una ubicación

`POST /agregar`

**Parámetros**

- `"producto":int` identificador numérico del producto.
- `"deposito":string` identificador del depósito constando de 4 caracteres, los 2 primeros siendo el código ISO de país y los otros son una secuencia numérica, e.g. AR01.
- `"ubicacion":string` identificador de la ubicación según {Area}-{Pasillo}-{Fila}-{Cara}
con 2 dígitos para cada parte, e.g. AL-04-02-DE.
- `"cantidad":int` cantidad de producto a agregar.

**Respuesta**

- `500 Internal Server Error` Si se produjo un error durante el proceso de consulta a la base de datos.
- `406 Not Acceptable` Si la ubicación no tiene el patrón correcto.
- `406 Not Acceptable` Si el depósito no tiene el patrón correcto.
- `406 Not Acceptable` Si se intentó agregar una cantidad negativa del producto.
- `406 Not Acceptable` Si no hay stock suficiente del producto.
- `404 Not Found` Si el producto no fue encontrado.
- `200 OK` Si el stock fue actualizado.

**Ejemplo 200**

`curl -X POST -F 'producto=2' -F 'deposito=AR01' -F 'ubicacion=AL-04-02-DE' -F 'cantidad=1' localhost:5000/agregar`

```json
{
    "mensaje": "La base de datos fue actualizada",
    "data": {}
}
```

## 2- Retirar cierta cantidad de un producto dado un id de producto, un depósito, una cantidad y una ubicación

`PUT /retirar`

**Respuesta**

- `500 Internal Server Error` Si se produjo un error durante el proceso de consulta a la base de datos.
- `406 Not Acceptable` Si la ubicación no tiene el patrón correcto.
- `406 Not Acceptable` Si el depósito no tiene el patrón correcto.
- `406 Not Acceptable` Si se intentó descontar una cantidad negativa del producto.
- `406 Not Acceptable` Si no hay stock suficiente del producto.
- `404 Not Found` Si el producto no fue encontrado.
- `200 OK` Si el stock fue actualizado.

**Ejemplo 200**

`curl -X PUT -F 'producto=4' -F 'deposito=AR01' -F 'ubicacion=AL-04-02-DE' -F 'cantidad=1' localhost:5000/retirar`

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

- `500 Internal Server Error` Si se produjo un error durante el proceso de consulta a la base de datos.
- `406 Not Acceptable` Si la ubicación no tiene el patrón correcto.
- `406 Not Acceptable` Si el depósito no tiene el patrón correcto.
- `404 Not Found` Si ningún producto fue encontrado.
- `200 OK` Productos encontrados.

**Ejemplo 200**

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

**Respuesta**

- `500 Internal Server Error` Si se produjo un error durante el proceso de consulta a la base de datos.
- `406 Not Acceptable` Si el depósito no tiene el patrón correcto.
- `404 Not Found` Si el producto no fue encontrado en el deposito.
- `200 OK` Si el producto fue encontrado en el depósito.

**Ejemplo 200**

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