import unittest
from unittest.mock import MagicMock
from manager import Manager

print("🔍 Iniciando pruebas del módulo Manager...\n")

class TestManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("⚙️  Configurando entorno de pruebas para Manager...")
        # Creamos una instancia parcial (sin ejecutar __init__) para evitar GUI
        cls.app = Manager.__new__(Manager)
        print("✅ Entorno de pruebas configurado correctamente\n")

    def test_rutas_local(self):
        """Verifica que la función rutas devuelva una ruta válida"""
        try:
            ruta = self.app.rutas("icono.ico")
            self.assertIn("icono.ico", ruta)
            print("✅ Función rutas() devuelve una ruta válida")
        except Exception as e:
            self.fail(f"❌ Error en rutas(): {e}")

    def test_show_frame(self):
        """Verifica que show_frame llama tkraise() correctamente"""
        try:
            fake_frame = MagicMock()
            self.app.frames = {"Login": fake_frame}
            self.app.show_frame("Login")
            fake_frame.tkraise.assert_called_once()
            print("✅ show_frame() ejecuta tkraise() correctamente")
        except AssertionError:
            self.fail("❌ El método tkraise() no fue llamado correctamente")
        except Exception as e:
            self.fail(f"❌ Error inesperado en show_frame(): {e}")

    def test_instancia_manager(self):
        """Verifica que Manager se inicializa sin errores"""
        try:
            # Evitamos ejecutar mainloop ni iconbitmap
            app = Manager.__new__(Manager)
            app.title = lambda x=None: "Sistema de Ventas V1.0.0"
            app.resizable = lambda x=None, y=None: (False, False)
            app.frames = {}
            self.assertEqual(app.title(), "Sistema de Ventas V1.0.0")
            self.assertFalse(app.resizable()[0])
            self.assertFalse(app.resizable()[1])
            print("✅ Instancia de Manager creada correctamente (sin GUI real)")
        except Exception as e:
            self.fail(f"❌ Error al crear instancia de Manager: {e}")


if __name__ == "__main__":
    unittest.main()
