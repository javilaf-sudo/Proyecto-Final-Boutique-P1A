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
        command=comando
    )


def crear_titulo(texto):
    tk.Label(
        ventana,
        text=texto,
        font=("Arial", 22, "bold"),
        bg=COLOR_FONDO,
        fg=COLOR_TITULO
    ).pack(pady=15)


def ejecutar_consulta(sql, datos=None, retornar=False):
    conexion = conectar()
    cursor = conexion.cursor()

    if datos:
        cursor.execute(sql, datos)
    else:
        cursor.execute(sql)

    if retornar:
        resultado = cursor.fetchall()
        conexion.close()
        return resultado

    conexion.commit()
    conexion.close()


def menu_principal():
    limpiar_ventana()
    ventana.configure(bg=COLOR_FONDO)

    tk.Label(
        ventana,
        text="SISTEMA DE VENTAS BOUTIQUE",
        font=("Arial", 24, "bold"),
        bg=COLOR_FONDO,
        fg=COLOR_TITULO
    ).pack(pady=40)

    crear_boton("Productos", ventana_productos).pack(pady=10)
    crear_boton("Clientes", ventana_clientes).pack(pady=10)
    crear_boton("Ventas", ventana_ventas).pack(pady=10)
    crear_boton("Salir", ventana.destroy, COLOR_SALIR, "white").pack(pady=10)


def ventana_productos():
    limpiar_ventana()
    ventana.configure(bg=COLOR_FONDO)
    crear_titulo("GESTIÓN DE PRODUCTOS")
    tk.Label(ventana, text="ID para editar/eliminar", bg=COLOR_FONDO, fg=COLOR_TITULO).pack()
    entrada_id = tk.Entry(ventana, width=30)
    entrada_id.pack(pady=3)

    campos = ["Nombre", "Categoría", "Talla", "Color", "Precio", "Stock"]
    entradas = {}

    for campo in campos:
        tk.Label(ventana, text=campo, bg=COLOR_FONDO, fg=COLOR_TITULO).pack()
        entrada = tk.Entry(ventana, width=30)
        entrada.pack(pady=3)
        entradas[campo] = entrada

    tabla = ttk.Treeview(
        ventana,
        columns=("ID", "Nombre", "Categoria", "Talla", "Color", "Precio", "Stock"),
        show="headings",
        height=8
    )

    for col in ("ID", "Nombre", "Categoria", "Talla", "Color", "Precio", "Stock"):
        tabla.heading(col, text=col)

    tabla.column("ID", width=50)
    tabla.column("Nombre", width=150)
    tabla.column("Categoria", width=120)
    tabla.column("Talla", width=70)
    tabla.column("Color", width=100)
    tabla.column("Precio", width=100)
    tabla.column("Stock", width=80)
    tabla.pack(pady=15)

    def limpiar():
        entrada_id.delete(0, tk.END)
        for entrada in entradas.values():
            entrada.delete(0, tk.END)

    def mostrar():
        tabla.delete(*tabla.get_children())
        productos = ejecutar_consulta(
            "SELECT * FROM productos ORDER BY id_producto ASC",
            retornar=True
        )

        for producto in productos:
            tabla.insert("", tk.END, values=producto)

    def guardar():
        try:
            datos = (
                entradas["Nombre"].get(),
                entradas["Categoría"].get(),
                entradas["Talla"].get(),
                entradas["Color"].get(),
                float(entradas["Precio"].get()),
                int(entradas["Stock"].get())
            )

            ejecutar_consulta(
                """
                INSERT INTO productos (nombre, categoria, talla, color, precio, stock)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                datos
            )

            messagebox.showinfo("Éxito", "Producto guardado correctamente")
            limpiar()
            mostrar()

        except:
            messagebox.showerror("Error", "Revise los datos del producto")

    def editar():
        try:
            datos = (
                entradas["Nombre"].get(),
                entradas["Categoría"].get(),
                entradas["Talla"].get(),
                entradas["Color"].get(),
                float(entradas["Precio"].get()),
                int(entradas["Stock"].get()),
                int(entrada_id.get())
            )

            ejecutar_consulta(
                """
                UPDATE productos
                SET nombre=%s, categoria=%s, talla=%s, color=%s, precio=%s, stock=%s
                WHERE id_producto=%s
                """,
                datos
            )

            messagebox.showinfo("Éxito", "Producto editado correctamente")
            limpiar()
            mostrar()

        except:
            messagebox.showerror("Error", "No se pudo editar el producto")

    def eliminar():
        try:
            ejecutar_consulta(
                "DELETE FROM productos WHERE id_producto=%s",
                (int(entrada_id.get()),)
            )

            messagebox.showinfo("Éxito", "Producto eliminado correctamente")
            limpiar()
            mostrar()

        except:
            messagebox.showerror("Error", "No se puede eliminar. Puede estar relacionado con una venta.")

    crear_boton("Guardar Producto", guardar).pack(pady=3)
    crear_boton("Editar Producto", editar).pack(pady=3)
    crear_boton("Eliminar Producto", eliminar).pack(pady=3)
    crear_boton("Regresar", menu_principal, COLOR_SALIR, "white").pack(pady=3)

    mostrar()


def ventana_clientes():
    limpiar_ventana()
    ventana.configure(bg=COLOR_FONDO)
    crear_titulo("GESTIÓN DE CLIENTES")

    tk.Label(ventana, text="ID para editar/eliminar", bg=COLOR_FONDO, fg=COLOR_TITULO).pack()
    entrada_id = tk.Entry(ventana, width=30)
    entrada_id.pack(pady=3)

    campos = ["Nombre", "Apellido", "Teléfono", "Correo"]
    entradas = {}

    for campo in campos:
        tk.Label(ventana, text=campo, bg=COLOR_FONDO, fg=COLOR_TITULO).pack()
        entrada = tk.Entry(ventana, width=30)
        entrada.pack(pady=3)
        entradas[campo] = entrada

    tabla = ttk.Treeview(
        ventana,
        columns=("ID", "Nombre", "Apellido", "Telefono", "Correo"),
        show="headings",
        height=8
    )

    for col in ("ID", "Nombre", "Apellido", "Telefono", "Correo"):
        tabla.heading(col, text=col)

    tabla.column("ID", width=50)
    tabla.column("Nombre", width=140)
    tabla.column("Apellido", width=140)
    tabla.column("Telefono", width=120)
    tabla.column("Correo", width=220)
    tabla.pack(pady=15)

    def limpiar():
        entrada_id.delete(0, tk.END)
        for entrada in entradas.values():
            entrada.delete(0, tk.END)

    def mostrar():
        tabla.delete(*tabla.get_children())
        clientes = ejecutar_consulta(
            "SELECT * FROM clientes ORDER BY id_cliente ASC",
            retornar=True
        )

        for cliente in clientes:
            tabla.insert("", tk.END, values=cliente)

    def guardar():
        try:
            datos = (
                entradas["Nombre"].get(),
                entradas["Apellido"].get(),
                entradas["Teléfono"].get(),
                entradas["Correo"].get()
            )

            ejecutar_consulta(
                """
                INSERT INTO clientes (nombre, apellido, telefono, correo)
                VALUES (%s, %s, %s, %s)
                """,
                datos
            )

            messagebox.showinfo("Éxito", "Cliente guardado correctamente")
            limpiar()
            mostrar()

        except:
            messagebox.showerror("Error", "No se pudo guardar el cliente")

    def editar():
        try:
            datos = (
                entradas["Nombre"].get(),
                entradas["Apellido"].get(),
                entradas["Teléfono"].get(),
                entradas["Correo"].get(),
                int(entrada_id.get())
            )

            ejecutar_consulta(
                """
                UPDATE clientes
                SET nombre=%s, apellido=%s, telefono=%s, correo=%s
                WHERE id_cliente=%s
                """,
                datos
            )

            messagebox.showinfo("Éxito", "Cliente editado correctamente")
            limpiar()
            mostrar()

        except:
            messagebox.showerror("Error", "No se pudo editar el cliente")

    def eliminar():
        try:
            ejecutar_consulta(
                "DELETE FROM clientes WHERE id_cliente=%s",
                (int(entrada_id.get()),)
            )

            messagebox.showinfo("Éxito", "Cliente eliminado correctamente")
            limpiar()
            mostrar()

        except:
            messagebox.showerror("Error", "No se puede eliminar. Puede estar relacionado con una venta.")

    crear_boton("Guardar Cliente", guardar).pack(pady=3)
    crear_boton("Mostrar Clientes", mostrar).pack(pady=3)
    crear_boton("Editar Cliente", editar).pack(pady=3)
    crear_boton("Eliminar Cliente", eliminar).pack(pady=3)
    crear_boton("Regresar", menu_principal, COLOR_SALIR, "white").pack(pady=10)

    mostrar()


def ventana_ventas():
    limpiar_ventana()
    ventana.configure(bg=COLOR_FONDO)
    crear_titulo("REGISTRAR VENTA")

    frame_arriba = tk.Frame(ventana, bg=COLOR_FONDO)
    frame_arriba.pack()

    tk.Label(frame_arriba, text="ID Cliente", bg=COLOR_FONDO, fg=COLOR_TITULO).grid(row=0, column=0, padx=10)
    id_cliente = tk.Entry(frame_arriba, width=20)
    id_cliente.grid(row=1, column=0, padx=10)

    tk.Label(frame_arriba, text="ID Producto", bg=COLOR_FONDO, fg=COLOR_TITULO).grid(row=0, column=1, padx=10)
    id_producto = tk.Entry(frame_arriba, width=20)
    id_producto.grid(row=1, column=1, padx=10)

    tk.Label(frame_arriba, text="Cantidad", bg=COLOR_FONDO, fg=COLOR_TITULO).grid(row=0, column=2, padx=10)
    cantidad = tk.Entry(frame_arriba, width=20)
    cantidad.grid(row=1, column=2, padx=10)

    frame_tablas = tk.Frame(ventana, bg=COLOR_FONDO)
    frame_tablas.pack(pady=15)

    tk.Label(frame_tablas, text="PRODUCTOS", bg=COLOR_FONDO, fg=COLOR_TITULO, font=("Arial", 12, "bold")).grid(row=0, column=0)
    tabla_productos = ttk.Treeview(frame_tablas, columns=("ID", "Nombre", "Precio", "Stock"), show="headings", height=8)

    for col in ("ID", "Nombre", "Precio", "Stock"):
        tabla_productos.heading(col, text=col)

    tabla_productos.column("ID", width=50)
    tabla_productos.column("Nombre", width=150)
    tabla_productos.column("Precio", width=90)
    tabla_productos.column("Stock", width=70)
    tabla_productos.grid(row=1, column=0, padx=15)

    tk.Label(frame_tablas, text="CLIENTES", bg=COLOR_FONDO, fg=COLOR_TITULO, font=("Arial", 12, "bold")).grid(row=0, column=1)
    tabla_clientes = ttk.Treeview(frame_tablas, columns=("ID", "Nombre", "Apellido"), show="headings", height=8)

    for col in ("ID", "Nombre", "Apellido"):
        tabla_clientes.heading(col, text=col)

    tabla_clientes.column("ID", width=50)
    tabla_clientes.column("Nombre", width=150)
    tabla_clientes.column("Apellido", width=150)
    tabla_clientes.grid(row=1, column=1, padx=15)

    tk.Label(
        ventana,
        text="HISTORIAL DE VENTAS",
        bg=COLOR_FONDO,
        fg=COLOR_TITULO,
        font=("Arial", 12, "bold")
    ).pack(pady=5)

    tabla_ventas = ttk.Treeview(
        ventana,
        columns=("Venta", "Cliente", "Producto", "Cantidad", "Total", "Fecha"),
        show="headings",
        height=6
    )

    for col in ("Venta", "Cliente", "Producto", "Cantidad", "Total", "Fecha"):
        tabla_ventas.heading(col, text=col)

    tabla_ventas.column("Venta", width=70)
    tabla_ventas.column("Cliente", width=140)
    tabla_ventas.column("Producto", width=140)
    tabla_ventas.column("Cantidad", width=90)
    tabla_ventas.column("Total", width=100)
    tabla_ventas.column("Fecha", width=160)
    tabla_ventas.pack(pady=10)

    def mostrar_productos():
        tabla_productos.delete(*tabla_productos.get_children())
        productos = ejecutar_consulta(
            "SELECT id_producto, nombre, precio, stock FROM productos ORDER BY id_producto ASC",
            retornar=True
        )

        for producto in productos:
            tabla_productos.insert("", tk.END, values=producto)

    def mostrar_clientes():
        tabla_clientes.delete(*tabla_clientes.get_children())
        clientes = ejecutar_consulta(
            "SELECT id_cliente, nombre, apellido FROM clientes ORDER BY id_cliente ASC",
            retornar=True
        )

        for cliente in clientes:
            tabla_clientes.insert("", tk.END, values=cliente)

    def mostrar_ventas():
        tabla_ventas.delete(*tabla_ventas.get_children())
        ventas = ejecutar_consulta(
            """
            SELECT ventas.id_venta, clientes.nombre, productos.nombre,
                   detalle_ventas.cantidad, detalle_ventas.subtotal, ventas.fecha
            FROM detalle_ventas
            INNER JOIN ventas ON detalle_ventas.id_venta = ventas.id_venta
            INNER JOIN clientes ON ventas.id_cliente = clientes.id_cliente
            INNER JOIN productos ON detalle_ventas.id_producto = productos.id_producto
            ORDER BY ventas.id_venta ASC
            """,
            retornar=True
        )

        for venta in ventas:
            tabla_ventas.insert("", tk.END, values=venta)

    def registrar():
        try:
            producto_id = int(id_producto.get())
            cliente_id = int(id_cliente.get())
            cant = int(cantidad.get())

            producto = ejecutar_consulta(
                "SELECT precio, stock FROM productos WHERE id_producto=%s",
                (producto_id,),
                retornar=True
            )

            if len(producto) == 0:
                messagebox.showerror("Error", "Producto no encontrado")
                return

            precio = float(producto[0][0])
            stock = int(producto[0][1])

            if cant > stock:
                messagebox.showerror("Error", "No hay suficiente stock")
                return

            subtotal = precio * cant

            conexion = conectar()
            cursor = conexion.cursor()

            cursor.execute(
                "INSERT INTO ventas (id_cliente) VALUES (%s) RETURNING id_venta",
                (cliente_id,)
            )

            venta_id = cursor.fetchone()[0]

            cursor.execute(
                """
                INSERT INTO detalle_ventas (id_venta, id_producto, cantidad, subtotal)
                VALUES (%s, %s, %s, %s)
                """,
                (venta_id, producto_id, cant, subtotal)
            )

            cursor.execute(
                "UPDATE productos SET stock=%s WHERE id_producto=%s",
                (stock - cant, producto_id)
            )

            conexion.commit()
            conexion.close()

            messagebox.showinfo("Éxito", "Venta registrada. Total Q" + str(subtotal))

            id_cliente.delete(0, tk.END)
            id_producto.delete(0, tk.END)
            cantidad.delete(0, tk.END)

            mostrar_productos()
            mostrar_clientes()
            mostrar_ventas()

        except:
            messagebox.showerror("Error", "No se pudo registrar la venta")

    crear_boton("Registrar Venta", registrar).pack(pady=3)
    crear_boton("Actualizar Datos", lambda: [mostrar_productos(), mostrar_clientes(), mostrar_ventas()]).pack(pady=3)
    crear_boton("Regresar", menu_principal, COLOR_SALIR, "white").pack(pady=8)

    mostrar_productos()
    mostrar_clientes()
    mostrar_ventas()


ventana = tk.Tk()
ventana.title("Sistema de Ventas Boutique")
ventana.geometry("1000x760")

menu_principal()
ventana.mainloop()
