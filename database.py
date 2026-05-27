import pg8000

def conectar():
    try:
        conexion = pg8000.connect(
            host="localhost",
            database="boutique_db",
            user="postgres",
            password="18402001J@se"
        )

        return conexion

    except Exception as e:
        print("Error al conectar:", e)