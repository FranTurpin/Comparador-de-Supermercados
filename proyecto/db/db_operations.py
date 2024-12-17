import asyncio
from database import connect_db

async def fetch_data(query, *args):
    """
    Ejecuta una consulta SELECT en la base de datos y devuelve los resultados.
    """
    connection = await connect_db()
    if connection:
        try:
            result = await connection.fetch(query, *args)
            await connection.close()
            return result
        except Exception as e:
            print(f"Error en fetch_data: {e}")
            await connection.close()
    return []

async def execute_query(query, *args):
    """
    Ejecuta una consulta INSERT, UPDATE o DELETE en la base de datos.
    """
    connection = await connect_db()
    if connection:
        try:
            await connection.execute(query, *args)
            await connection.close()
            return True
        except Exception as e:
            print(f"Error en execute_query: {e}")
            await connection.close()
    return False

def obtener_productos():
    """
    Obtiene la lista de productos únicos disponibles en la base de datos.
    Devuelve una lista de diccionarios con 'nombre'.
    """
    query = "SELECT DISTINCT nombre FROM productos"
    async def query_func():
        return await fetch_data(query)

    result = asyncio.run(query_func())
    return [{"nombre": row["nombre"]} for row in result]

def obtener_precios_productos_por_supermercado():
    """
    Devuelve un diccionario con los precios de productos por supermercado.
    Estructura: { 'Supermercado1': {'Producto1': Precio1, 'Producto2': Precio2}, ... }
    """
    query = """
    SELECT s.nombre AS supermercado, p.nombre AS producto, p.precio
    FROM productos p
    JOIN supermercados s ON p.supermercados_id = s.id
    """
    async def query_func():
        return await fetch_data(query)

    result = asyncio.run(query_func())

    precios_por_supermercado = {}
    for row in result:
        supermercado = row["supermercado"]
        producto = row["producto"]
        precio = row["precio"]

        if supermercado not in precios_por_supermercado:
            precios_por_supermercado[supermercado] = {}
        precios_por_supermercado[supermercado][producto] = precio

    return precios_por_supermercado

def eliminar_producto(nombre):
    """
    Elimina un producto de la base de datos por su nombre.
    """
    query = "DELETE FROM productos WHERE nombre = $1"
    async def query_func():
        return await execute_query(query, nombre)

    return asyncio.run(query_func())

def add_product(nombre, precio, supermercado_id):
    """
    Añade un nuevo producto a la base de datos.
    """
    query = """
    INSERT INTO productos (nombre, precio, supermercados_id) 
    VALUES ($1, $2, $3)
    """
    async def query_func():
        return await execute_query(query, nombre, float(precio), int(supermercado_id))

    return asyncio.run(query_func())

def add_supermercado(nombre):
    """
    Añade un nuevo supermercado a la base de datos.
    """
    query = "INSERT INTO supermercados (nombre) VALUES ($1)"
    async def query_func():
        return await execute_query(query, nombre)

    return asyncio.run(query_func())

def obtener_supermercados():
    """
    Obtiene la lista de supermercados disponibles en la base de datos.
    Devuelve una lista de diccionarios con 'id' y 'nombre'.
    """
    query = "SELECT id, nombre FROM supermercados"
    async def query_func():
        return await fetch_data(query)

    result = asyncio.run(query_func())
    return [{"id": row["id"], "nombre": row["nombre"]} for row in result]

def eliminar_supermercado(nombre):
    """
    Elimina un supermercado de la base de datos por su nombre.
    Si el supermercado tiene productos asociados, se eliminan primero los productos.
    """
    async def query_func():
        connection = await connect_db()
        if connection:
            try:
                # Eliminar productos asociados
                await connection.execute(
                    "DELETE FROM productos WHERE supermercados_id IN "
                    "(SELECT id FROM supermercados WHERE nombre = $1)", nombre
                )
                # Eliminar el supermercado
                result = await connection.execute(
                    "DELETE FROM supermercados WHERE nombre = $1", nombre
                )
                await connection.close()
                return result
            except Exception as e:
                print(f"Error al eliminar supermercado: {e}")
                await connection.close()
                return None

    return asyncio.run(query_func())

def obtener_productos_con_supermercado():
    """
    Obtiene la lista de productos con los nombres de supermercados asociados.
    Devuelve una lista de diccionarios con 'producto', 'supermercado' y 'precio'.
    """
    query = """
    SELECT p.nombre AS producto, s.nombre AS supermercado, p.precio
    FROM productos p
    JOIN supermercados s ON p.supermercados_id = s.id
    """
    async def query_func():
        return await fetch_data(query)

    result = asyncio.run(query_func())
    return [{"producto": row["producto"], "supermercado": row["supermercado"], "precio": row["precio"]} for row in result]
