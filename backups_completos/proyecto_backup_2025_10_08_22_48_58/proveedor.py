import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
import datetime
import sys
import os

class Proveedor(tk.Frame):
    db_name = "database.db"

    def __init__(self, padre):
        super().__init__(padre)
        self.widgets()

    def rutas(self,ruta):
        try:
            rutabase=sys.__MEIPASS
        except Exception:
            rutabase=os.path.abspath(".")
        return os.path.join(rutabase,ruta)

    def widgets(self):

        self.frame1 = tk.Frame(self, bg="#C6D9E3",highlightbackground="gray", highlightthickness=1)
        self.frame1.place(x=0, y=0, width=1100, height=610)  # Ajuste de altura a 260
        
        ruta=self.rutas(r"icono/proveedores.png")
        imagen_pil = Image.open(ruta)
        imagen_resize = imagen_pil.resize((100, 100))
        imagen_tk = ImageTk.PhotoImage(imagen_resize)
        
        btn1 = tk.Button(self.frame1, text="Registro \nde proveedores", font="sans 14 bold", bg="#dddddd",command=self.proveedores)
        btn1.config(image=imagen_tk, compound="top", pady=10)
        btn1.image = imagen_tk
        btn1.place(x=300, y=120, width=200, height=200)

        ruta=self.rutas(r"icono/pedido.png")
        imagen_pil = Image.open(ruta)
        imagen_resize = imagen_pil.resize((100, 100))
        imagen_tk = ImageTk.PhotoImage(imagen_resize)
        
        btn4 = tk.Button(self.frame1, text="Registro \nde pedidos", font="sans 14 bold", bg="#dddddd",command=self.pedidos_a_proveedores)
        btn4.config(image=imagen_tk, compound="top", pady=10)
        btn4.image = imagen_tk
        btn4.place(x=600, y=120, width=200, height=200)

    def proveedores(self):
        ventana = tk.Toplevel(self)  
        ventana.title("Registro de proveedores")
        ventana.geometry("1100x650+120+20")
        ventana.config(bg="#C6D9E3")
        ventana.resizable(False, False)
        ventana.transient(self.master)
        ventana.grab_set()
        ventana.focus_set()
        ventana.lift()

        titulo = tk.Label(ventana, text="REGISTRO DE PROVEEDORES", font="sans 30 bold", bg="#dddddd", anchor="center", highlightbackground="gray", highlightthickness=1)
        titulo.place(x=0, y=0, width=1100, height=90)
        
        labelframe = tk.LabelFrame(ventana, text="Registrar proveedor", font="sans 22 bold", bg="#C6D9E3")
        labelframe.place(x=20, y=120, width=400, height=500)

        lblnombre = Label(labelframe, text="Nombre: ", font="sans 14 bold", bg="#C6D9E3")
        lblnombre.place(x=10, y=20)
        self.nombre = ttk.Entry(labelframe, font="sans 14 bold")
        self.nombre.place(x=140, y=20, width=240, height=40)

        lblidentificacion = Label(labelframe, text="Identificación: ", font="sans 14 bold", bg="#C6D9E3")
        lblidentificacion.place(x=10, y=80)
        self.identificacion = ttk.Entry(labelframe, font="sans 14 bold")
        self.identificacion.place(x=140, y=80, width=240, height=40)

        lblcelular = Label(labelframe, text="Celular: ", font="sans 14 bold", bg="#C6D9E3")
        lblcelular.place(x=10, y=140)
        self.celular = ttk.Entry(labelframe, font="sans 14 bold")
        self.celular.place(x=140, y=140, width=240, height=40)

        lbldireccion = Label(labelframe, text="Dirección: ", font="sans 14 bold", bg="#C6D9E3")
        lbldireccion.place(x=10, y=200)
        self.direccion = ttk.Entry(labelframe, font="sans 14 bold")
        self.direccion.place(x=140, y=200, width=240, height=40)

        lblcorreo = Label(labelframe, text="Correo: ", font="sans 14 bold", bg="#C6D9E3")
        lblcorreo.place(x=10, y=260)
        self.correo = ttk.Entry(labelframe, font="sans 14 bold")
        self.correo.place(x=140, y=260, width=240, height=40)

        ruta = self.rutas(r"icono/ingresarc.png")
        imagen_pil = Image.open(ruta)
        imagen_resize = imagen_pil.resize((50, 50))
        imagen_tk = ImageTk.PhotoImage(imagen_resize)

        btn1 = Button(labelframe, bg="#dddddd", fg="black", text="Registrar", font="roboto 12 bold", command=self.registrar_proveedor)
        btn1.config(image=imagen_tk, compound="top", padx=10)
        btn1.image = imagen_tk
        btn1.place(x=50, y=340,width=80, height=80)
        
        ruta=self.rutas(r"icono/eliminar.png")
        imagen_pil = Image.open(ruta)
        imagen_resize1 = imagen_pil.resize((50, 50))
        imagen_tk = ImageTk.PhotoImage(imagen_resize1)
        
        btn_eliminar = Button(labelframe, bg="#dddddd", fg="black", text="Eliminar", font="roboto 12 bold", command=self.eliminar)
        btn_eliminar.config(image=imagen_tk, compound="top", padx=10)
        btn_eliminar.image = imagen_tk
        btn_eliminar.place(x=150, y=340,width=80,height=80)
        
        ruta = self.rutas(r"icono/modificar.png")
        imagen_pil = Image.open(ruta)
        imagen_resize2 = imagen_pil.resize((50, 50))
        imagen_tk = ImageTk.PhotoImage(imagen_resize2)
        
        btn2 = Button(labelframe, bg="#dddddd", fg="black", text="Editar", font="roboto 12 bold", command=self.editar_proveedor)
        btn2.config(image=imagen_tk, compound="top", padx=10)
        btn2.image = imagen_tk
        btn2.place(x=250, y=340,width=80, height=80)

        #==============TreeView Tabla==========================================================================================================#
        treFrame = Frame(ventana, bg="white")  # Frame recuadro dentro de la ventana ventas
        treFrame.place(x=440, y=150, width=620, height=450)
        
        # Barra de desplazamiento vertical
        scrol_y = ttk.Scrollbar(treFrame)
        scrol_y.pack(side=RIGHT, fill=Y)

        # Barra de desplazamiento horizontal
        scrol_x = ttk.Scrollbar(treFrame, orient=HORIZONTAL)
        scrol_x.pack(side=BOTTOM, fill=X)
        
        self.tre = ttk.Treeview(treFrame, yscrollcommand=scrol_y.set, xscrollcommand=scrol_x.set, height=40, 
                                columns=("Nombre", "Identificación", "Celular", "Dirección", "Correo"), show="headings")
        self.tre.pack(expand=True, fill=BOTH)

        scrol_y.config(command=self.tre.yview)
        scrol_x.config(command=self.tre.xview)
        
        self.tre.heading("Nombre", text="Nombre")
        self.tre.heading("Identificación", text="Identificación")
        self.tre.heading("Celular", text="Celular")
        self.tre.heading("Dirección", text="Dirección")
        self.tre.heading("Correo", text="Correo")
        
        self.tre.column("Nombre", width=150, anchor="center")
        self.tre.column("Identificación", width=120, anchor="center")
        self.tre.column("Celular", width=120, anchor="center")
        self.tre.column("Dirección", width=200, anchor="center")
        self.tre.column("Correo", width=200, anchor="center")

        # Obtener datos de la base de datos
        self.cargar_proveedores()
        #===========================================================================================================================================#
        
    def pedidos_a_proveedores(self):
        ventana = tk.Toplevel(self)  
        ventana.title("Pedidos a proveedores")
        ventana.geometry("1100x650+120+20")
        ventana.config(bg="#C6D9E3")
        ventana.resizable(False, False)
        ventana.transient(self.master)
        ventana.grab_set()
        ventana.focus_set()
        ventana.lift()

        self.numero_pedido = 1  # Variable para mantener el número de pedido actual

        titulo = tk.Label(ventana, text="REGISTRO DE PEDIDOS", font="sans 30 bold", bg="#dddddd", anchor="center", highlightbackground="gray", highlightthickness=1)
        titulo.place(x=0, y=0, width=1100, height=90)

        labelframe = tk.LabelFrame(ventana, text="Registrar pedidos", font="sans 22 bold", bg="#C6D9E3")
        labelframe.place(x=20,y=120,width=400,height=500)

        lblpedido = Label(labelframe, text="N° Pedido: ", font="sans 14 bold", bg="#C6D9E3")
        lblpedido.place(x=10, y=20)
        self.pedido = Label(labelframe, text="", font="sans 14 bold", relief="groove")
        self.pedido.place(x=140,y=20,width=240,height=40)
        self.actualizar_numero_pedido()  # Actualizar el número de pedido inicial

        lblproveedor = Label(labelframe, text="Proveedor: ", font="sans 14 bold", bg="#C6D9E3")
        lblproveedor.place(x=10, y=80)
        self.proveedor = ttk.Combobox(labelframe, font="sans 14 bold",state="readonly")
        self.proveedor.place(x=140,y=80,width=240,height=40)

        self.cargar_proveedores_pedidos()

        lblproducto = Label(labelframe, text="Producto: ", font="sans 14 bold", bg="#C6D9E3")
        lblproducto.place(x=10, y=140)
        self.producto = ttk.Combobox(labelframe, font="sans 14 bold",state="readonly")
        self.producto.place(x=140,y=140,width=240,height=40)

        self.cargar_productos()

        lblcantidad = Label(labelframe, text="Nueva Cant: ", font="sans 14 bold", bg="#C6D9E3")
        lblcantidad.place(x=10, y=200)
        self.cantidad = ttk.Entry(labelframe, font="sans 14 bold")
        self.cantidad.place(x=140,y=200,width=240,height=40)

        ruta=self.rutas(r"icono/pedido.png")
        imagen_pil = Image.open(ruta)
        imagen_resize = imagen_pil.resize((50, 50))
        imagen_tk = ImageTk.PhotoImage(imagen_resize)

        btn1 = Button(labelframe, bg="#dddddd", fg="black", text="Agregar", font="roboto 12 bold",command=self.agregar_pedido)
        btn1.config(image=imagen_tk, compound="top", padx=10)
        btn1.image = imagen_tk
        btn1.place(x=50, y=280,width=80, height=80)
        
        ruta=self.rutas(r"icono/rpedido.png")
        imagen_pil = Image.open(ruta)
        imagen_resize1 = imagen_pil.resize((50, 50))
        imagen_tk = ImageTk.PhotoImage(imagen_resize1)

        btn2 = Button(labelframe, bg="#dddddd", fg="black", text="Registrar", font="roboto 12 bold",command=self.registrar_pedido)
        btn2.config(image=imagen_tk, compound="top", padx=10)
        btn2.image = imagen_tk
        btn2.place(x=150, y=280,width=80, height=80)

        ruta=self.rutas(r"icono/verpedidos.png")
        imagen_pil = Image.open(ruta)
        imagen_resize1 = imagen_pil.resize((50, 50))
        imagen_tk = ImageTk.PhotoImage(imagen_resize1)

        btn3 = Button(labelframe, bg="#dddddd", fg="black", text="Ver pedidos", font="roboto 12 bold",command=self.ver_pedidos)
        btn3.config(image=imagen_tk, compound="top", padx=10)
        btn3.image = imagen_tk
        btn3.place(x=250, y=280,width=100, height=80)

        #=========TreeView Tabla=========================================================================================#
        treFrame=Frame(ventana,bg="white") #frame recuadro dentro de la ventana ventas
        treFrame.place(x=440,y=150,width=620,height=450)
        
        # Barra de desplazamiento vertical
        scrol_y = ttk.Scrollbar(treFrame)
        scrol_y.pack(side=RIGHT, fill=Y)

        # Barra de desplazamiento horizontal
        scrol_x = ttk.Scrollbar(treFrame, orient=HORIZONTAL)
        scrol_x.pack(side=BOTTOM, fill=X)
        
        self.treeview = ttk.Treeview(treFrame, columns=("N° Pedido", "Proveedor", "Producto", "Cantidad", "Fecha", "Hora"), show="headings")
        self.treeview.pack(expand=True, fill=BOTH)

        scrol_y.config(command=self.treeview.yview)
        scrol_x.config(command=self.treeview.xview)

        # Configurar las columnas
        self.treeview.heading("N° Pedido", text="N° Pedido")
        self.treeview.heading("Proveedor", text="Proveedor")
        self.treeview.heading("Producto", text="Producto")
        self.treeview.heading("Cantidad", text="Cantidad")
        self.treeview.heading("Fecha", text="Fecha")
        self.treeview.heading("Hora", text="Hora")

        # Establecer el ancho de las columnas
        self.treeview.column("N° Pedido", width=80,anchor="center")
        self.treeview.column("Proveedor", width=100,anchor="center")
        self.treeview.column("Producto", width=100,anchor="center")
        self.treeview.column("Cantidad", width=100,anchor="center")
        self.treeview.column("Fecha", width=100,anchor="center")
        self.treeview.column("Hora", width=100,anchor="center")
        #============================================================================================================================================#

    def registrar_proveedor(self):
        # Obtener los datos de los Entry
        nombre = self.nombre.get()
        identificacion = self.identificacion.get()
        celular = self.celular.get()
        direccion = self.direccion.get()
        correo = self.correo.get()

        # Conexión a la base de datos
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        try:
            # Insertar los datos en la tabla proveedores, excepto en la columna id
            cursor.execute("INSERT INTO proveedores (nombre, identificacion, celular, direccion, correo) VALUES (?, ?, ?, ?, ?)",
                        (nombre, identificacion, celular, direccion, correo))

            # Confirmar la transacción y cerrar la conexión
            conn.commit()
            messagebox.showinfo("Éxito", "Proveedor registrado correctamente.")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se pudo registrar el proveedor: {e}")
        finally:
            conn.close()

        # Limpiar el Treeview antes de cargar los proveedores nuevamente
        for item in self.tre.get_children():
            self.tre.delete(item)

        # Limpiar los campos después de la inserción
        self.nombre.delete(0, END)
        self.identificacion.delete(0, END)
        self.celular.delete(0, END)
        self.direccion.delete(0, END)
        self.correo.delete(0, END)
        self.cargar_proveedores()

    def eliminar(self):
        if not self.tre.selection():
            messagebox.showerror("Error", "Por favor seleccione un proveedor para eliminar.")
            return
        
        # Mostrar cuadro de entrada para el PIN de seguridad
        pin = simpledialog.askstring("PIN de seguridad", "Ingrese el PIN de seguridad:", show='*')

        if not pin or len(pin) != 4 or not pin.isdigit():
            messagebox.showerror("Error", "PIN inválido. Debe ser un número de 4 dígitos.")
            return

        # Verificar que el PIN sea correcto (aquí puedes definir el PIN que desees)
        if pin != "2024":  # Cambia "1234" por el PIN que prefieras
            messagebox.showerror("Error", "PIN incorrecto.")
            return


        if messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar este proveedor?"):
            item = self.tre.selection()[0]
            id_proveedor = self.tre.item(item, "values")[0]

            # Eliminar registro de la base de datos
            try:
                conn = sqlite3.connect(self.db_name)
                cursor = conn.cursor()
                cursor.execute("DELETE FROM proveedores WHERE ID=?", (id_proveedor,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Éxito", "Proveedor eliminado correctamente.")
                self.tre.delete(item)
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"No se pudo eliminar el proveedor: {e}")
                self.cargar_proveedores()

    def editar_proveedor(self):
        # Obtener el item seleccionado en el Treeview
        seleccionado = self.tre.selection()
        if not seleccionado:
            messagebox.showerror("Error", "Por favor, seleccione un proveedor para editar.")
            return

        # Obtener los detalles del proveedor seleccionado
        item = seleccionado[0]
        detalles = self.tre.item(item, 'values')

        # Crear una ventana Toplevel para editar los detalles del proveedor
        ventana_editar = tk.Toplevel(self)
        ventana_editar.title("Editar Proveedor")
        ventana_editar.geometry("400x400")
        ventana_editar.config(bg="#C6D9E3")

        # Etiquetas y campos de entrada para editar los detalles
        lblnombre = tk.Label(ventana_editar, text="Nombre:", font="sans 14 bold", bg="#C6D9E3")
        lblnombre.grid(row=0, column=0, padx=10, pady=5)
        nombre_editar = ttk.Entry(ventana_editar, font="sans 14 bold")
        nombre_editar.grid(row=0, column=1, padx=10, pady=5)
        nombre_editar.insert(0, detalles[0])

        lblidentificacion = tk.Label(ventana_editar, text="Identificación:", font="sans 14 bold", bg="#C6D9E3")
        lblidentificacion.grid(row=1, column=0, padx=10, pady=5)
        identificacion_editar = ttk.Entry(ventana_editar, font="sans 14 bold")
        identificacion_editar.grid(row=1, column=1, padx=10, pady=5)
        identificacion_editar.insert(0, detalles[1])

        lblcelular = tk.Label(ventana_editar, text="Celular:", font="sans 14 bold", bg="#C6D9E3")
        lblcelular.grid(row=2, column=0, padx=10, pady=5)
        celular_editar = ttk.Entry(ventana_editar, font="sans 14 bold")
        celular_editar.grid(row=2, column=1, padx=10, pady=5)
        celular_editar.insert(0, detalles[2])

        lbldireccion = tk.Label(ventana_editar, text="Dirección:", font="sans 14 bold", bg="#C6D9E3")
        lbldireccion.grid(row=3, column=0, padx=10, pady=5)
        direccion_editar = ttk.Entry(ventana_editar, font="sans 14 bold")
        direccion_editar.grid(row=3, column=1, padx=10, pady=5)
        direccion_editar.insert(0, detalles[3])

        lblcorreo = tk.Label(ventana_editar, text="Correo:", font="sans 14 bold", bg="#C6D9E3")
        lblcorreo.grid(row=4, column=0, padx=10, pady=5)
        correo_editar = ttk.Entry(ventana_editar, font="sans 14 bold")
        correo_editar.grid(row=4, column=1, padx=10, pady=5)
        correo_editar.insert(0, detalles[4])

        # Función para guardar los cambios
        def guardar_cambios():
            # Obtener el ID del proveedor seleccionado
            proveedor_id = self.tre.item(item, 'text')

            # Obtener los nuevos valores
            nuevo_nombre = nombre_editar.get()
            nueva_identificacion = identificacion_editar.get()
            nuevo_celular = celular_editar.get()
            nueva_direccion = direccion_editar.get()
            nuevo_correo = correo_editar.get()

            # Actualizar los valores en el Treeview
            self.tre.item(item, values=(nuevo_nombre, nueva_identificacion, nuevo_celular, nueva_direccion, nuevo_correo))

            # Actualizar los valores en la base de datos
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            cursor.execute("UPDATE proveedores SET nombre=?, identificacion=?, celular=?, direccion=?, correo=? WHERE id=?",
                            (nuevo_nombre, nueva_identificacion, nuevo_celular, nueva_direccion, nuevo_correo, proveedor_id))

            conn.commit()
            conn.close()

            # Mostrar el mensaje de éxito
            messagebox.showinfo("Proveedor editado", "Proveedor editado correctamente.")

            # Cerrar la ventana de edición
            ventana_editar.destroy()
        
        # Botón para guardar los cambios
        ruta = self.rutas(r"icono/guardar.png")
        imagen_pil = Image.open(ruta)
        imagen_resize4 = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize4)
        
        btn_guardar = tk.Button(ventana_editar, text="Guardar Cambios", bg="#dddddd", fg="black", font="roboto 16 bold", command=guardar_cambios)
        btn_guardar.config(image=imagen_tk, compound="left", padx=10)
        btn_guardar.image = imagen_tk
        btn_guardar.grid(row=5, column=0, columnspan=2, pady=10)
        
    def cargar_proveedores(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM proveedores")
        rows = cursor.fetchall()
        for row in rows:
            self.tre.insert('', 'end', text=row[0], values=row[1:])
        conn.close()

    def cargar_proveedores_pedidos(self):
            try:
                conn = sqlite3.connect(self.db_name)
                c = conn.cursor()
                c.execute("SELECT nombre FROM proveedores")
                proveedores = c.fetchall()
                nombres_proveedores = [proveedor[0] for proveedor in proveedores]
                self.proveedor["values"] = nombres_proveedores
                conn.close()
            except sqlite3.Error as e:
                print("Error cargando proveedores:", e)
                
    def cargar_productos(self):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT articulo FROM articulos")
            products = c.fetchall()
            self.producto["values"] = [product[0] for product in products]
            conn.close()
        except sqlite3.Error as e:
            print("Error cargando productos:", e)
            
    def actualizar_fecha_y_hora(self):
        # Obtener la fecha y hora actual
        fecha_actual = datetime.datetime.now().strftime("%d-%m-%Y")
        hora_actual = datetime.datetime.now().strftime("%H:%M:%S")

        # Actualizar las etiquetas de fecha y hora
        self.label_fecha.config(text=fecha_actual)
        self.label_hora.config(text=hora_actual)

        # Llamar a este método nuevamente después de 1000 ms (1 segundo)
        self.after(1000, self.actualizar_fecha_y_hora)
        
    def actualizar_numero_pedido(self):
        # Conexión a la base de datos
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Obtener el último número de pedido registrado en la base de datos
        cursor.execute("SELECT MAX(numero_pedido) FROM pedidos")
        ultimo_pedido = cursor.fetchone()[0]

        # Si no hay pedidos registrados, establecer el número de pedido como 1
        if ultimo_pedido is None:
            self.numero_pedido = 1
        else:
            # Aumentar el número de pedido en 1
            self.numero_pedido = ultimo_pedido + 1

        # Actualizar la visualización del número de pedido en la interfaz de usuario
        self.pedido.config(text=str(self.numero_pedido))

        # Cerrar la conexión a la base de datos
        conn.close()

    def registrar_pedido(self):
        # Verificar si el Treeview está vacío
        if not self.treeview.get_children():
            messagebox.showerror("Error", "Agregue primero un producto para el pedido.")
            return  # Terminar la función si el Treeview está vacío

        # Conexión a la base de datos
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()

        # Recorrer los elementos del Treeview y guardarlos en la base de datos
        for child in self.treeview.get_children():
            pedido = self.treeview.item(child)['values']
            numero_pedido, proveedor, producto, cantidad, fecha, hora = pedido
            
            # Insertar el pedido en la tabla 'pedidos'
            cursor.execute("INSERT INTO pedidos (numero_pedido, proveedor, producto, cantidad, fecha, hora) VALUES (?, ?, ?, ?, ?, ?)", pedido)
            
            # Actualizar el stock en la tabla 'inventario'
            cursor.execute("UPDATE articulos SET stock = stock + ? WHERE articulo = ?", (cantidad, producto))

        # Confirmar la transacción y cerrar la conexión
        conn.commit()
        conn.close()

        # Limpiar el Treeview
        self.treeview.delete(*self.treeview.get_children())

        # Mostrar un mensaje de confirmación
        messagebox.showinfo("Pedido registrado", "El pedido ha sido registrado exitosamente.")
        
        # Actualizar la visualización del número de pedido
        self.actualizar_numero_pedido()
        
    def agregar_pedido(self):
        # Aquí iría tu lógica para obtener los datos del pedido, como el proveedor, producto y cantidad
        proveedor = self.proveedor.get()  # Obtener el proveedor seleccionado
        producto = self.producto.get()  # Obtener el producto seleccionado
        cantidad = self.cantidad.get()  # Obtener la cantidad ingresada
        
        # Verificar si se han ingresado todos los datos necesarios
        if proveedor and producto and cantidad:
            # Llamar a la función para agregar el pedido al Treeview
            self.agregar_pedido_a_treeview(proveedor, producto, cantidad)
            
            # Limpiar los campos después de agregar el pedido
            self.proveedor.set("")  # Limpiar el proveedor seleccionado
            self.producto.set("")    # Limpiar el producto seleccionado
            self.cantidad.delete(0, "end")  # Limpiar la cantidad ingresada
        else:
            messagebox.showerror("Error", "Por favor, complete todos los campos.")
               
    def agregar_pedido_a_treeview(self, proveedor, producto, cantidad):
        # Obtener el número de pedido actual
        n_pedido = self.numero_pedido
        
        # Obtener la fecha y hora actual
        fecha_actual = datetime.datetime.now().strftime("%d-%m-%Y")
        hora_actual = datetime.datetime.now().strftime("%H:%M:%S")
        
        # Insertar los datos del pedido en el Treeview con el mismo número de pedido
        self.treeview.insert("", "end", values=(n_pedido, proveedor, producto, cantidad, fecha_actual, hora_actual))
        
    def ver_pedidos(self):
        # Crear el Toplevel
        top_pedidos = Toplevel(self)
        top_pedidos.title("Lista de Pedidos Registrados")
        top_pedidos.geometry("800x600")  # Definir el tamaño del Toplevel
        top_pedidos.config(bg="#C6D9E3")  # Configurar el color de fondo del Toplevel
        top_pedidos.resizable(False, False)
        top_pedidos.transient(self.master)
        top_pedidos.grab_set()
        top_pedidos.focus_set()
        top_pedidos.lift()

        # Crear el Label "Pedidos Registrados"
        label_pedidos = tk.Label(top_pedidos, text="Pedidos Registrados", font="sans 22 bold", bg="#C6D9E3")
        label_pedidos.pack(pady=10)  # Ajustar el espaciado vertical

        # Crear el Treeview
        tree_pedidos = ttk.Treeview(top_pedidos, show="headings")
        tree_pedidos['columns'] = ('N° Pedido', 'Proveedor', 'Producto', 'Cantidad', 'Fecha', 'Hora')
        tree_pedidos.column("#0", anchor='center', width=100)
        tree_pedidos.column('#1', anchor='center', width=100)
        tree_pedidos.column('#2', anchor='center', width=100)
        tree_pedidos.column('#3', anchor='center', width=100)
        tree_pedidos.column('#4', anchor='center', width=100)
        tree_pedidos.column('#5', anchor='center', width=150)
        tree_pedidos.column('#6', anchor='center', width=150)

        #tree_pedidos.heading("#0", text='ID')
        tree_pedidos.heading('#1', text='N° Pedido')
        tree_pedidos.heading('#2', text='Proveedor')
        tree_pedidos.heading('#3', text='Producto')
        tree_pedidos.heading('#4', text='Cantidad')
        tree_pedidos.heading('#5', text='Fecha')
        tree_pedidos.heading('#6', text='Hora')

        # Obtener datos de la base de datos
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pedidos")
        rows = cursor.fetchall()
        for row in rows:
            tree_pedidos.insert('', 'end', text=row[0], values=row[1:])
        conn.close()

        # Ubicar el Treeview en el Toplevel usando place con coordenadas absolutas
        tree_pedidos.place(x=50, y=100, width=700, height=450)  # Ajustar las coordenadas y el tamaño según sea necesario

        # Asegurar que el Treeview tenga barras de desplazamiento vertical
        scroll_y_pedidos = ttk.Scrollbar(top_pedidos, orient='vertical', command=tree_pedidos.yview)
        scroll_y_pedidos.place(x=750, y=100, height=450)  # Ubicar la barra de desplazamiento vertical
        tree_pedidos.config(yscrollcommand=scroll_y_pedidos.set)
 