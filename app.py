import tkinter as tk
from tkinter import messagebox, ttk

from database import conectar


COLOR_FONDO = "#f8d7da"
COLOR_TITULO = "#7b2d26"
COLOR_BOTON = "#ffcad4"
COLOR_SALIR = "#ff8fab"


def limpiar_ventana():
    for widget in ventana.winfo_children():
        widget.destroy()


def crear_boton(texto, comando, color=COLOR_BOTON, texto_color=COLOR_TITULO):
    return tk.Button(
        ventana,
        text=texto,
        width=25,
        height=2,
        bg=color,
        fg=texto_color,
        font=("Arial", 10, "bold"),
        activebackground="#ffb3c1",
        command=comando,
    )


def crear_titulo(texto):
    tk.Label(
        ventana,
        text=texto,
        font=("Arial", 22, "bold"),
        bg=COLOR_FONDO,
        fg=COLOR_TITULO,
    ).pack(pady=15)


def crear_entrada(texto, contenedor=None, ancho=30):
    contenedor = contenedor or ventana
    tk.Label(contenedor, text=texto, bg=COLOR_FONDO, fg=COLOR_TITULO).pack()
    entrada = tk.Entry(contenedor, width=ancho)
    entrada.pack(pady=3)
    return entrada


def crear_formulario(campos):
    return {campo: crear_entrada(campo) for campo in campos}


def crear_tabla(contenedor, columnas, anchos, alto=8):
    tabla = ttk.Treeview(contenedor, columns=columnas, show="headings", height=alto)
    for columna in columnas:
        tabla.heading(columna, text=columna)
        tabla.column(columna, width=anchos.get(columna, 100))
    return tabla


def limpiar_campos(*entradas):
    for entrada in entradas:
        entrada.delete(0, tk.END)


def ejecutar_consulta(sql, datos=None, retornar=False):
    conexion = conectar()
    cursor = conexion.cursor()
    try:
        cursor.execute(sql, datos) if datos is not None else cursor.execute(sql)
        if retornar:
            return cursor.fetchall()
        conexion.commit()
    finally:
        cursor.close()
        conexion.close()


def cargar_tabla(tabla, consulta):
    tabla.delete(*tabla.get_children())
    for fila in ejecutar_consulta(consulta, retornar=True):
        tabla.insert("", tk.END, values=fila)


def copiar_id(tabla, entrada):
    seleccion = tabla.selection()
    if seleccion:
        entrada.delete(0, tk.END)
        entrada.insert(0, tabla.item(seleccion[0], "values")[0])


def menu_principal():
    limpiar_ventana()
    ventana.configure(bg=COLOR_FONDO)

    tk.Label(
        ventana,
        text="SISTEMA DE VENTAS BOUTIQUE",
        font=("Arial", 24, "bold"),
        bg=COLOR_FONDO,
        fg=COLOR_TITULO,
    ).pack(pady=40)

    for texto, comando, color, texto_color in (
        ("Productos", ventana_productos, COLOR_BOTON, COLOR_TITULO),
        ("Clientes", ventana_clientes, COLOR_BOTON, COLOR_TITULO),
        ("Ventas", ventana_ventas, COLOR_BOTON, COLOR_TITULO),
        ("Salir", ventana.destroy, COLOR_SALIR, "white"),
    ):
        crear_boton(texto, comando, color, texto_color).pack(pady=10)


def ventana_productos():
    limpiar_ventana()
    ventana.configure(bg=COLOR_FONDO)
    crear_titulo("GESTIÓN DE PRODUCTOS")

    entrada_id = crear_entrada("ID para editar/eliminar")
    entradas = crear_formulario(["Nombre", "Categoría", "Talla", "Color", "Precio", "Stock"])

    columnas = ("ID", "Nombre", "Categoria", "Talla", "Color", "Precio", "Stock")
    anchos = {"ID": 50, "Nombre": 150, "Categoria": 120, "Talla": 70, "Color": 100, "Precio": 100, "Stock": 80}
    tabla = crear_tabla(ventana, columnas, anchos)
    tabla.pack(pady=15)

    def limpiar():
        limpiar_campos(entrada_id, *entradas.values())

    def mostrar():
        cargar_tabla(tabla, "SELECT * FROM productos ORDER BY id_producto ASC")

    def datos_producto(incluir_id=False):
        datos = (
            entradas["Nombre"].get(),
            entradas["Categoría"].get(),
            entradas["Talla"].get(),
            entradas["Color"].get(),
            float(entradas["Precio"].get()),
            int(entradas["Stock"].get()),
        )
        return datos + (int(entrada_id.get()),) if incluir_id else datos

    def guardar():
        try:
            ejecutar_consulta(
                """
                INSERT INTO productos (nombre, categoria, talla, color, precio, stock)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                datos_producto(),
            )
            messagebox.showinfo("Éxito", "Producto guardado correctamente")
            limpiar()
            mostrar()
        except Exception:
            messagebox.showerror("Error", "Revise los datos del producto")

    def editar():
        try:
            ejecutar_consulta(
                """
                UPDATE productos
                SET nombre=%s, categoria=%s, talla=%s, color=%s, precio=%s, stock=%s
                WHERE id_producto=%s
                """,
                datos_producto(incluir_id=True),
            )
            messagebox.showinfo("Éxito", "Producto editado correctamente")
            limpiar()
            mostrar()
        except Exception:
            messagebox.showerror("Error", "No se pudo editar el producto")

    def eliminar():
        try:
            ejecutar_consulta("DELETE FROM productos WHERE id_producto=%s", (int(entrada_id.get()),))
            messagebox.showinfo("Éxito", "Producto eliminado correctamente")
            limpiar()
            mostrar()
        except Exception:
            messagebox.showerror("Error", "No se puede eliminar. Puede estar relacionado con una venta.")

    for texto, comando, color, texto_color in (
        ("Guardar Producto", guardar, COLOR_BOTON, COLOR_TITULO),
        ("Editar Producto", editar, COLOR_BOTON, COLOR_TITULO),
        ("Eliminar Producto", eliminar, COLOR_BOTON, COLOR_TITULO),
        ("Regresar", menu_principal, COLOR_SALIR, "white"),
    ):
        crear_boton(texto, comando, color, texto_color).pack(pady=3)

    mostrar()


def ventana_clientes():
    limpiar_ventana()
    ventana.configure(bg=COLOR_FONDO)
    crear_titulo("GESTIÓN DE CLIENTES")

    entrada_id = crear_entrada("ID para editar/eliminar")
    entradas = crear_formulario(["Nombre", "Apellido", "Teléfono", "Correo"])

    columnas = ("ID", "Nombre", "Apellido", "Telefono", "Correo")
    anchos = {"ID": 50, "Nombre": 140, "Apellido": 140, "Telefono": 120, "Correo": 220}
    tabla = crear_tabla(ventana, columnas, anchos)
    tabla.pack(pady=15)

    def limpiar():
        limpiar_campos(entrada_id, *entradas.values())

    def mostrar():
        cargar_tabla(tabla, "SELECT * FROM clientes ORDER BY id_cliente ASC")

    def datos_cliente(incluir_id=False):
        datos = (
            entradas["Nombre"].get(),
            entradas["Apellido"].get(),
            entradas["Teléfono"].get(),
            entradas["Correo"].get(),
        )
        return datos + (int(entrada_id.get()),) if incluir_id else datos

    def guardar():
        try:
            ejecutar_consulta(
                """
                INSERT INTO clientes (nombre, apellido, telefono, correo)
                VALUES (%s, %s, %s, %s)
                """,
                datos_cliente(),
            )
            messagebox.showinfo("Éxito", "Cliente guardado correctamente")
            limpiar()
            mostrar()
        except Exception:
            messagebox.showerror("Error", "No se pudo guardar el cliente")

    def editar():
        try:
            ejecutar_consulta(
                """
                UPDATE clientes
                SET nombre=%s, apellido=%s, telefono=%s, correo=%s
                WHERE id_cliente=%s
                """,
                datos_cliente(incluir_id=True),
            )
            messagebox.showinfo("Éxito", "Cliente editado correctamente")
            limpiar()
            mostrar()
        except Exception:
            messagebox.showerror("Error", "No se pudo editar el cliente")

    def eliminar():
        try:
            ejecutar_consulta("DELETE FROM clientes WHERE id_cliente=%s", (int(entrada_id.get()),))
            messagebox.showinfo("Éxito", "Cliente eliminado correctamente")
            limpiar()
            mostrar()
        except Exception:
            messagebox.showerror("Error", "No se puede eliminar. Puede estar relacionado con una venta.")

    for texto, comando, color, texto_color in (
        ("Guardar Cliente", guardar, COLOR_BOTON, COLOR_TITULO),
        ("Editar Cliente", editar, COLOR_BOTON, COLOR_TITULO),
        ("Eliminar Cliente", eliminar, COLOR_BOTON, COLOR_TITULO),
        ("Regresar", menu_principal, COLOR_SALIR, "white"),
    ):
        crear_boton(texto, comando, color, texto_color).pack(pady=3)

    mostrar()


def ventana_ventas():
    limpiar_ventana()
    ventana.configure(bg=COLOR_FONDO)
    crear_titulo("REGISTRAR VENTA")

    frame_arriba = tk.Frame(ventana, bg=COLOR_FONDO)
    frame_arriba.pack()

    entradas = {}
    for columna, campo in enumerate(("ID Cliente", "ID Producto", "Cantidad")):
        tk.Label(frame_arriba, text=campo, bg=COLOR_FONDO, fg=COLOR_TITULO).grid(row=0, column=columna, padx=10)
        entradas[campo] = tk.Entry(frame_arriba, width=20)
        entradas[campo].grid(row=1, column=columna, padx=10)

    frame_tablas = tk.Frame(ventana, bg=COLOR_FONDO)
    frame_tablas.pack(pady=15)

    tk.Label(frame_tablas, text="PRODUCTOS", bg=COLOR_FONDO, fg=COLOR_TITULO, font=("Arial", 12, "bold")).grid(row=0, column=0)
    tabla_productos = crear_tabla(frame_tablas, ("ID", "Nombre", "Precio", "Stock"), {"ID": 50, "Nombre": 150, "Precio": 90, "Stock": 70})
    tabla_productos.grid(row=1, column=0, padx=15)

    tk.Label(frame_tablas, text="CLIENTES", bg=COLOR_FONDO, fg=COLOR_TITULO, font=("Arial", 12, "bold")).grid(row=0, column=1)
    tabla_clientes = crear_tabla(frame_tablas, ("ID", "Nombre", "Apellido"), {"ID": 50, "Nombre": 150, "Apellido": 150})
    tabla_clientes.grid(row=1, column=1, padx=15)

    tk.Label(
        ventana,
        text="HISTORIAL DE VENTAS",
        bg=COLOR_FONDO,
        fg=COLOR_TITULO,
        font=("Arial", 12, "bold"),
    ).pack(pady=5)

    columnas_ventas = ("Venta", "Cliente", "Producto", "Cantidad", "Total", "Fecha")
    tabla_ventas = crear_tabla(
        ventana,
        columnas_ventas,
        {"Venta": 70, "Cliente": 140, "Producto": 140, "Cantidad": 90, "Total": 100, "Fecha": 160},
        alto=6,
    )
    tabla_ventas.pack(pady=10)

    def mostrar_productos():
        cargar_tabla(tabla_productos, "SELECT id_producto, nombre, precio, stock FROM productos ORDER BY id_producto ASC")

    def mostrar_clientes():
        cargar_tabla(tabla_clientes, "SELECT id_cliente, nombre, apellido FROM clientes ORDER BY id_cliente ASC")

    def mostrar_ventas():
        cargar_tabla(
            tabla_ventas,
            """
            SELECT ventas.id_venta, clientes.nombre, productos.nombre,
                   detalle_ventas.cantidad, detalle_ventas.subtotal, ventas.fecha
            FROM detalle_ventas
            INNER JOIN ventas ON detalle_ventas.id_venta = ventas.id_venta
            INNER JOIN clientes ON ventas.id_cliente = clientes.id_cliente
            INNER JOIN productos ON detalle_ventas.id_producto = productos.id_producto
            ORDER BY ventas.id_venta ASC
            """,
        )

    tabla_productos.bind("<<TreeviewSelect>>", lambda _e: copiar_id(tabla_productos, entradas["ID Producto"]))
    tabla_clientes.bind("<<TreeviewSelect>>", lambda _e: copiar_id(tabla_clientes, entradas["ID Cliente"]))

    def registrar():
        try:
            producto_id = int(entradas["ID Producto"].get().strip())
            cliente_id = int(entradas["ID Cliente"].get().strip())
            cantidad = int(entradas["Cantidad"].get().strip())

            if cantidad <= 0:
                messagebox.showerror("Error", "La cantidad debe ser mayor que cero")
                return

            producto = ejecutar_consulta(
                "SELECT precio, stock FROM productos WHERE id_producto=%s",
                (producto_id,),
                retornar=True,
            )

            if not producto:
                messagebox.showerror("Error", "Producto no encontrado. Selecciona un producto de la tabla.")
                return

            cliente = ejecutar_consulta("SELECT 1 FROM clientes WHERE id_cliente=%s", (cliente_id,), retornar=True)
            if not cliente:
                messagebox.showerror("Error", "Cliente no encontrado. Selecciona un cliente de la tabla.")
                return

            precio, stock = float(producto[0][0]), int(producto[0][1])
            if cantidad > stock:
                messagebox.showerror("Error", "No hay suficiente stock")
                return

            subtotal = precio * cantidad
            conexion = conectar()
            cursor = conexion.cursor()
            try:
                cursor.execute("INSERT INTO ventas (id_cliente) VALUES (%s) RETURNING id_venta", (cliente_id,))
                venta_id = cursor.fetchone()[0]
                cursor.execute(
                    """
                    INSERT INTO detalle_ventas (id_venta, id_producto, cantidad, subtotal)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (venta_id, producto_id, cantidad, subtotal),
                )
                cursor.execute("UPDATE productos SET stock=%s WHERE id_producto=%s", (stock - cantidad, producto_id))
                conexion.commit()
            finally:
                cursor.close()
                conexion.close()

            messagebox.showinfo("Éxito", "Venta registrada. Total Q" + str(subtotal))
            limpiar_campos(*entradas.values())
            mostrar_productos()
            mostrar_clientes()
            mostrar_ventas()

        except ValueError:
            messagebox.showerror("Error", "ID Cliente, ID Producto y Cantidad deben ser numeros enteros.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar la venta:\n{e}")

    crear_boton("Registrar Venta", registrar).pack(pady=3)
    crear_boton("Regresar", menu_principal, COLOR_SALIR, "white").pack(pady=8)

    mostrar_productos()
    mostrar_clientes()
    mostrar_ventas()


ventana = tk.Tk()
ventana.title("Sistema de Ventas Boutique")
ventana.geometry("1000x760")

menu_principal()
ventana.mainloop()
