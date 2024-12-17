import asyncpg

async def connect_db():
    """
    Conectar a la base de datos PostgreSQL.
    Ajusta los parámetros (usuario, contraseña, base de datos, host y puerto).
    """
    try:
        connection = await asyncpg.connect(
            user="postgres",
            password="1234",
            database="comparador_db",
            host="localhost",
            port=5432
        )
        return connection
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
