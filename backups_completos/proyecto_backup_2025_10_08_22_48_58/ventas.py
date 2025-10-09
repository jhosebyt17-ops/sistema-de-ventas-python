import sqlite3
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
import threading
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from collections import defaultdict
import sys
import os
import re

class Ventas(tk.Frame):
    db_name = "database.db"

    def __init__(self, parent):
        super().__init__(parent)
        self.numero_factura = self.obtener_numero_factura_actual()
        self.productos_seleccionados = []
        self.widgets()
        self.cargar_productos()
        self.cargar_clientes()
        self.timer_cliente = None
        self.timer_producto = None
        
    def rutas(self,ruta):
        try:
            rutabase=sys.__MEIPASS
        except Exception:
            rutabase=os.path.abspath(".")
        return os.path.join(rutabase,ruta)
        
    def obtener_numero_factura_actual(self):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT MAX(factura) FROM ventas")
            last_invoice_number = c.fetchone()[0]
            conn.close()
            return last_invoice_number + 1 if last_invoice_number is not None else 1
        except sqlite3.Error as e:
            print("Error obteniendo el número de factura actual:", e)
            return 1
        
    def cargar_clientes(self):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT nombre FROM clientes")
            clientes = c.fetchall()
            self.clientes = [cliente[0] for cliente in clientes]
            self.entry_cliente["values"] = self.clientes
            conn.close()
        except sqlite3.Error as e:
            print("Error cargando clientes:", e)
            
    def filtrar_clientes(self, event):
        if self.timer_cliente:
            self.timer_cliente.cancel()
        self.timer_cliente = threading.Timer(0.5, self._filter_clientes)
        self.timer_cliente.start()

    def _filter_clientes(self):
        typed = self.entry_cliente.get()
        
        if typed == '':
            data = self.clientes
        else:
            data = [item for item in self.clientes if typed.lower() in item.lower()]
        
        if data:
            self.entry_cliente['values'] = data
            self.entry_cliente.event_generate('<Down>')  # Mostrar la lista desplegable
        else:
            self.entry_cliente['values'] = ['No results found']
            self.entry_cliente.event_generate('<Down>')  # Mostrar la lista desplegable
            self.entry_cliente.delete(0, tk.END)  # Limpiar la entrada si no hay resultados
    
    def cargar_productos(self):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT articulo FROM articulos")
            self.products = [product[0] for product in c.fetchall()]
            self.entry_producto["values"] = self.products
            conn.close()
        except sqlite3.Error as e:
            print("Error cargando productos:", e)

    def filtrar_productos(self, event):
        if self.timer_producto:
            self.timer_producto.cancel()
        self.timer_producto = threading.Timer(0.5, self._filter_products)
        self.timer_producto.start()

    def _filter_products(self):
        typed = self.entry_producto.get()
        
        if typed == '':
            data = self.products
        else:
            data = [item for item in self.products if typed.lower() in item.lower()]
        
        if data:
            self.entry_producto['values'] = data
            self.entry_producto.event_generate('<Down>')  # Mostrar la lista desplegable
        else:
            self.entry_producto['values'] = ['No results found']
            self.entry_producto.event_generate('<Down>')  # Mostrar la lista desplegable
            self.entry_producto.delete(0, tk.END)  # Limpiar la entrada si no hay resultados
            
    def agregar_articulo(self):
        cliente = self.entry_cliente.get()
        producto = self.entry_producto.get()
        cantidad = self.entry_cantidad.get()

        if not cliente:
            messagebox.showerror("Error", "Por favor seleccione un cliente.")
            return
        
        if not producto:
            messagebox.showerror("Error", "Por favor seleccione un producto.")
            return

        if not cantidad.isdigit() or int(cantidad) <= 0:
            messagebox.showerror("Error", "Por favor ingrese una cantidad válida.")
            return

        cantidad = int(cantidad)
        cliente = self.entry_cliente.get()

        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT precio, costo, stock FROM articulos WHERE articulo=?", (producto,))
            resultado = c.fetchone()
            
            if resultado is None:
                messagebox.showerror("Error", "Producto no encontrado.")
                return

            precio, costo, stock = resultado
            
            if cantidad > stock:
                messagebox.showerror("Error", f"Stock insuficiente. Solo hay {stock} unidades disponibles.")
                return

            total = precio * cantidad
            total_cop = "{:,.2f}".format(total)

            # Insertar el artículo en el Treeview con el número de factura actual
            self.tre.insert("", "end", values=(self.numero_factura, cliente, producto, "{:,.2f}".format(precio), cantidad, total_cop))
            self.productos_seleccionados.append((self.numero_factura, cliente, producto, precio, cantidad, total_cop, costo))

            conn.close()

            # Limpiar Entry de cantidad y deseleccionar Combobox
            self.entry_cantidad.delete(0, 'end')
            self.entry_producto.set('')
            # self.entry_cliente.set('')  # Limpiar la selección del cliente
        except sqlite3.Error as e:
            print("Error al agregar artículo:", e)
            
        self.calcular_precio_total()  # Calcular el precio total después de agregar un artículo
    
    def calcular_precio_total(self):
        total_pagar = sum(
            float(self.tre.item(item)["values"][-1].replace("", "").replace(",", "")) 
            for item in self.tre.get_children()
        )
        total_pagar_cop = "{:,.2f}".format(total_pagar)
        self.label_precio_total.config(text=f"Precio a Pagar: {total_pagar_cop}")
            
    def actualizar_stock(self, event=None):
        producto_seleccionado = self.entry_producto.get()

        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT stock FROM articulos WHERE articulo=?", (producto_seleccionado,))
            stock = c.fetchone()[0]
            conn.close()

            self.label_stock.config(text=f"Stock: {stock}")
        except sqlite3.Error as e:
            print("Error al obtener el stock del producto:", e)
            
    def realizar_pago(self):
        if not self.tre.get_children():
            messagebox.showerror("Error", "No hay productos seleccionados para realizar el pago.")
            return
        
        # Eliminar el símbolo de dólar y las comas antes de convertir a float
        total_venta = sum(
            float(item[5].replace("", "").replace(",", "").strip())  # Eliminar comas y el símbolo '$'
            for item in self.productos_seleccionados
        )
        
        # Formatear el total para agregar puntos en los miles
        total_formateado = "{:,.2f}".format(total_venta)

        # Crear una nueva ventana TopLevel para que el usuario ingrese el monto pagado
        ventana_pago = tk.Toplevel(self)
        ventana_pago.title("Realizar pago")
        ventana_pago.geometry("400x400+450+80")
        ventana_pago.config(bg="#C6D9E3")
        ventana_pago.resizable(False, False)
        ventana_pago.transient(self.master)
        ventana_pago.grab_set()
        ventana_pago.focus_set()
        ventana_pago.lift()

        label_titulo = tk.Label(ventana_pago, text="Realizar pago", font="sans 30 bold", bg="#C6D9E3")
        label_titulo.place(x=70, y=10)

        label_total = tk.Label(ventana_pago, text=f"Total a pagar: {total_formateado}", font="sans 14 bold", bg="#C6D9E3")
        label_total.place(x=80, y=100)

        label_monto = tk.Label(ventana_pago, text="Ingrese el monto pagado:", font="sans 14 bold", bg="#C6D9E3")
        label_monto.place(x=80, y=160)

        entry_monto = ttk.Entry(ventana_pago, font="sans 14 bold")
        entry_monto.place(x=80, y=210, width=240, height=40)
        
        ruta=self.rutas(r"icono/pago.png")
        imagen_pil = Image.open(ruta)
        imagen_resize10 = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize10)
        
        button_confirmar_pago = tk.Button(ventana_pago, text="Confirmar Pago", font="sans 14 bold", bg="#dddddd", fg="black", command=lambda: self.procesar_pago(entry_monto.get(), ventana_pago, total_venta))
        button_confirmar_pago.config(image=imagen_tk, compound="left", padx=10)
        button_confirmar_pago.image = imagen_tk
        button_confirmar_pago.place(x=80, y=270, width=240, height=40)

    def procesar_pago(self, cantidad_pagada, ventana_pago, total_venta):
        if ',' in cantidad_pagada:
            messagebox.showwarning("Advertencia", "No coloque comas. Solo utilice punto si requiere decimales.")
            return  # Salir de la función si la entrada es incorrecta

        # Expresión regular para verificar si el precio y costo tienen hasta 2 decimales
        decimal_pattern = r'^\d+(\.\d{1,2})?$'

        # Validar que el precio y costo sigan el formato de hasta 2 decimales
        if not re.match(decimal_pattern, cantidad_pagada):
            messagebox.showwarning("Advertencia", "Cantidad pagada debe tener un máximo de dos decimales.")
            return  # Salir de la función si el formato no es correcto
        
        try:
            cantidad_pagada = float(cantidad_pagada)
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese una cantidad válida.")
            return

        cliente = self.entry_cliente.get()  # Obtener el cliente seleccionado

        if cantidad_pagada < total_venta:
            messagebox.showerror("Error", "La cantidad pagada es insuficiente.")
            return

        cambio = cantidad_pagada - total_venta

        # Formatear el total para agregar puntos en los miles
        total_formateado = "{:,.2f}".format(total_venta)

        mensaje = f"Total: {total_formateado} \nCantidad pagada: {cantidad_pagada:,.2f} \nCambio: {cambio:,.2f} "
        messagebox.showinfo("Pago Realizado", mensaje)

        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()

            # Obtener la fecha y hora actual
            fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d")
            hora_actual = datetime.datetime.now().strftime("%H:%M:%S")

            # Insertar las ventas en la tabla 'ventas' usando el número de factura actual
            for item in self.productos_seleccionados:
                factura, cliente, producto, precio, cantidad, total, costo = item
                c.execute("INSERT INTO ventas (factura, cliente, articulo, precio, cantidad, total, costo, fecha, hora) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (factura, cliente, producto, precio, cantidad, total.replace(" ", "").replace(",", ""), costo * cantidad, fecha_actual, hora_actual))

                # Restar la cantidad de productos vendidos del stock en la tabla 'articulos'
                c.execute("UPDATE articulos SET stock = stock - ? WHERE articulo = ?", (cantidad, producto))

            conn.commit()
            
            # Generar factura en PDF
            self.generar_factura_pdf(total_venta, cliente, cantidad_pagada, cambio)

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al registrar la venta: {e}")

        self.numero_factura += 1
        self.label_numero_factura.config(text=str(self.numero_factura))

        self.productos_seleccionados = []
        self.limpiar_campos()

        # Cerrar la ventana de pago después de procesar el pago
        ventana_pago.destroy()
        
    def limpiar_campos(self):
        # Limpiar TreeView y Label de precio total
        for item in self.tre.get_children():
            self.tre.delete(item)
        self.label_precio_total.config(text="Precio a Pagar: 0 ")

        self.entry_producto.set('')
        self.entry_cantidad.delete(0, 'end')
        
    def ver_ventas_realizadas(self):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT * FROM ventas")
            ventas = c.fetchall()
            conn.close()

            ventana_ventas = tk.Toplevel(self)
            ventana_ventas.title("Ventas Realizadas")
            ventana_ventas.geometry("1100x650+120+20")
            ventana_ventas.configure(bg="#C6D9E3")
            ventana_ventas.resizable(False, False)
            ventana_ventas.transient(self.master)
            ventana_ventas.grab_set()
            ventana_ventas.focus_set()
            ventana_ventas.lift()
            ruta=self.rutas(r"icono.ico")
            ventana_ventas.iconbitmap(ruta)

            # Función para filtrar las ventas
            def filtrar_ventas():
                factura_a_buscar = entry_factura.get()
                cliente_a_buscar = entry_cliente.get()
                for item in tree.get_children():
                    tree.delete(item)

                ventas_filtradas = [
                    venta for venta in ventas
                    if (str(venta[0]) == factura_a_buscar or not factura_a_buscar) and
                    (venta[1].lower() == cliente_a_buscar.lower() or not cliente_a_buscar)
                ]

                # Usamos defaultdict para agrupar las ventas por factura
                ventas_por_factura = defaultdict(lambda: {'cliente': '', 'fecha': '', 'hora': '', 'total': 0})

                for venta in ventas_filtradas:
                    factura = venta[0]  # Número de factura
                    cliente = venta[1]  # Cliente
                    fecha = venta[6]  # Fecha
                    hora = venta[7]  # Hora
                    total_item = venta[5]  # Total por item

                    # Acumulamos el total por factura
                    ventas_por_factura[factura]['cliente'] = cliente
                    ventas_por_factura[factura]['fecha'] = fecha
                    ventas_por_factura[factura]['hora'] = hora
                    ventas_por_factura[factura]['total'] += total_item

                # Insertar los resultados en el Treeview
                for factura, datos in ventas_por_factura.items():
                    datos['fecha'] = datetime.datetime.strptime(datos['fecha'], "%Y-%m-%d").strftime("%d-%m-%Y")  # Formato de fecha
                    datos['total'] = "{:,.2f}".format(datos['total'])  # Formatear el total
                    tree.insert("", "end", values=(factura, datos['cliente'], datos['total'], datos['fecha'], datos['hora']))

            # Agregar el Label "Ventas Realizadas"
            label_ventas_realizadas = tk.Label(ventana_ventas, text="Ventas Realizadas", font="sans 26 bold", bg="#C6D9E3")
            label_ventas_realizadas.place(x=350, y=20)

            # Frame para el filtro
            filtro_frame = tk.Frame(ventana_ventas, bg="#C6D9E3")
            filtro_frame.place(x=20, y=60, width=1060, height=60)

            # Entry para ingresar el número de factura
            label_factura = tk.Label(filtro_frame, text="Número de Factura:", bg="#C6D9E3", font="sans 14 bold")
            label_factura.place(x=10, y=15)
            entry_factura = ttk.Entry(filtro_frame, font="sans 14 bold")
            entry_factura.place(x=200, y=10, width=200, height=40)

            # Entry para ingresar el nombre del cliente
            label_cliente = tk.Label(filtro_frame, text="Nombre del Cliente:", bg="#C6D9E3", font="sans 14 bold")
            label_cliente.place(x=420, y=15)
            entry_cliente = ttk.Entry(filtro_frame, font="sans 14 bold")
            entry_cliente.place(x=620, y=10, width=200, height=40)

            # Botón para aplicar el filtro
            ruta = self.rutas(r"icono/filtrar.png")
            imagen_pil = Image.open(ruta)
            imagen_resize = imagen_pil.resize((30, 30))
            imagen_tk = ImageTk.PhotoImage(imagen_resize)

            btn_filtrar = tk.Button(filtro_frame, text="Filtrar", font="sans 14 bold", bg="#dddddd", command=filtrar_ventas)
            btn_filtrar.config(image=imagen_tk, compound="left", padx=10)
            btn_filtrar.image = imagen_tk
            btn_filtrar.place(x=840, y=10)

            # Frame para el Treeview
            tree_frame = tk.Frame(ventana_ventas, bg="gray")
            tree_frame.place(x=20, y=130, width=1060, height=500)

            # Barra de desplazamiento vertical
            scrol_y = ttk.Scrollbar(tree_frame)
            scrol_y.pack(side="right", fill="y")

            # Barra de desplazamiento horizontal
            scrol_x = ttk.Scrollbar(tree_frame, orient=HORIZONTAL)
            scrol_x.pack(side=BOTTOM, fill=X)

            # Treeview
            tree = ttk.Treeview(tree_frame, columns=("Factura", "Cliente", "Total", "Fecha", "Hora"), show="headings")
            tree.pack(expand=True, fill=BOTH)

            scrol_y.config(command=tree.yview)
            scrol_x.config(command=tree.xview)

            tree.heading("Factura", text="Factura")
            tree.heading("Cliente", text="Cliente")
            tree.heading("Total", text="Total")
            tree.heading("Fecha", text="Fecha")
            tree.heading("Hora", text="Hora")

            tree.column("Factura", width=50, anchor="center")
            tree.column("Cliente", width=180, anchor="center")
            tree.column("Total", width=100, anchor="center")
            tree.column("Fecha", width=100, anchor="center")
            tree.column("Hora", width=80, anchor="center")

            # Mostrar todas las ventas agrupadas
            ventas_por_factura = defaultdict(lambda: {'cliente': '', 'fecha': '', 'hora': '', 'total': 0})
            for venta in ventas:
                factura = venta[0]
                cliente = venta[1]
                fecha = venta[6]
                hora = venta[7]
                total = venta[5]

                # Acumulamos el total por factura
                ventas_por_factura[factura]['cliente'] = cliente
                ventas_por_factura[factura]['fecha'] = fecha
                ventas_por_factura[factura]['hora'] = hora
                ventas_por_factura[factura]['total'] += float(total)

            # Insertar los datos agregados en el Treeview
            for factura, datos in ventas_por_factura.items():
                datos['fecha'] = datetime.datetime.strptime(datos['fecha'], "%Y-%m-%d").strftime("%d-%m-%Y")  # Formato de fecha
                datos['total'] = "{:,.2f}".format(datos['total'])  # Formatear el total
                tree.insert("", "end", values=(factura, datos['cliente'], datos['total'], datos['fecha'], datos['hora']))

            # Función para mostrar los detalles de la factura seleccionada
            def ver_detalles_factura(event):
                item = tree.selection()[0]  # Obtener el item seleccionado
                factura_seleccionada = tree.item(item, "values")[0]  # Obtener la factura

                # Crear una nueva ventana para mostrar los detalles de la factura
                ventana_detalles = tk.Toplevel(self)
                ventana_detalles.title(f"Detalles de la Factura {factura_seleccionada}")
                ventana_detalles.geometry("1100x650+120+20")
                ventana_detalles.configure(bg="#C6D9E3")
                ventana_detalles.resizable(False, False)
                ventana_detalles.transient(self.master)
                ventana_detalles.grab_set()
                ventana_detalles.focus_set()
                ventana_detalles.lift()

                label_detalle_ventas = tk.Label(ventana_detalles, text=f"Detalles de la Factura No.{factura_seleccionada}", font="sans 30 bold", bg="#C6D9E3")
                label_detalle_ventas.place(x=300, y=40)
                
                tree_frame1 = tk.Frame(ventana_detalles, bg="gray")
                tree_frame1.place(x=20, y=130, width=1060, height=500)
                
                # Barra de desplazamiento vertical
                scrol_y = ttk.Scrollbar(tree_frame1)
                scrol_y.pack(side="right", fill="y")

                # Barra de desplazamiento horizontal
                scrol_x = ttk.Scrollbar(tree_frame1, orient=HORIZONTAL)
                scrol_x.pack(side=BOTTOM, fill=X)

                # Crear el Treeview para mostrar los detalles
                tree_detalles = ttk.Treeview(tree_frame1, columns=("Factura", "Cliente", "Producto", "Precio", "Cantidad", "Total", "Fecha", "Hora", "Costo"), show="headings")
                tree_detalles.pack(expand=True, fill=BOTH)
                
                scrol_y.config(command=tree.yview)
                scrol_x.config(command=tree.xview)

                # Agregar las columnas
                tree_detalles.heading("Factura", text="Factura")
                tree_detalles.heading("Cliente", text="Cliente")
                tree_detalles.heading("Producto", text="Producto")
                tree_detalles.heading("Precio", text="Precio")
                tree_detalles.heading("Cantidad", text="Cantidad")
                tree_detalles.heading("Total", text="Total")
                tree_detalles.heading("Fecha", text="Fecha")
                tree_detalles.heading("Hora", text="Hora")
                tree_detalles.heading("Costo", text="Costo")

                tree_detalles.column("Factura", width=50, anchor="center")
                tree_detalles.column("Cliente", width=180, anchor="center")
                tree_detalles.column("Producto", width=150, anchor="center")
                tree_detalles.column("Precio", width=80, anchor="center")
                tree_detalles.column("Cantidad", width=80, anchor="center")
                tree_detalles.column("Total", width=100, anchor="center")
                tree_detalles.column("Fecha", width=100, anchor="center")
                tree_detalles.column("Hora", width=80, anchor="center")
                tree_detalles.column("Costo", width=80, anchor="center")

                # Consultar todos los registros de la factura seleccionada
                conn = sqlite3.connect(self.db_name)
                c = conn.cursor()
                c.execute("SELECT * FROM ventas WHERE factura = ?", (factura_seleccionada,))
                detalles_venta = c.fetchall()
                conn.close()

                # Insertar los detalles en el Treeview, formateando los valores
                for detalle in detalles_venta:
                    # Formatear el precio, total y costo con coma en miles y 2 decimales
                    detalle_formateado = list(detalle)
                    detalle_formateado[3] = "{:,.2f}".format(detalle_formateado[3])  # Precio
                    detalle_formateado[5] = "{:,.2f}".format(detalle_formateado[5])  # Total
                    detalle_formateado[8] = "{:,.2f}".format(detalle_formateado[8])  # Costo
                    tree_detalles.insert("", "end", values=detalle_formateado)

            # Asociar el evento de doble clic en el Treeview con la función de ver detalles
            tree.bind("<Double-1>", ver_detalles_factura)

        except sqlite3.Error as e:
            print("Error al obtener las ventas:", e)
            
    def generar_factura_pdf(self, total_venta, cliente, cantidad_pagada, cambio):
        try:
            # Crear un lienzo para el PDF
            factura_path = f"facturas/Factura_{self.numero_factura}.pdf"
            c = canvas.Canvas(factura_path, pagesize=letter)

            # Información de la empresa
            empresa_nombre = "Sistema de Ventas Version 1.0.0"
            empresa_direccion = "Diagonal 18 No. 20-29 Universidad de Cundinamarca, Fusagasuga, Colombia"
            empresa_telefono = "+57 3241852459 / +57 320 4028440"
            empresa_email = "jhosebyt17@gmail.com"
            empresa_website = "www.Sistemadeventas.com"
            

            # Encabezado de la factura
            c.setFont("Helvetica-Bold", 18)
            c.setFillColor(colors.darkblue)
            c.drawCentredString(300, 750, "FACTURA DE SERVICIOS")

            # Información de la empresa
            c.setFillColor(colors.black)
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, 710, f"{empresa_nombre}")
            c.setFont("Helvetica", 12)
            c.drawString(50, 690, f"Dirección: {empresa_direccion}")
            c.drawString(50, 670, f"Teléfono: {empresa_telefono}")
            c.drawString(50, 650, f"Email: {empresa_email}")
            c.drawString(50, 630, f"Website: {empresa_website}")

            # Línea divisoria
            c.setLineWidth(0.5)
            c.setStrokeColor(colors.grey)
            c.line(50, 620, 550, 620)

            # Información de la factura
            c.setFont("Helvetica", 12)
            c.drawString(50, 600, f"Número de Factura: {self.numero_factura}")
            c.drawString(50, 580, f"Fecha: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            # Línea divisoria
            c.line(50, 560, 550, 560)

            # Información del cliente
            c.drawString(50, 540, f"Cliente: {cliente}")
            c.drawString(50, 520, "Descripción de Productos:")

            # Crear una tabla para los productos con bordes
            y_offset = 500
            c.setFont("Helvetica-Bold", 12)
            c.drawString(70, y_offset, "Producto")
            c.drawString(270, y_offset, "Cantidad")
            c.drawString(370, y_offset, "Precio")
            c.drawString(470, y_offset, "Total")

            # Dibujar una línea debajo del encabezado de la tabla
            c.line(50, y_offset - 10, 550, y_offset - 10)
            y_offset -= 30
            c.setFont("Helvetica", 12)
            for item in self.productos_seleccionados:
                factura, cliente, producto, precio, cantidad, total, costo = item
                c.drawString(70, y_offset, producto)
                c.drawString(270, y_offset, str(cantidad))
                c.drawString(370, y_offset, "{:,.2f}".format(precio))
                c.drawString(470, y_offset, total)
                y_offset -= 20

            # Línea divisoria
            c.line(50, y_offset, 550, y_offset)
            y_offset -= 20

            # Total a pagar
            c.setFont("Helvetica-Bold", 14)
            c.setFillColor(colors.darkblue)
            c.drawString(50, y_offset, f"Total a Pagar: {total_venta:,.2f}")
            c.drawString(50, y_offset - 20, f"Cantidad pagada: {cantidad_pagada:,.2f}")
            c.drawString(50, y_offset - 40, f"Cambio: {cambio:,.2f}")
            c.setFillColor(colors.black)
            c.setFont("Helvetica", 12)
            
            y_offset -= 20
            c.line(50, y_offset, 550, y_offset)

            # Mensaje de agradecimiento
            c.setFont("Helvetica-Bold", 16)
            c.drawString(150, y_offset - 60, "¡Gracias por tu compra, vuelve pronto!")

            # Términos y condiciones
            y_offset -= 100
            c.setFont("Helvetica", 10)
            c.drawString(50, y_offset, "Términos y Condiciones:")
            c.drawString(50, y_offset - 20, "1. Los productos comprados no tienen devolución.")
            c.drawString(50, y_offset - 40, "2. Conserve esta factura como comprobante de su compra.")
            c.drawString(50, y_offset - 60, "3. Para más información, visite nuestro sitio web o contacte a servicio al cliente.")

            # Pie de página con información de contacto y redes sociales
            c.setFont("Helvetica", 10)
            c.drawString(50, 50, "Para más información, visite nuestro sitio web o síganos en nuestras redes sociales:")
            c.drawString(50, 40, f"Telefono: +57 3241852459/ +57 320 4028440, software creado por Sebastian Morales / Johan Rubio")

            c.save()

            messagebox.showinfo("Factura Generada", f"Se ha generado la factura en: {factura_path}")
            
            # Abrir el archivo PDF
            os.startfile(os.path.abspath(factura_path))

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar la factura: {e}")
            
    def limpiar_lista(self):
        self.tre.delete(*self.tre.get_children())
        self.productos_seleccionados.clear()
        self.calcular_precio_total()
        
    def eliminar_articulo(self):
        # Obtener el artículo seleccionado en el Treeview
        item_seleccionado = self.tre.selection()
        if not item_seleccionado:
            messagebox.showerror("Error", "No hay ningún artículo seleccionado.")
            return

        item_id = item_seleccionado[0]
        valores_item = self.tre.item(item_id)["values"]
        factura, cliente, articulo, precio, cantidad, total = valores_item

        # Eliminar el artículo del Treeview
        self.tre.delete(item_id)

        # Actualizar la lista de productos seleccionados
        self.productos_seleccionados = [producto for producto in self.productos_seleccionados if producto[2] != articulo]

        # Recalcular el precio total
        self.calcular_precio_total()
        
    def editar_articulo(self):
        selected_item = self.tre.selection()
        if not selected_item:
            messagebox.showerror("Error", "Por favor seleccione un artículo para editar.")
            return
        
        item_values = self.tre.item(selected_item[0], 'values')
        if not item_values:
            return

        current_producto = item_values[2]
        current_cantidad = item_values[4]

        new_cantidad = simpledialog.askinteger("Editar Artículo", "Ingrese la nueva cantidad:", initialvalue=current_cantidad)
        
        if new_cantidad is not None:
            try:
                conn = sqlite3.connect(self.db_name)
                c = conn.cursor()
                c.execute("SELECT precio, costo, stock FROM articulos WHERE articulo=?", (current_producto,))
                resultado = c.fetchone()
                
                if resultado is None:
                    messagebox.showerror("Error", "Producto no encontrado.")
                    return

                precio, costo, stock = resultado
                
                if new_cantidad > stock:
                    messagebox.showerror("Error", f"Stock insuficiente. Solo hay {stock} unidades disponibles.")
                    return

                total = precio * new_cantidad
                total_cop = "{:,.2f} ".format(total)

                self.tre.item(selected_item[0], values=(self.numero_factura, self.entry_cliente.get(), current_producto, "{:,.2f} ".format(precio), new_cantidad, total_cop))
                
                for idx, producto in enumerate(self.productos_seleccionados):
                    if producto[2] == current_producto:
                        self.productos_seleccionados[idx] = (self.numero_factura, self.entry_cliente.get(), current_producto, precio, new_cantidad, total_cop, costo)
                        break
                
                conn.close()

                self.calcular_precio_total()  # Actualizar el precio total después de editar el artículo
            except sqlite3.Error as e:
                print("Error al editar el artículo:", e)

    def widgets(self):

        # LabelFrame con entrys para ingresar datos
        labelframe = tk.LabelFrame(self, font="sans 12 bold", bg="#C6D9E3")  
        labelframe.place(x=25, y=30, width=1045, height=180)

        label_cliente = tk.Label(labelframe, text="Cliente:", font="sans 14 bold", bg="#C6D9E3")
        label_cliente.place(x=10, y=11)
        self.entry_cliente = ttk.Combobox(labelframe, font="sans 14 bold")
        self.entry_cliente.place(x=120, y=8, width=260, height=40)
        self.entry_cliente.bind('<KeyRelease>', self.filtrar_clientes)
        
        ruta=self.rutas(r"icono/actualizar.png")
        imagen_pil = Image.open(ruta)
        imagen_resize = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize)
        
        self.btn_actualizarc = tk.Button(labelframe, command=self.cargar_clientes)
        self.btn_actualizarc.config(image=imagen_tk, compound="left", padx=10)
        self.btn_actualizarc.image = imagen_tk
        self.btn_actualizarc.place(x=400, y=8, width=40, height=40)
        
        label_producto = tk.Label(labelframe, text="Producto:", font="sans 14 bold", bg="#C6D9E3")
        label_producto.place(x=10, y=70)
        self.entry_producto = ttk.Combobox(labelframe, font="sans 14 bold")
        self.entry_producto.place(x=120, y=66, width=260, height=40)
        self.entry_producto.bind('<KeyRelease>', self.filtrar_productos)
        
        ruta=self.rutas(r"icono/actualizar.png")
        imagen_pil = Image.open(ruta)
        imagen_resize = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize)
        
        self.btn_actualizar = tk.Button(labelframe, command=self.cargar_productos)
        self.btn_actualizar.config(image=imagen_tk, compound="left", padx=10)
        self.btn_actualizar.image = imagen_tk
        self.btn_actualizar.place(x=400, y=66, width=40, height=40)

        label_cantidad = tk.Label(labelframe, text="Cantidad:", font="sans 14 bold", bg="#C6D9E3")
        label_cantidad.place(x=500, y=11)
        self.entry_cantidad = ttk.Entry(labelframe, font="sans 14 bold")
        self.entry_cantidad.place(x=610, y=8, width=100, height=40)
        
        # Label para mostrar el stock del producto seleccionado
        self.label_stock = tk.Label(labelframe, text="Stock:", font="sans 14 bold", bg="#C6D9E3")
        self.label_stock.place(x=500, y=70)
        
        self.entry_producto.bind("<<ComboboxSelected>>", self.actualizar_stock)  # Llamar a actualizar_stock cuando se seleccione un producto
        
        ruta=self.rutas(r"icono/factura.png")
        imagen_pil = Image.open(ruta)
        imagen_resize11 = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize11)
        
        label_factura = tk.Label(labelframe, text="Factura:", font="sans 14 bold", bg="#C6D9E3")
        label_factura.config(image=imagen_tk, compound="left", padx=10)
        label_factura.image = imagen_tk
        label_factura.place(x=800, y=11)
        
        self.label_numero_factura = tk.Label(labelframe, text=f"{self.numero_factura}", font="sans 14 bold", bg="#C6D9E3")
        self.label_numero_factura.place(x=950, y=15)

        ruta=self.rutas(r"icono/agregar.png")
        imagen_pil = Image.open(ruta)
        imagen_resize = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize)
        
        boton_agregar = tk.Button(labelframe, text="Agregar", font="sans 14 bold", command=self.agregar_articulo)
        boton_agregar.config(image=imagen_tk, compound="left", padx=10)
        boton_agregar.image = imagen_tk
        boton_agregar.place(x=90, y=120, width=200, height=40)
        
        ruta=self.rutas(r"icono/eliminar.png")
        imagen_pil = Image.open(ruta)
        imagen_resize = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize)
        
        boton_eliminar = tk.Button(labelframe, text="Eliminar", font="arial 14 bold", command=self.eliminar_articulo)
        boton_eliminar.config(image=imagen_tk, compound="left", padx=10)
        boton_eliminar.image = imagen_tk
        boton_eliminar.place(x=310, y=120, width=200, height=40)
        
        ruta=self.rutas(r"icono/modificar.png")
        imagen_pil = Image.open(ruta)
        imagen_resize = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize)
        
        boton_editar = tk.Button(labelframe, text="Editar", font="arial 14 bold", command=self.editar_articulo)
        boton_editar.config(image=imagen_tk, compound="left", padx=10)
        boton_editar.image = imagen_tk
        boton_editar.place(x=530, y=120, width=200, height=40)
        
        ruta=self.rutas(r"icono/limpiar.png")
        imagen_pil = Image.open(ruta)
        imagen_resize = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize)
        
        boton_limpiar = tk.Button(labelframe, text="Limpiar", font="arial 14 bold", command=self.limpiar_lista)
        boton_limpiar.config(image=imagen_tk, compound="left", padx=10)
        boton_limpiar.image = imagen_tk
        boton_limpiar.place(x=750, y=120, width=200, height=40)
        
        # TreeView Tabla
        treFrame = tk.Frame(self, bg="white") 
        treFrame.place(x=70, y=220, width=980, height=300) 

        # Barra de desplazamiento vertical
        scrol_y = ttk.Scrollbar(treFrame)
        scrol_y.pack(side=RIGHT, fill=Y)

        # Barra de desplazamiento horizontal
        scrol_x = ttk.Scrollbar(treFrame, orient=HORIZONTAL)
        scrol_x.pack(side=BOTTOM, fill=X)

        self.tre = ttk.Treeview(treFrame,  yscrollcommand=scrol_y.set, xscrollcommand=scrol_x.set, height=40, columns=("Factura", "Cliente", "Producto", "Precio", "Cantidad", "Total"), show="headings")
        self.tre.pack(expand=True, fill=BOTH)
        
        scrol_y.config(command=self.tre.yview)
        scrol_x.config(command=self.tre.xview)
        
        self.tre.heading("Factura", text="Factura")
        self.tre.heading("Cliente", text="Cliente")
        self.tre.heading("Producto", text="Producto")
        self.tre.heading("Precio", text="Precio")
        self.tre.heading("Cantidad", text="Cantidad")
        self.tre.heading("Total", text="Total")

        self.tre.column("Factura", width=70, anchor="center")
        self.tre.column("Cliente", width=250, anchor="center")
        self.tre.column("Producto", width=250, anchor="center")
        self.tre.column("Precio", width=120, anchor="center")
        self.tre.column("Cantidad", width=120, anchor="center")
        self.tre.column("Total", width=150, anchor="center")

        ruta=self.rutas(r"icono/precio.png")
        imagen_pil = Image.open(ruta)
        imagen_resize11 = imagen_pil.resize((50, 50))
        imagen_tk = ImageTk.PhotoImage(imagen_resize11)
        
        self.label_precio_total = tk.Label(self, text="Precio a Pagar: 0", font="sans 22 bold", bg="#C6D9E3")
        self.label_precio_total.config(image=imagen_tk, compound="left", padx=10)
        self.label_precio_total.image = imagen_tk
        self.label_precio_total.place(x=580, y=540)
        
        ruta=self.rutas(r"icono/pago.png")
        imagen_pil = Image.open(ruta)
        imagen_resize1 = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize1)
        
        boton_pagar = tk.Button(self, text="Pagar", font="sans 14 bold", command=self.realizar_pago)
        boton_pagar.config(image=imagen_tk, compound="left", padx=10)
        boton_pagar.image = imagen_tk
        boton_pagar.place(x=20, y=550, width=180, height=40)

        ruta=self.rutas(r"icono/ver.png")
        imagen_pil = Image.open(ruta)
        imagen_resize2 = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize2)

        boton_ver_ventas = tk.Button(self, text="Ver Ventas", font="sans 14 bold", bg="#dddddd", command=self.ver_ventas_realizadas)
        boton_ver_ventas.config(image=imagen_tk, compound="left", padx=10)
        boton_ver_ventas.image = imagen_tk
        boton_ver_ventas.place(x=220, y=550, width=180, height=40)