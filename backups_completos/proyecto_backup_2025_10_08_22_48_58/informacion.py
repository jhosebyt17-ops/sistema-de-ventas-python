import tkinter as tk
from tkinter import ttk
import datetime
from PIL import Image, ImageTk
import sys
import os

class Informacion(tk.Frame):
    db_name = "database.db"

    def __init__(self, parent, user=None):
        super().__init__(parent)
        self.user = user  # Store the user
        self.widgets()
        
    def rutas(self,ruta):
        try:
            rutabase=sys.__MEIPASS
        except Exception:
            rutabase=os.path.abspath(".")
        return os.path.join(rutabase,ruta)

    def widgets(self):
        
        frame2 = tk.Frame(self, bg="#C6D9E3",highlightbackground="gray", highlightthickness=1)
        frame2.place(x=0, y=0, width=1100, height=650)
        
        ruta=self.rutas(r"imagenes/innova1.png")
        self.logo_image1 = Image.open(ruta)
        self.logo_image1 = self.logo_image1.resize((680, 180))
        self.logo_image1 = ImageTk.PhotoImage(self.logo_image1)
        self.logo_label1 = ttk.Label(frame2, image=self.logo_image1, background="#C6D9E3")
        self.logo_label1.place(x=220, y=40)
        
        # Texto de información sobre nosotros
        texto_informacion = """
        Sistema de Ventas V1.0.0 es una solución diseñada para optimizar la gestion comercial
        Ofrecemos herramientas eficientes y fáciles de usar para controlar inventario, ventas y clientes,
        brindando a nuestros usuarios una experiencia confiable y productiva.
        ¡Gracias por confiar en nosotros!
        
        Proyecto: Sistema de Ventas
        Version: 1.0.0
        Ultima actualizacion: 01/05/2025
        
        Soporte: jhoansmorales@ucundinamarca.edu.co / Jfernandorubio@ucundimarca.edu.co
        Celular: +57 3241852459 / +57 3204028440
        
        
        Copyright © 2025 Todos los derechos reservados
        """
        label_info = tk.Label(frame2, text=texto_informacion, font="sans 16", bg="#C6D9E3", justify="center")
        label_info.place(x=100, y=180)
 
        #===========================================================================================================================#
    