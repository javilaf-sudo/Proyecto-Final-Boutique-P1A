from database import conectar


def pedir_entero(mensaje):
    while True:
        try:
            numero = int(input(mensaje))
            return numero
        except:
            print("Error: debe ingresar un numero entero.")


def pedir_decimal(mensaje):
    while True:
        try:
            numero = float(input(mensaje))
            return numero
        except:
            print("Error: debe ingresar un numero valido.")


def agregar_producto():
    conexion = conectar()

    if conexion is not None:
        try:
            cursor = conexion.cursor()

            nombre = input("Nombre del producto: ")
            categoria = input("Categoria: ")
            talla = input("Talla: ")
            color = input("Color: ")
            precio = pedir_decimal("Precio: ")
            stock = pedir_entero("Stock: ")

            sql = """
            INSERT INTO productos (nombre, categoria, talla, color, precio, stock)
            VALUES (%s, %s, %s, %s, %s, %s)
            """

            datos = (nombre, categoria, talla, color, precio, stock)
            cursor.execute(sql, datos)
            conexion.commit()

            print("Producto agregado correctamente.")

            cursor.close()
            conexion.close()

        except Exception as e:
            print("Error al agregar producto:", e)


def mostrar_productos():
    conexion = conectar()

    if conexion is not None:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM productos ORDER BY id_producto ASC")
            productos = cursor.fetchall()

            print("\n--- LISTA DE PRODUCTOS ---")

            for producto in productos:
                print("ID:", producto[0], "| Nombre:", producto[1], "| Categoria:", producto[2],
                      "| Talla:", producto[3], "| Color:", producto[4],
                      "| Precio:", producto[5], "| Stock:", producto[6])

            cursor.close()
            conexion.close()

        except Exception as e:
            print("Error al mostrar productos:", e)


def editar_producto():
    conexion = conectar()

    if conexion is not None:
        try:
            cursor = conexion.cursor()

            mostrar_productos()

            id_producto = pedir_entero("Ingrese el ID del producto que desea editar: ")

            nombre = input("Nuevo nombre: ")
            categoria = input("Nueva categoria: ")
            talla = input("Nueva talla: ")
            color = input("Nuevo color: ")
            precio = pedir_decimal("Nuevo precio: ")
            stock = pedir_entero("Nuevo stock: ")

            sql = """
            UPDATE productos
            SET nombre=%s, categoria=%s, talla=%s, color=%s, precio=%s, stock=%s
            WHERE id_producto=%s
            """

            datos = (nombre, categoria, talla, color, precio, stock, id_producto)

            cursor.execute(sql, datos)
            conexion.commit()

            print("Producto actualizado correctamente.")

            cursor.close()
            conexion.close()

        except Exception as e:
            print("Error al editar producto:", e)


def eliminar_producto():
    conexion = conectar()

    if conexion is not None:
        try:
            cursor = conexion.cursor()

            mostrar_productos()

            id_producto = pedir_entero("Ingrese el ID del producto que desea eliminar: ")

            sql = "DELETE FROM productos WHERE id_producto=%s"
            datos = (id_producto,)

            cursor.execute(sql, datos)
            conexion.commit()

            print("Producto eliminado correctamente.")

            cursor.close()
            conexion.close()

        except Exception as e:
            print("Error al eliminar producto:", e)


def registrar_cliente():
    conexion = conectar()

    if conexion is not None:
        try:
            cursor = conexion.cursor()

            nombre = input("Nombre del cliente: ")
            apellido = input("Apellido del cliente: ")
            telefono = input("Telefono: ")
            correo = input("Correo: ")

            sql = """
            INSERT INTO clientes (nombre, apellido, telefono, correo)
            VALUES (%s, %s, %s, %s)
            """

            datos = (nombre, apellido, telefono, correo)

            cursor.execute(sql, datos)
            conexion.commit()

            print("Cliente registrado correctamente.")

            cursor.close()
            conexion.close()

        except Exception as e:
            print("Error al registrar cliente:", e)


def mostrar_clientes():
    conexion = conectar()

    if conexion is not None:
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM clientes ORDER BY id_cliente ASC")
            clientes = cursor.fetchall()

            print("\n--- LISTA DE CLIENTES ---")

            for cliente in clientes:
                print("ID:", cliente[0], "| Nombre:", cliente[1], cliente[2],
                      "| Telefono:", cliente[3], "| Correo:", cliente[4])

            cursor.close()
            conexion.close()

        except Exception as e:
            print("Error al mostrar clientes:", e)


def registrar_venta():
    conexion = conectar()

    if conexion is not None:
        try:
            cursor = conexion.cursor()

            mostrar_clientes()
            id_cliente = pedir_entero("Ingrese el ID del cliente: ")

            mostrar_productos()
            id_producto = pedir_entero("Ingrese el ID del producto vendido: ")
            cantidad = pedir_entero("Ingrese la cantidad vendida: ")

            cursor.execute("SELECT precio, stock FROM productos WHERE id_producto=%s", (id_producto,))
            producto = cursor.fetchone()

            if producto is None:
                print("Producto no encontrado.")
                cursor.close()
                conexion.close()
                return

            precio = float(producto[0])
            stock = int(producto[1])

            if cantidad > stock:
                print("No hay suficiente stock.")
                cursor.close()
                conexion.close()
                return

            subtotal = precio * cantidad

            cursor.execute("INSERT INTO ventas (id_cliente) VALUES (%s) RETURNING id_venta", (id_cliente,))
            id_venta = cursor.fetchone()[0]

            sql_detalle = """
            INSERT INTO detalle_ventas (id_venta, id_producto, cantidad, subtotal)
            VALUES (%s, %s, %s, %s)
            """

            cursor.execute(sql_detalle, (id_venta, id_producto, cantidad, subtotal))

            nuevo_stock = stock - cantidad

            cursor.execute(
                "UPDATE productos SET stock=%s WHERE id_producto=%s",
                (nuevo_stock, id_producto)
            )

            conexion.commit()

            print("Venta registrada correctamente.")
            print("Total de la venta: Q", subtotal)

            cursor.close()
            conexion.close()

        except Exception as e:
            print("Error al registrar venta:", e)


def menu():
    opcion = 0

    while opcion != 8:
        print("\nSISTEMA DE VENTAS BOUTIQUE UMG")
        print("1. Agregar producto")
        print("2. Mostrar productos")
        print("3. Editar producto")
        print("4. Eliminar producto")
        print("5. Registrar cliente")
        print("6. Mostrar clientes")
        print("7. Registrar venta")
        print("8. Salir")

        opcion = pedir_entero("Seleccione una opcion: ")

        if opcion == 1:
            agregar_producto()
        elif opcion == 2:
            mostrar_productos()
        elif opcion == 3:
            editar_producto()
        elif opcion == 4:
            eliminar_producto()
        elif opcion == 5:
            registrar_cliente()
        elif opcion == 6:
            mostrar_clientes()
        elif opcion == 7:
            registrar_venta()
        elif opcion == 8:
            print("Saliendo del sistema...")
        else:
            print("Opcion incorrecta.")


menu()