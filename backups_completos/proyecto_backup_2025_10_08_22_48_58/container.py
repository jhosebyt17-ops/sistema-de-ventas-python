from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
import tkinter as tk
from ventas import Ventas
from inventario import Inventario
from clientes import Clientes
from reportes import Reportes
from proveedor import Proveedor
from informacion import Informacion
import sys
import os

class Container(tk.Frame):
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.controlador = controlador
        self.pack()
        self.place(x=0, y=0, width=1100, height=650)
        self.widgets()
        self.frames = {}
        self.buttons = []  # Lista para mantener referencias a los botones
        for i in (Ventas, Inventario, Clientes, Reportes, Proveedor, Informacion):
            frame = i(self)
            self.frames[i] = frame
            frame.pack()
            frame.config(bg="#C6D9E3", highlightbackground="gray", highlightthickness=1)
            frame.place(x=0, y=40, width=1100, height=610)
        self.show_frames(Ventas)
 
    def rutas(self,ruta):
        try:
            rutabase=sys.__MEIPASS
        except Exception:
            rutabase=os.path.abspath(".")
        return os.path.join(rutabase,ruta)

    def show_frames(self, container):
        frame = self.frames[container]
        frame.tkraise()

    def ventas(self):
        self.show_frames(Ventas)

    def inventario(self):
        self.show_frames(Inventario)

    def clientes(self):
        self.show_frames(Clientes)

    def proveedor(self):
        self.show_frames(Proveedor)

    def reportes(self):
        self.show_frames(Reportes)
        
    def informacion(self):
        self.show_frames(Informacion)

    def widgets(self):  # botones parte izquierda
        
        frame2 = tk.Frame(self, bg="white")
        frame2.place(x=0, y=0, width=1100, height=40)

        # Crear botones y sus indicadores
        ruta=self.rutas(r"icono/btnventas.png")
        imagen_pil = Image.open(ruta)
        imagen_resize = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize)
        
        self.btn_ventas = Button(frame2, fg="black", text="Ventas", font="sans 16 bold", command=self.ventas)
        self.btn_ventas.config(image=imagen_tk, compound="left", padx=10)
        self.btn_ventas.image = imagen_tk
        self.btn_ventas.place(x=0, y=0, width=184, height=40)
        
        ruta=self.rutas(r"icono/btninventario.png")
        imagen_pil = Image.open(ruta)
        imagen_resize = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize)
        
        self.btn_inventario = Button(frame2, fg="black", text="Inventario", font="sans 16 bold", command=self.inventario)
        self.btn_inventario.config(image=imagen_tk, compound="left", padx=10)
        self.btn_inventario.image = imagen_tk
        self.btn_inventario.place(x=184, y=0, width=184, height=40)
        
        ruta=self.rutas(r"icono/btnclientes.png")
        imagen_pil = Image.open(ruta)
        imagen_resize = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize)
        
        self.btn_clientes = Button(frame2, fg="black", text="Clientes", font="sans 16 bold", command=self.clientes)
        self.btn_clientes.config(image=imagen_tk, compound="left", padx=10)
        self.btn_clientes.image = imagen_tk
        self.btn_clientes.place(x=369, y=0, width=184, height=40)
        
        ruta=self.rutas(r"icono/btnproveedor.png")
        imagen_pil = Image.open(ruta)
        imagen_resize = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize)
        
        self.btn_proveedor = Button(frame2, fg="black", text="Proveedor", font="sans 16 bold", command=self.proveedor)
        self.btn_proveedor.config(image=imagen_tk, compound="left", padx=10)
        self.btn_proveedor.image = imagen_tk
        self.btn_proveedor.place(x=554, y=0, width=184, height=40)
        
        ruta=self.rutas(r"icono/btnpedidos.png")
        imagen_pil = Image.open(ruta)
        imagen_resize = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize)
        
        self.btn_pedidos = Button(frame2, fg="black", text="Reportes", font="sans 16 bold", command=self.reportes)
        self.btn_pedidos.config(image=imagen_tk, compound="left", padx=10)
        self.btn_pedidos.image = imagen_tk
        self.btn_pedidos.place(x=739, y=0, width=184, height=40)  
        
        ruta=self.rutas(r"icono/btninformacion.png")
        imagen_pil = Image.open(ruta)
        imagen_resize = imagen_pil.resize((30, 30))
        imagen_tk = ImageTk.PhotoImage(imagen_resize)
        
        self.btn_informacion = Button(frame2, fg="black", text="Información", font="sans 16 bold", command=self.informacion)
        self.btn_informacion.config(image=imagen_tk, compound="left", padx=10)
        self.btn_informacion.image = imagen_tk
        self.btn_informacion.place(x=923, y=0, width=184, height=40) 
        
        self.buttons = [self.btn_ventas, self.btn_inventario, self.btn_clientes, self.btn_proveedor, self.btn_pedidos, self.btn_informacion]

