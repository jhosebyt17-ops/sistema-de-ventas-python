import unittest
import sqlite3
import os
from reportes import Reportes
import tkinter as tk

print("🔍 Iniciando pruebas del módulo de Reportes...\n")

class TestReportes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Crear ventana raíz de Tkinter (necesaria para los componentes de reportes)
        cls.root = tk.Tk()
        cls.root.withdraw()  # Ocultar ventana
        cls.app = Reportes(cls.root)

        # Asegurar que la base de datos exista
        cls.db_name = "database.db"
        if not os.path.exists(cls.db_name):
            raise FileNotFoundError("❌ La base de datos 'database.db' no existe en el directorio del proyecto.")

    def test_conexion_bd(self):
        """Verifica conexión a la base de datos."""
        try:
            conn = sqlite3.connect(self.db_name)
            conn.close()
            print("✅ Conexión a la base de datos exitosa")
        except Exception as e:
            self.fail(f"❌ Error conectando a la base de datos: {e}")

    def test_tabla_ventas_existe(self):
        """Verifica que la tabla 'ventas' exista."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ventas'")
        existe = cursor.fetchone()
        conn.close()
        self.assertIsNotNone(existe, "❌ La tabla 'ventas' no existe.")
        print("✅ Tabla 'ventas' detectada correctamente")

    def test_tabla_articulos_existe(self):
        """Verifica que la tabla 'articulos' exista."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='articulos'")
        existe = cursor.fetchone()
        conn.close()
        self.assertIsNotNone(existe, "❌ La tabla 'articulos' no existe.")
        print("✅ Tabla 'articulos' detectada correctamente")

    def test_format_currency(self):
        """Verifica formato de moneda."""
        valor = 1234567.89
        resultado = self.app.format_currency(valor)
        self.assertEqual(resultado, "1,234,567.89")
        print("✅ Formato de moneda correcto")

    def test_eje_consulta(self):
        """Verifica ejecución de una consulta simple."""
        cursor = self.app.eje_consulta("SELECT 1")
        self.assertIsNotNone(cursor)
        print("✅ Ejecución de consulta básica exitosa")

    def test_calculo_inventario(self):
        """Verifica que calcular_costo_total funcione sin errores."""
        try:
            self.app.tabla_costo_inventario = tk.ttk.Treeview()
            self.app.calcular_costo_total()
            print("✅ Cálculo de costo total de inventario ejecutado correctamente")
        except Exception as e:
            self.fail(f"❌ Error en calcular_costo_total: {e}")

    def test_calculo_costo_ventas(self):
        """Verifica que calcular_costo_total_ventas funcione sin errores."""
        try:
            self.app.tabla_costo_ventas = tk.ttk.Treeview()
            self.app.entry_desde_ventas = tk.Entry()
            self.app.entry_hasta_ventas = tk.Entry()
            self.app.entry_desde_ventas.insert(0, "2024-01-01")
            self.app.entry_hasta_ventas.insert(0, "2025-12-31")
            self.app.calcular_costo_total_ventas()
            print("✅ Cálculo de costo total de ventas ejecutado correctamente")
        except Exception as e:
            self.fail(f"❌ Error en calcular_costo_total_ventas: {e}")

if __name__ == "__main__":
    unittest.main()
