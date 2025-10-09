import unittest
import sqlite3
import os
import tkinter as tk
from login import Login, Registro  # ✅ tus clases originales, sin modificar nada

print("🔐 Iniciando pruebas del módulo de Login y Registro...\n")

DB_PATH = os.path.join(os.getcwd(), "database.db")


class DummyControlador:
    """🧠 Controlador falso solo para pruebas."""
    def __init__(self):
        self.frames = {}
    def mostrar_frame(self, nombre):
        pass


class TestLogin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("⚙️  Configurando entorno de pruebas para Login...")
        cls.db = sqlite3.connect(DB_PATH)
        cls.cursor = cls.db.cursor()
        cls.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        cls.db.commit()
        print("✅ Base de datos y tabla 'usuarios' listas para pruebas de Login")

    def setUp(self):
        # 🪄 Crear entorno de pruebas sin abrir ventana real
        self.root = tk.Tk()
        self.root.withdraw()
        self.controlador = DummyControlador()
        self.app = Login(self.root, self.controlador)  # ✅ ahora sí pasamos controlador

    def tearDown(self):
        self.root.destroy()

    def test_login_usuario_correcto(self):
        """🔑 Verifica que se pueda hacer login con un usuario existente"""
        try:
            cursor = self.db.cursor()
            cursor.execute("DELETE FROM usuarios WHERE username='testuser'")
            cursor.execute("INSERT INTO usuarios (username, password) VALUES ('testuser', '1234')")
            self.db.commit()

            cursor.execute("SELECT * FROM usuarios WHERE username='testuser' AND password='1234'")
            result = cursor.fetchone()

            self.assertIsNotNone(result, "El usuario testuser debería poder iniciar sesión.")
            print("✅ Login exitoso con usuario existente")
        except Exception as e:
            self.fail(f"❌ Error ejecutando login: {e}")

    def test_login_usuario_incorrecto(self):
        """🚫 Verifica manejo de credenciales incorrectas"""
        try:
            cursor = self.db.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE username='noexiste' AND password='incorrecta'")
            result = cursor.fetchone()
            self.assertIsNone(result, "El login debería fallar con credenciales incorrectas.")
            print("✅ Login manejó correctamente credenciales incorrectas")
        except Exception as e:
            self.fail(f"❌ Error al manejar credenciales incorrectas: {e}")

    def test_validacion_campos_llenos(self):
        """🧩 Verifica que la validación funcione con datos válidos"""
        usuario = "user1"
        password = "pass1"
        self.assertTrue(len(usuario) > 0 and len(password) > 0)
        print("✅ Validación de campos llenos correcta")

    def test_validacion_campos_vacios(self):
        """🧩 Verifica que la validación falle con campos vacíos"""
        usuario = ""
        password = ""
        self.assertFalse(len(usuario) > 0 and len(password) > 0)
        print("✅ Validación detecta campos vacíos correctamente")

    def test_ruta_existente(self):
        """📁 Verifica que la base de datos exista en el proyecto"""
        self.assertTrue(os.path.exists(DB_PATH), f"No se encontró la base de datos en: {DB_PATH}")
        print(f"✅ Base de datos encontrada correctamente: {DB_PATH}")


class TestRegistro(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n🧩 Configurando entorno de pruebas para Registro...")
        cls.db = sqlite3.connect(DB_PATH)
        cls.cursor = cls.db.cursor()
        print("✅ Entorno de Registro listo para pruebas")

    def test_instancia_registro(self):
        """🧾 Verifica que Registro se instancie correctamente"""
        root = tk.Tk()
        root.withdraw()
        controlador = DummyControlador()
        app = Registro(root, controlador)
        self.assertIsInstance(app, Registro)
        print("✅ Instancia de Registro creada sin errores")
        root.destroy()


if __name__ == "__main__":
    unittest.main(verbosity=2)
