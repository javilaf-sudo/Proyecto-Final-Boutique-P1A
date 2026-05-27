import tkinter as tk
from tkinter import messagebox
from database import conectar


def ventana_productos():
    ventana_p = tk.Toplevel()
    ventana_p.title("Productos")
    ventana_p.geometry("700x600")

    tk.Label(ventana_p, text="GESTION DE PRODUCTOS", font=("Arial", 14, "bold")).pack(pady=10)

    tk.Label(ventana_p, text="ID para editar/eliminar").pack()
    entrada_id = tk.Entry(ventana_p)
    entrada_id.pack()

    tk.Label(ventana_p, text="Nombre").pack()
    entrada_nombre = tk.Entry(ventana_p)
    entrada_nombre.pack()

    tk.Label(ventana_p, text="Categoria").pack()
    entrada_categoria = tk.Entry(ventana_p)
    entrada_categoria.pack()

    tk.Label(ventana_p, text="Talla").pack()
    entrada_talla = tk.Entry(ventana_p)
    entrada_talla.pack()

    tk.Label(ventana_p, text="Color").pack()
    entrada_color = tk.Entry(ventana_p)
    entrada_color.pack()

    tk.Label(ventana_p, text="Precio").pack()
    entrada_precio = tk.Entry(ventana_p)
    entrada_precio.pack()

    tk.Label(ventana_p, text="Stock").pack()
    entrada_stock = tk.Entry(ventana_p)
    entrada_stock.pack()

    lista = tk.Listbox(ventana_p, width=90, height=8)
    lista.pack(pady=10)

    def limpiar():
        entrada_id.delete(0, tk.END)
        entrada_nombre.delete(0, tk.END)
        entrada_categoria.delete(0, tk.END)
        entrada_talla.delete(0, tk.END)
        entrada_color.delete(0, tk.END)
        entrada_precio.delete(0, tk.END)
        entrada_stock.delete(0, tk.END)

    def mostrar_productos():
        try:
            conexion = conectar()
            cursor = conexion.cursor()

            cursor.execute("SELECT * FROM productos ORDER BY id_producto ASC")
            productos = cursor.fetchall()

            lista.delete(0, tk.END)

            for p in productos:
                texto = f"ID: {p[0]} | {p[1]} | {p[2]} | Talla: {p[3]} | Color: {p[4]} | Q{p[5]} | Stock: {p[6]}"
                lista.insert(tk.END, texto)

            cursor.close()
            conexion.close()

        except Exception as e:
            messagebox.showerror("Error", "No se pudieron mostrar los productos")

    def guardar_producto():
        try:
            conexion = conectar()
            cursor = conexion.cursor()

            sql = """
            INSERT INTO productos (nombre, categoria, talla, color, precio, stock)
            VALUES (%s, %s, %s, %s, %s, %s)
            """

            datos = (
                entrada_nombre.get(),
                entrada_categoria.get(),
                entrada_talla.get(),
                entrada_color.get(),
                float(entrada_precio.get()),
                int(entrada_stock.get())
            )

            cursor.execute(sql, datos)
            conexion.commit()

            cursor.close()
            conexion.close()

            messagebox.showinfo("Exito", "Producto guardado correctamente")
            limpiar()
            mostrar_productos()

        except:
            messagebox.showerror("Error", "Revise los datos del producto")

    def editar_producto():
        try:
            conexion = conectar()
            cursor = conexion.cursor()

            sql = """
            UPDATE productos
            SET nombre=%s, categoria=%s, talla=%s, color=%s, precio=%s, stock=%s
            WHERE id_producto=%s
            """

            datos = (
                entrada_nombre.get(),
                entrada_categoria.get(),
                entrada_talla.get(),
                entrada_color.get(),
                float(entrada_precio.get()),
                int(entrada_stock.get()),
                int(entrada_id.get())
            )

            cursor.execute(sql, datos)
            conexion.commit()

            cursor.close()
            conexion.close()

            messagebox.showinfo("Exito", "Producto editado correctamente")
            limpiar()
            mostrar_productos()

        except:
            messagebox.showerror("Error", "No se pudo editar el producto")

    def eliminar_producto():
        try:
            conexion = conectar()
            cursor = conexion.cursor()

            id_producto = int(entrada_id.get())

            cursor.execute("DELETE FROM productos WHERE id_producto=%s", (id_producto,))
            conexion.commit()

            cursor.close()
            conexion.close()

            messagebox.showinfo("Exito", "Producto eliminado correctamente")
            limpiar()
            mostrar_productos()

        except:
            messagebox.showerror("Error", "Ingrese un ID valido")

    tk.Button(ventana_p, text="Guardar Producto", width=25, command=guardar_producto).pack(pady=3)
    tk.Button(ventana_p, text="Mostrar Productos", width=25, command=mostrar_productos).pack(pady=3)
    tk.Button(ventana_p, text="Editar Producto", width=25, command=editar_producto).pack(pady=3)
    tk.Button(ventana_p, text="Eliminar Producto", width=25, command=eliminar_producto).pack(pady=3)
    tk.Button(ventana_p, text="Cerrar", width=25, command=ventana_p.destroy).pack(pady=5)


def ventana_clientes():
    ventana_c = tk.Toplevel()
    ventana_c.title("Clientes")
    ventana_c.geometry("650x500")

    tk.Label(ventana_c, text="GESTION DE CLIENTES", font=("Arial", 14, "bold")).pack(pady=10)

    tk.Label(ventana_c, text="Nombre").pack()
    entrada_nombre = tk.Entry(ventana_c)
    entrada_nombre.pack()

    tk.Label(ventana_c, text="Apellido").pack()
    entrada_apellido = tk.Entry(ventana_c)
    entrada_apellido.pack()

    tk.Label(ventana_c, text="Telefono").pack()
    entrada_telefono = tk.Entry(ventana_c)
    entrada_telefono.pack()

    tk.Label(ventana_c, text="Correo").pack()
    entrada_correo = tk.Entry(ventana_c)
    entrada_correo.pack()

    lista = tk.Listbox(ventana_c, width=80, height=8)
    lista.pack(pady=10)

    def mostrar_clientes():
        try:
            conexion = conectar()
            cursor = conexion.cursor()

            cursor.execute("SELECT * FROM clientes ORDER BY id_cliente ASC")
            clientes = cursor.fetchall()

            lista.delete(0, tk.END)

            for c in clientes:
                texto = f"ID: {c[0]} | {c[1]} {c[2]} | Tel: {c[3]} | Correo: {c[4]}"
                lista.insert(tk.END, texto)

            cursor.close()
            conexion.close()

        except:
            messagebox.showerror("Error", "No se pudieron mostrar los clientes")

    def guardar_cliente():
        try:
            conexion = conectar()
            cursor = conexion.cursor()

            sql = """
            INSERT INTO clientes (nombre, apellido, telefono, correo)
            VALUES (%s, %s, %s, %s)
            """

            datos = (
                entrada_nombre.get(),
                entrada_apellido.get(),
                entrada_telefono.get(),
                entrada_correo.get()
            )

            cursor.execute(sql, datos)
            conexion.commit()

            cursor.close()
            conexion.close()

            messagebox.showinfo("Exito", "Cliente guardado correctamente")

            entrada_nombre.delete(0, tk.END)
            entrada_apellido.delete(0, tk.END)
            entrada_telefono.delete(0, tk.END)
            entrada_correo.delete(0, tk.END)

            mostrar_clientes()

        except:
            messagebox.showerror("Error", "No se pudo guardar el cliente")

    tk.Button(ventana_c, text="Guardar Cliente", width=25, command=guardar_cliente).pack(pady=5)
    tk.Button(ventana_c, text="Mostrar Clientes", width=25, command=mostrar_clientes).pack(pady=5)
    tk.Button(ventana_c, text="Cerrar", width=25, command=ventana_c.destroy).pack(pady=5)


def ventana_ventas():
    ventana_v = tk.Toplevel()
    ventana_v.title("Ventas")
    ventana_v.geometry("650x500")

    tk.Label(ventana_v, text="REGISTRAR VENTA", font=("Arial", 14, "bold")).pack(pady=10)

    tk.Label(ventana_v, text="ID Cliente").pack()
    entrada_cliente = tk.Entry(ventana_v)
    entrada_cliente.pack()

    tk.Label(ventana_v, text="ID Producto").pack()
    entrada_producto = tk.Entry(ventana_v)
    entrada_producto.pack()

    tk.Label(ventana_v, text="Cantidad").pack()
    entrada_cantidad = tk.Entry(ventana_v)
    entrada_cantidad.pack()

    lista = tk.Listbox(ventana_v, width=85, height=10)
    lista.pack(pady=10)

    def mostrar_ventas():
        try:
            conexion = conectar()
            cursor = conexion.cursor()

            sql = """
            SELECT ventas.id_venta, clientes.nombre, productos.nombre, detalle_ventas.cantidad, detalle_ventas.subtotal, ventas.fecha
            FROM detalle_ventas
            INNER JOIN ventas ON detalle_ventas.id_venta = ventas.id_venta
            INNER JOIN clientes ON ventas.id_cliente = clientes.id_cliente
            INNER JOIN productos ON detalle_ventas.id_producto = productos.id_producto
            ORDER BY ventas.id_venta ASC
            """

            cursor.execute(sql)
            ventas = cursor.fetchall()

            lista.delete(0, tk.END)

            for v in ventas:
                texto = f"Venta: {v[0]} | Cliente: {v[1]} | Producto: {v[2]} | Cantidad: {v[3]} | Total: Q{v[4]} | Fecha: {v[5]}"
                lista.insert(tk.END, texto)

            cursor.close()
            conexion.close()

        except:
            messagebox.showerror("Error", "No se pudieron mostrar las ventas")

    def registrar_venta():
        try:
            conexion = conectar()
            cursor = conexion.cursor()

            id_cliente = int(entrada_cliente.get())
            id_producto = int(entrada_producto.get())
            cantidad = int(entrada_cantidad.get())

            cursor.execute("SELECT precio, stock FROM productos WHERE id_producto=%s", (id_producto,))
            producto = cursor.fetchone()

            if producto is None:
                messagebox.showerror("Error", "Producto no encontrado")
                return

            precio = float(producto[0])
            stock = int(producto[1])

            if cantidad > stock:
                messagebox.showerror("Error", "No hay suficiente stock")
                return

            subtotal = precio * cantidad

            cursor.execute("INSERT INTO ventas (id_cliente) VALUES (%s) RETURNING id_venta", (id_cliente,))
            id_venta = cursor.fetchone()[0]

            sql = """
            INSERT INTO detalle_ventas (id_venta, id_producto, cantidad, subtotal)
            VALUES (%s, %s, %s, %s)
            """

            cursor.execute(sql, (id_venta, id_producto, cantidad, subtotal))

            nuevo_stock = stock - cantidad
            cursor.execute("UPDATE productos SET stock=%s WHERE id_producto=%s", (nuevo_stock, id_producto))

            conexion.commit()

            cursor.close()
            conexion.close()

            messagebox.showinfo("Exito", "Venta registrada. Total: Q" + str(subtotal))

            entrada_cliente.delete(0, tk.END)
            entrada_producto.delete(0, tk.END)
            entrada_cantidad.delete(0, tk.END)

            mostrar_ventas()

        except:
            messagebox.showerror("Error", "Revise los datos de la venta")

    tk.Button(ventana_v, text="Registrar Venta", width=25, command=registrar_venta).pack(pady=5)
    tk.Button(ventana_v, text="Mostrar Ventas", width=25, command=mostrar_ventas).pack(pady=5)
    tk.Button(ventana_v, text="Cerrar", width=25, command=ventana_v.destroy).pack(pady=5)


ventana = tk.Tk()
ventana.title("Sistema de Ventas Boutique")
ventana.geometry("500x420")

tk.Label(
    ventana,
    text="SISTEMA DE VENTAS BOUTIQUE",
    font=("Arial", 16, "bold")
).pack(pady=25)

tk.Button(ventana, text="Productos", width=30, height=2, command=ventana_productos).pack(pady=8)
tk.Button(ventana, text="Clientes", width=30, height=2, command=ventana_clientes).pack(pady=8)
tk.Button(ventana, text="Ventas", width=30, height=2, command=ventana_ventas).pack(pady=8)
tk.Button(ventana, text="Salir", width=30, height=2, command=ventana.destroy).pack(pady=8)

ventana.mainloop()