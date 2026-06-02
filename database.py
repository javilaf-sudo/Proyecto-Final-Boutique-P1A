import pg8000

def conectar():
    try:
        conexion = pg8000.connect(
            host="localhost",
            database="boutique_db",
            user="postgres",
            password="Hola1234"
        )

        return conexion

    except Exception as e:
        print("Error al conectar:", e)