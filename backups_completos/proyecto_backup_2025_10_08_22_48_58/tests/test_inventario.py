import unittest
import sqlite3
import os
import tkinter as tk
from inventario import Inventario

print("📦 Iniciando pruebas del módulo de Inventario...\n")

DB_PATH = os.path.join(os.getcwd(), "database.db")

class TestInventario(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("⚙️  Configurando entorno de pruebas para Inventario...")
        cls.db = sqlite3.connect(DB_PATH)
        cls.cursor = cls.db.cursor()
        # Crear tabla de artículos si no existe
        cls.cursor.execute('''
            CREATE TABLE IF NOT EXISTS articulos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                articulo TEXT NOT NULL,
                precio REAL NOT NULL,
                costo REAL NOT NULL,
                stock INTEGER NOT NULL,
                estado TEXT NOT NULL,
                image_path TEXT
            )
        ''')
        cls.db.commit()
        print("✅ Base de datos y tabla 'articulos' listas para pruebas")

    def setUp(self):
        # Crea un entorno de prueba sin interfaz visible
        self.root = tk.Tk()
        self.root.withdraw()
        self.app = Inventario(self.root)

    def tearDown(self):
        self.root.destroy()

    # -----------------------------------------------------------------------
    def test_tabla_articulos_existe(self):
        """📁 Verifica que la tabla 'articulos' exista en la base de datos"""
        self.cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='articulos'"
        )
        result = self.cursor.fetchone()
        self.assertIsNotNone(result, "La tabla 'articulos' debería existir.")
        print("✅ Tabla 'articulos' verificada correctamente")

    # -----------------------------------------------------------------------
    def test_insertar_articulo(self):
        """🧾 Verifica que se pueda insertar un artículo"""
        try:
            self.cursor.execute(
                "INSERT INTO articulos (articulo, precio, costo, stock, estado, image_path) VALUES (?, ?, ?, ?, ?, ?)",
                ("PruebaArticulo", 10.5, 5.0, 100, "Activo", "fotos/default.png"),
            )
            self.db.commit()
            self.cursor.execute("SELECT * FROM articulos WHERE articulo='PruebaArticulo'")
            result = self.cursor.fetchone()
            self.assertIsNotNone(result, "El artículo no fue insertado correctamente.")
            print("✅ Artículo insertado y verificado correctamente")
        except Exception as e:
            self.fail(f"❌ Error al insertar artículo: {e}")

    # -----------------------------------------------------------------------
    def test_filtrar_articulos_funciona(self):
        """🔍 Verifica que la función de filtrado no genere errores"""
        try:
            self.app.articulos = ["Manzana", "Banano", "Mango"]
            self.app.comboboxbuscar.set("Man")
            self.app._filter_articulos()
            valores = self.app.comboboxbuscar["values"]
            self.assertIn("Manzana", valores)
            print("✅ Filtrado de artículos funciona correctamente")
        except Exception as e:
            self.fail(f"❌ Error al ejecutar filtrado: {e}")

    # -----------------------------------------------------------------------
    def test_instancia_inventario(self):
        """🧩 Verifica que la clase Inventario se instancie correctamente"""
        self.assertIsInstance(self.app, Inventario)
        print("✅ Instancia de Inventario creada sin errores")

    # -----------------------------------------------------------------------
    def test_cargar_articulos(self):
        """📋 Verifica que cargar_articulos no genere errores"""
        try:
            self.app.cargar_articulos()
            print("✅ Método cargar_articulos ejecutado correctamente")
        except Exception as e:
            self.fail(f"❌ Error al ejecutar cargar_articulos: {e}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
