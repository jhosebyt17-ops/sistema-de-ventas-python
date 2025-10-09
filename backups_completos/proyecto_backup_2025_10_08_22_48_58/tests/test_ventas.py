import unittest
import sqlite3
import os

DB_PATH = "database.db"

class TestVentas(unittest.TestCase):

    def setUp(self):
        """Conecta a la base de datos y prepara una venta de prueba antes de cada test"""
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()

        # Venta de prueba temporal
        self.venta_prueba = ("TEST-001", "Cliente Prueba", "Articulo Prueba", 1000.0, 2, 2000.0, "2025-10-08")

        # Insertar antes de cada prueba (si no existe)
        self.cursor.execute("DELETE FROM ventas WHERE factura = ?", (self.venta_prueba[0],))
        self.cursor.execute("""
            INSERT INTO ventas (factura, cliente, articulo, precio, cantidad, total, fecha)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, self.venta_prueba)
        self.conn.commit()

    def tearDown(self):
        """Elimina la venta de prueba después de cada test"""
        self.cursor.execute("DELETE FROM ventas WHERE factura = ?", ("TEST-001",))
        self.conn.commit()
        self.conn.close()

    def test_conexion_base_datos(self):
        """Prueba que la base de datos se conecte correctamente"""
        self.assertTrue(os.path.exists(DB_PATH), "No se encontró la base de datos.")
        print("✅ Conexión a la base de datos exitosa")

    def test_insertar_venta(self):
        """Verifica que la venta de prueba se haya insertado correctamente"""
        self.cursor.execute("SELECT * FROM ventas WHERE factura = ?", ("TEST-001",))
        venta = self.cursor.fetchone()
        self.assertIsNotNone(venta, "❌ No se insertó la venta correctamente.")
        print("✅ Inserción de venta exitosa")

    def test_consultar_venta(self):
        """Prueba consultar una venta existente"""
        self.cursor.execute("SELECT cliente, total FROM ventas WHERE factura = ?", ("TEST-001",))
        venta = self.cursor.fetchone()
        self.assertIsNotNone(venta, "❌ La venta no existe en la base de datos.")
        self.assertEqual(venta[0], "Cliente Prueba")
        print("✅ Consulta de venta exitosa")

    def test_actualizar_total(self):
        """Prueba actualizar el total de una venta"""
        nuevo_total = 2500.0
        self.cursor.execute("UPDATE ventas SET total = ? WHERE factura = ?", (nuevo_total, "TEST-001"))
        self.conn.commit()

        self.cursor.execute("SELECT total FROM ventas WHERE factura = ?", ("TEST-001",))
        total_actual = self.cursor.fetchone()[0]
        self.assertEqual(total_actual, nuevo_total, "❌ No se actualizó correctamente el total.")
        print("✅ Actualización de total exitosa")

    def test_eliminar_venta(self):
        """Prueba eliminar la venta de prueba"""
        self.cursor.execute("DELETE FROM ventas WHERE factura = ?", ("TEST-001",))
        self.conn.commit()

        self.cursor.execute("SELECT * FROM ventas WHERE factura = ?", ("TEST-001",))
        venta = self.cursor.fetchone()
        self.assertIsNone(venta, "❌ La venta no fue eliminada correctamente.")
        print("✅ Eliminación de venta exitosa")


if __name__ == "__main__":
    print("🔍 Iniciando pruebas del módulo de Ventas...\n")
    unittest.main(verbosity=2)

