import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from tkcalendar import DateEntry
import threading
import babel.numbers
import sys
import os
import re

class Inventario(tk.Frame):
    db_name = "database.db"
    
    def __init__(self, padre):
        super().__init__(padre)
        self.widgets()
        self.articulos_combobox()
        self.cargar_articulos()
        self.timer_articulos = None
        
        # Carpeta para almacenar las imágenes
        self.image_folder = "fotos"
        if not os.path.exists(self.image_folder):
            os.makedirs(self.image_folder)
            
    def rutas(self,ruta):
        try:
            rutabase=sys.__MEIPASS
        except Exception:
            rutabase=os.path.abspath(".")
        return os.path.join(rutabase,ruta)

    def widgets(self):
        
        #==============================================================================================================#   
        canva_articulos = tk.LabelFrame(self, text="Articulos", font="arial 14 bold", bg="#C6D9E3")
        canva_articulos.place(x=300, y=10, width=780, height=580)
        
        self.canvas = tk.Canvas(canva_articulos, bg="#C6D9E3")
        self.scrollbar = tk.Scrollbar(canva_articulos, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#C6D9E3")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        #==============================================================================================================#
        lblframe_buscar = LabelFrame(self, text="Buscar", font="arial 14 bold", bg="#C6D9E3")
        lblframe_buscar.place(x=10, y=10, width=280, height=80)
        
        self.comboboxbuscar = ttk.Combobox(lblframe_buscar, font="arial 12")
        self.comboboxbuscar.place(x=5, y=5, width=260, height=40)
        self.comboboxbuscar.bind("<<ComboboxSelected>>", self.on_combobox_select)
        self.comboboxbuscar.bind("<KeyRelease>", self.filtrar_articulos)
        
        #==============================================================================================================#
        lblframe_seleccion = tk.LabelFrame(self, text="Selección", font="arial 14 bold",bg="#C6D9E3")
        lblframe_seleccion.place(x=10, y=95, width=280, height=190)
        
        self.label1 = tk.Label(lblframe_seleccion, text="Articulo: ", font="arial 12", bg="#C6D9E3", wraplength=300)
        self.label1.place(x=5, y=5)
        
        self.label2 = tk.Label(lblframe_seleccion, text="Precio: ", font="arial 12", bg="#C6D9E3")
        self.label2.place(x=5, y=40)
        
        self.label3 = tk.Label(lblframe_seleccion, text="Costo: ", font="arial 12", bg="#C6D9E3")
        self.label3.place(x=5, y=70)
        
        self.label4 = tk.Label(lblframe_seleccion, text="Stock: ", font="arial 12", bg="#C6D9E3")
        self.label4.place(x=5, y=100)
        
        self.label5 = tk.Label(lblframe_seleccion, text="Estado: ", font="arial 12", bg="#C6D9E3")
        self.label5.place(x=5, y=130)
        
        #==============================================================================================================#
        lblframe_botones = LabelFrame(self, bg="#C6D9E3", text="Opciones", font="arial 14 bold")
        lblframe_botones.place(x=10, y=290, width=280, height=300)
        
        ruta=self.rutas(r"icono/ingresara.png")
        imagen_pil = Image.open(ruta)
        imagen_resize = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize)
        
        btn1 = tk.Button(lblframe_botones, text="Agregar", font="arial 14 bold", command=self.agregar_articulo)
        btn1.config(image=imagen_tk, compound=LEFT, padx=10)
        btn1.image = imagen_tk
        btn1.place(x=20, y=10, width=240, height=40)
        
        ruta=self.rutas(r"icono/editar.png")
        imagen_pil = Image.open(ruta)
        imagen_resize = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize)
        
        btn2 = tk.Button(lblframe_botones, text="Editar", font="arial 14 bold", command=self.editar_articulo)
        btn2.config(image=imagen_tk, compound=LEFT, padx=10)
        btn2.image = imagen_tk
        btn2.place(x=20, y=60, width=240, height=40)
        #==============================================================================================================#
    
    def articulos_combobox(self):
        # Cargar artículos desde la base de datos al iniciar
        self.con = sqlite3.connect('database.db')
        self.cur = self.con.cursor()
        self.cur.execute("SELECT articulo FROM articulos")
        self.articulos = [row[0] for row in self.cur.fetchall()]
        self.comboboxbuscar['values'] = self.articulos
        
    def filtrar_articulos(self, event):
        if self.timer_articulos:
            self.timer_articulos.cancel()
        self.timer_articulos = threading.Timer(0.5, self._filter_articulos)
        self.timer_articulos.start()

    def _filter_articulos(self):
        typed = self.comboboxbuscar.get()
        
        if typed == '':
            data = self.articulos
        else:
            data = [item for item in self.articulos if typed.lower() in item.lower()]
        
        # Actualiza los valores del combobox
        if data:
            self.comboboxbuscar['values'] = data
            self.comboboxbuscar.event_generate('<Down>')  # Mostrar la lista desplegable
        else:
            self.comboboxbuscar['values'] = ['No results found']
            self.comboboxbuscar.event_generate('<Down>')  # Mostrar la lista desplegable

        # Actualizar el canvas basado en el filtro aplicado
        self.cargar_articulos(filtro=typed)
        
    def cargar_articulos(self, filtro=None, categoria=None):
        # Ejecutar en el hilo principal
        self.after(0, self._cargar_articulos, filtro, categoria)

    def _cargar_articulos(self, filtro=None, categoria=None):
        # Limpiar el canvas antes de cargar los artículos
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # Consultar artículos en la base de datos con o sin filtro
        query = "SELECT articulo, precio, image_path FROM articulos"
        params = []
        
        if filtro:
            query += " WHERE articulo LIKE ?"
            params.append(f'%{filtro}%')
        
        self.cur.execute(query, params)
        articulos = self.cur.fetchall()
        
        self.row = 0
        self.column = 0
        
        for articulo, precio, image_path in articulos:
            self.mostrar_articulo(articulo, precio, image_path)
        
    def mostrar_articulo(self, articulo, precio, image_path):
        # Crear un frame para el artículo
        article_frame = tk.Frame(self.scrollable_frame, bg="white", relief="solid")
        article_frame.grid(row=self.row, column=self.column, padx=10, pady=10)
        
        # Mostrar la imagen en el frame
        if image_path and os.path.exists(image_path):
            image = Image.open(image_path)
            image = image.resize((150, 150), Image.LANCZOS)
            imagen = ImageTk.PhotoImage(image)
            image_label = tk.Label(article_frame, image=imagen)
            image_label.image = imagen  # Necesario para evitar que la imagen sea recolectada por el garbage collector
            image_label.pack(expand=True, fill="both")
        
        # Mostrar el nombre del artículo en el frame
        name_label = tk.Label(article_frame, text=articulo, bg="white", anchor="w", wraplength=150, font="arial 10 bold")
        name_label.pack(side="top", fill="x")
        
        # Mostrar el precio del artículo en el frame
        price_label = tk.Label(article_frame, text=f"Precio: {precio:,.2f}", bg="white", anchor="w", wraplength=150, font="arial 8 bold")
        price_label.pack(side="bottom", fill="x")
        
        # Actualizar la columna y fila para la próxima ubicación
        self.column += 1
        if self.column > 3:  # Cambiar a la siguiente fila después de 4 columnas
            self.column = 0
            self.row += 1
    
    def on_combobox_select(self, event):
        self.actualizar_label()
        
    def actualizar_label(self, event=None):
        articulo_seleccionado = self.comboboxbuscar.get()

        try:
            # Utiliza el cursor que ya has creado en lugar de crear uno nuevo
            self.cur.execute("SELECT articulo, precio, costo, stock, estado FROM articulos WHERE articulo=?", (articulo_seleccionado,))
            resultado = self.cur.fetchone()
            
            if resultado is not None:
                articulo, precio, costo, stock, estado = resultado
                
                # Actualizar las etiquetas con los datos del artículo
                self.label1.config(text=f"Articulo: {articulo}")
                self.label2.config(text=f"Precio: {precio}")
                self.label3.config(text=f"Costo: {costo}")
                self.label4.config(text=f"Stock: {stock}")
                
                # Actualizar el estado y cambiar el color del texto basado en el estado
                self.label5.config(text=f"Estado: {estado}")
                if estado.lower() == "activo":
                    self.label5.config(fg="green")
                elif estado.lower() == "inactivo":
                    self.label5.config(fg="red")
                else:
                    self.label5.config(fg="black")  # Default color if the state is neither 'activo' nor 'inactivo'
                
            else:
                # En caso de que no haya resultados, puedes limpiar o mostrar un mensaje en las etiquetas
                self.label1.config(text="Articulo: No encontrado")
                self.label2.config(text="Precio: N/A")
                self.label3.config(text="Costo: N/A")
                self.label4.config(text="Stock: N/A")
                self.label5.config(text="Estado: N/A", fg="black")
                
        except sqlite3.Error as e:
            print("Error al obtener los datos del artículo:", e)
            messagebox.showerror("Error", "Error al obtener los datos del artículo")
            
    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            # Cargar la imagen en la vista previa
            image = Image.open(file_path)
            image = image.resize((200, 200), Image.LANCZOS)
            image_name = os.path.basename(file_path)
            image_save_path = os.path.join(self.image_folder, image_name)
            image.save(image_save_path)
            
            self.image_tk = ImageTk.PhotoImage(image)
            
            self.product_image = self.image_tk
            self.image_path = image_save_path
            
            img_label = tk.Label(self.frameimg, image=self.image_tk)
            img_label.place(x=0, y=0, width=200, height=200)
            
    def agregar_articulo(self):
        # Crear la ventana secundaria
        top = tk.Toplevel(self)
        top.title("Agregar Artículo")
        top.geometry("700x400+200+50")
        top.config(bg="#C6D9E3")
        top.resizable(False, False)
        
        top.transient(self.master)
        top.grab_set()
        top.focus_set()
        top.lift()
        
        # Crear y colocar los campos de entrada y etiquetas
        tk.Label(top, text="Artículo: ", font="arial 12 bold", bg="#C6D9E3").place(x=20, y=20, width=80, height=25)
        entry_articulo = ttk.Entry(top, font="arial 12 bold")
        entry_articulo.place(x=120, y=20, width=250, height=30)
        
        tk.Label(top, text="Precio: ", font="arial 12 bold", bg="#C6D9E3").place(x=20, y=60, width=80, height=25)
        entry_precio = ttk.Entry(top, font="arial 12 bold")
        entry_precio.place(x=120, y=60, width=250, height=30)
        
        tk.Label(top, text="Costo: ", font="arial 12 bold", bg="#C6D9E3").place(x=20, y=100, width=80, height=25)
        entry_costo = ttk.Entry(top, font="arial 12 bold")
        entry_costo.place(x=120, y=100, width=250, height=30)
        
        tk.Label(top, text="Stock: ", font="arial 12 bold", bg="#C6D9E3").place(x=20, y=140, width=80, height=25)
        entry_stock = ttk.Entry(top, font="arial 12 bold")
        entry_stock.place(x=120, y=140, width=250, height=30)
        
        tk.Label(top, text="Estado: ", font="arial 12 bold", bg="#C6D9E3").place(x=20, y=180, width=80, height=25)
        entry_estado = ttk.Combobox(top, values=["Activo", "Inactivo"], state="readonly", font="arial 12 bold")
        entry_estado.place(x=120, y=180, width=250, height=30)
        
        self.frameimg = tk.Frame(top, bg="white", highlightbackground="gray", highlightthickness=1)
        self.frameimg.place(x=440, y=30, width=200, height=200)
        
        ruta=self.rutas(r"icono/foto.png")
        imagen_pil = Image.open(ruta)
        imagen_resize = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize)

        btnimagen = tk.Button(top, text="Cargar Imagen", font="arial 12 bold", command=self.load_image)
        btnimagen.config(image=imagen_tk, compound=LEFT, padx=10)
        btnimagen.image = imagen_tk
        btnimagen.place(x=450, y=260, width=200, height=40)
        
        def guardar():
            # Obtener datos de los campos de entrada
            articulo = entry_articulo.get()
            precio = entry_precio.get()
            costo = entry_costo.get()
            stock = entry_stock.get()
            estado = entry_estado.get()
            
            # Validar datos
            if not articulo or not precio or not costo or not stock or not estado:
                messagebox.showerror("Error", "Todos los campos deben ser completados")
                return

            # Validar que precio y costo no contengan comas
            if ',' in precio or ',' in costo:
                messagebox.showwarning("Advertencia", "No coloque comas. Solo utilice punto si requiere decimales.")
                return  # Salir de la función si la entrada es incorrecta

            # Expresión regular para verificar si el precio y costo tienen hasta 2 decimales
            decimal_pattern = r'^\d+(\.\d{1,2})?$'

            # Validar que el precio y costo sigan el formato de hasta 2 decimales
            if not re.match(decimal_pattern, precio) or not re.match(decimal_pattern, costo):
                messagebox.showwarning("Advertencia", "El precio y el costo deben tener un máximo de dos decimales.")
                return  # Salir de la función si el formato no es correcto
            
            # Intentar convertir precio, costo y stock a números
            try:
                precio = float(precio)
                costo = float(costo)
                stock = int(stock)
            except ValueError:
                messagebox.showerror("Error", "Precio, costo y stock deben ser números válidos")
                return
            
            # Guardar la ruta de la imagen seleccionada o usar la imagen por defecto
            if hasattr(self, 'image_path'):
                image_path = self.image_path
            else:
                ruta=self.rutas(r"fotos/default.png")
                image_path = ruta  # Ruta de la imagen por defecto
            
            # Insertar datos en la base de datos
            try:
                self.cur.execute("INSERT INTO articulos (articulo, precio, costo, stock, estado, image_path) VALUES (?, ?, ?, ?, ?, ?)", 
                                 (articulo, precio, costo, stock, estado, image_path))
                self.con.commit()
                messagebox.showinfo("Éxito", "Artículo agregado correctamente")
                top.destroy()
                self.cargar_articulos()
                self.articulos_combobox()
            except sqlite3.Error as e:
                print("Error al agregar el artículo:", e)
                messagebox.showerror("Error", "Error al agregar el artículo")
        
        ruta=self.rutas(r"icono/guardar.png")
        imagen_pil = Image.open(ruta)
        imagen_resize = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize)

        btnguardar = tk.Button(top, text="Guardar", font="arial 12 bold", command=guardar)
        btnguardar.config(image=imagen_tk, compound=LEFT, padx=10)
        btnguardar.image = imagen_tk
        btnguardar.place(x=50, y=260, width=150, height=40)

        ruta=self.rutas(r"icono/cancelar.png")
        imagen_pil = Image.open(ruta)
        imagen_resize = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize)

        btncancelar = tk.Button(top, text="Cancelar", font="arial 12 bold", command=top.destroy)
        btncancelar.config(image=imagen_tk, compound=LEFT, padx=10)
        btncancelar.image = imagen_tk
        btncancelar.place(x=250, y=260, width=150, height=40)
        
    def editar_articulo(self):
        selected_item = self.comboboxbuscar.get()
        
        if not selected_item:
            messagebox.showerror("Error", "Selecciona un artículo para editar")
            return
        
        # Obtener los datos del artículo seleccionado
        self.cur.execute("SELECT articulo, precio, costo, stock, estado, image_path FROM articulos WHERE articulo=?", (selected_item,))
        resultado = self.cur.fetchone()
        
        if not resultado:
            messagebox.showerror("Error", "Artículo no encontrado")
            return
        
        # Crear la ventana secundaria
        top = tk.Toplevel(self)
        top.title("Editar Artículo")
        top.geometry("700x400+200+50")
        top.config(bg="#C6D9E3")
        top.resizable(False, False)
        
        top.transient(self.master)
        top.grab_set()
        top.focus_set()
        top.lift()
        
        # Desempaquetar los datos
        (articulo, precio, costo, stock, estado, image_path) = resultado
        
        # Crear y colocar los campos de entrada y etiquetas con valores actuales
        tk.Label(top, text="Artículo: ", font="arial 12 bold", bg="#C6D9E3").place(x=20, y=20, width=80, height=25)
        entry_articulo = ttk.Entry(top, font="arial 12 bold")
        entry_articulo.place(x=120, y=20, width=250, height=30)
        entry_articulo.insert(0, articulo)
        
        tk.Label(top, text="Precio: ", font="arial 12 bold", bg="#C6D9E3").place(x=20, y=60, width=80, height=25)
        entry_precio = ttk.Entry(top, font="arial 12 bold")
        entry_precio.place(x=120, y=60, width=250, height=30)
        entry_precio.insert(0, precio)
        
        tk.Label(top, text="Costo: ", font="arial 12 bold", bg="#C6D9E3").place(x=20, y=100, width=80, height=25)
        entry_costo = ttk.Entry(top, font="arial 12 bold")
        entry_costo.place(x=120, y=100, width=250, height=30)
        entry_costo.insert(0, costo)
        
        tk.Label(top, text="Stock: ", font="arial 12 bold", bg="#C6D9E3").place(x=20, y=140, width=80, height=25)
        entry_stock = ttk.Entry(top, font="arial 12 bold")
        entry_stock.place(x=120, y=140, width=250, height=30)
        entry_stock.insert(0, stock)
        
        tk.Label(top, text="Estado: ", font="arial 12 bold", bg="#C6D9E3").place(x=20, y=180, width=80, height=25)
        entry_estado = ttk.Combobox(top, values=["Activo", "Inactivo"], state="readonly", font="arial 12 bold")
        entry_estado.place(x=120, y=180, width=250, height=30)
        if estado in ["Activo", "Inactivo"]:
            entry_estado.set(estado)
        
        self.frameimg = tk.Frame(top, bg="white", highlightbackground="gray", highlightthickness=1)
        self.frameimg.place(x=440, y=30, width=200, height=200)
        
        # Cargar la imagen existente si está disponible
        if image_path and os.path.exists(image_path):
            image = Image.open(image_path)
            image = image.resize((200, 200), Image.LANCZOS)
            self.product_image = ImageTk.PhotoImage(image)
            self.image_path = image_path
            # Crear un widget Label para mostrar la imagen
            image_label = tk.Label(self.frameimg, image=self.product_image)
            image_label.pack(expand=True, fill="both")
        
        ruta=self.rutas(r"icono/foto.png")
        imagen_pil = Image.open(ruta)
        imagen_resize = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize)
        
        btnimagen = tk.Button(top, text="Cargar Imagen", font="arial 12 bold", command=self.load_image)
        btnimagen.config(image=imagen_tk, compound=LEFT, padx=10)
        btnimagen.image = imagen_tk
        btnimagen.place(x=450, y=260, width=200, height=40)
        
        def guardar():
            # Obtener datos de los campos de entrada
            nuevo_articulo = entry_articulo.get()
            precio = entry_precio.get()
            costo = entry_costo.get()
            stock = entry_stock.get()
            estado = entry_estado.get()
            
            # Validar datos
            if not nuevo_articulo or not precio or not costo or not stock or not estado:
                messagebox.showerror("Error", "Todos los campos deben ser completados")
                return

            # Validar que precio y costo no contengan comas
            if ',' in precio or ',' in costo:
                messagebox.showwarning("Advertencia", "No coloque comas. Solo utilice punto si requiere decimales.")
                return  # Salir de la función si la entrada es incorrecta

            # Expresión regular para verificar si el precio y costo tienen hasta 2 decimales
            decimal_pattern = r'^\d+(\.\d{1,2})?$'

            # Validar que el precio y costo sigan el formato de hasta 2 decimales
            if not re.match(decimal_pattern, precio) or not re.match(decimal_pattern, costo):
                messagebox.showwarning("Advertencia", "El precio y el costo deben tener un máximo de dos decimales.")
                return  # Salir de la función si el formato no es correcto
            
            # Intentar convertir precio, costo y stock a números
            try:
                precio = float(precio)
                costo = float(costo)
                stock = int(stock)
            except ValueError:
                messagebox.showerror("Error", "Precio, costo y stock deben ser números válidos")
                return
            
            # Guardar la ruta de la imagen seleccionada o usar la imagen por defecto
            if hasattr(self, 'image_path'):
                image_path = self.image_path
            else:
                ruta=self.rutas(r"fotos/default.png")
                image_path = ruta  # Ruta de la imagen por defecto
            
            # Actualizar datos en la base de datos
            self.cur.execute("UPDATE articulos SET articulo=?, precio=?, costo=?, stock=?, image_path=?, estado=? WHERE articulo=?",
                            (nuevo_articulo, precio, costo, stock, image_path, estado, selected_item))
            self.con.commit()
            
            # Actualizar la lista de artículos en el combobox
            self.articulos_combobox()
            
            # Mostrar el artículo en el canvas
            self.after(0, lambda: self.cargar_articulos(filtro=nuevo_articulo))
            
            top.destroy()
            messagebox.showinfo("Éxito", "Artículo editado exitosamente")
        
        ruta=self.rutas(r"icono/guardar.png")
        imagen_pil = Image.open(ruta)
        imagen_resize = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize)
        
        btn_guardar = tk.Button(top, text="Guardar", font="arial 12 bold", command=guardar)
        btn_guardar.config(image=imagen_tk, compound=LEFT, padx=10)
        btn_guardar.image = imagen_tk
        btn_guardar.place(x=50, y=260, width=150, height=40)

        ruta=self.rutas(r"icono/cancelar.png")
        imagen_pil = Image.open(ruta)
        imagen_resize = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize)

        btncancelar = tk.Button(top, text="Cancelar", font="arial 12 bold", command=top.destroy)
        btncancelar.config(image=imagen_tk, compound=LEFT, padx=10)
        btncancelar.image = imagen_tk
        btncancelar.place(x=250, y=260, width=150, height=40)
        
