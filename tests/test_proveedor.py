import unittest
import sqlite3
import os

class TestProveedor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_path = os.path.join(os.path.dirname(__file__), '..', 'database.db')
        cls.conexion = sqlite3.connect(cls.db_path)
        cls.cursor = cls.conexion.cursor()
        print("🔍 Iniciando pruebas del módulo de Proveedores...")

        # Aseguramos limpiar pruebas previas
        cls.cursor.execute("DELETE FROM proveedores WHERE nombre='Proveedor Prueba'")
        cls.conexion.commit()

    def test_1_insertar_proveedor(self):
        """Prueba insertar un proveedor en la tabla proveedores"""
        try:
            datos = ("Proveedor Prueba", 1234567890, 3216549870, "Calle 123", "correo@prueba.com")
            self.cursor.execute("""
                INSERT INTO proveedores (nombre, identificacion, celular, direccion, correo)
                VALUES (?, ?, ?, ?, ?)
            """, datos)
            self.conexion.commit()

            self.cursor.execute("SELECT * FROM proveedores WHERE nombre=?", ("Proveedor Prueba",))
            proveedor = self.cursor.fetchone()
            self.assertIsNotNone(proveedor, "❌ No se insertó el proveedor correctamente.")
            print("✅ Inserción de proveedor exitosa.")
        except Exception as e:
            self.fail(f"Error al insertar proveedor: {e}")

    def test_2_consultar_proveedor(self):
        """Prueba consultar un proveedor existente"""
        self.cursor.execute("SELECT * FROM proveedores WHERE nombre='Proveedor Prueba'")
        proveedor = self.cursor.fetchone()
        self.assertIsNotNone(proveedor, "❌ No se encontró el proveedor en la base de datos.")
        print("✅ Consulta de proveedor exitosa.")

    def test_3_actualizar_proveedor(self):
        """Prueba actualizar los datos de un proveedor"""
        try:
            nuevo_correo = "proveedor_actualizado@correo.com"
            self.cursor.execute("""
                UPDATE proveedores SET correo=? WHERE nombre='Proveedor Prueba'
            """, (nuevo_correo,))
            self.conexion.commit()

            self.cursor.execute("SELECT correo FROM proveedores WHERE nombre='Proveedor Prueba'")
            resultado = self.cursor.fetchone()
            self.assertIsNotNone(resultado, "❌ No se encontró el proveedor para actualizar.")
            correo = resultado[0]
            self.assertEqual(correo, nuevo_correo, "❌ No se actualizó correctamente el correo del proveedor.")
            print("✅ Actualización de proveedor exitosa.")
        except Exception as e:
            self.fail(f"Error al actualizar proveedor: {e}")

    def test_4_eliminar_proveedor(self):
        """Prueba eliminar el proveedor de prueba"""
        try:
            self.cursor.execute("DELETE FROM proveedores WHERE nombre='Proveedor Prueba'")
            self.conexion.commit()
            self.cursor.execute("SELECT * FROM proveedores WHERE nombre='Proveedor Prueba'")
            eliminado = self.cursor.fetchone()
            self.assertIsNone(eliminado, "❌ No se eliminó el proveedor correctamente.")
            print("✅ Eliminación de proveedor exitosa.")
        except Exception as e:
            self.fail(f"Error al eliminar proveedor: {e}")

    @classmethod
    def tearDownClass(cls):
        cls.conexion.close()
        print("🔚 Pruebas del módulo de Proveedores finalizadas.\n")


if __name__ == "__main__":
    unittest.main(verbosity=2)
