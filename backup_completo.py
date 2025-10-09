import os
import shutil
from datetime import datetime

def backup_completo():
    """
    Crea un respaldo completo del proyecto incluyendo:
    - Código fuente
    - Base de datos
    - Carpeta tests
    - Archivos auxiliares
    Además genera un registro (log) de la fecha y hora de creación del backup.
    """

    # Carpeta base del proyecto (directorio actual)
    carpeta_proyecto = os.getcwd()

    # Carpeta donde se guardarán los backups
    carpeta_backup = os.path.join(carpeta_proyecto, "backups_completos")
    os.makedirs(carpeta_backup, exist_ok=True)

    # Nombre del backup con la fecha y hora actuales
    fecha = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    nombre_backup = f"proyecto_backup_{fecha}"
    destino_backup = os.path.join(carpeta_backup, nombre_backup)

    try:
        # Crear copia completa del proyecto
        shutil.copytree(
            carpeta_proyecto,
            destino_backup,
            ignore=shutil.ignore_patterns(
                "*.pyc", "__pycache__", "backups_completos", ".git", ".vscode"
            ),
        )

        # Crear o actualizar archivo log de backups
        ruta_log = os.path.join(carpeta_backup, "registro_backups.txt")
        with open(ruta_log, "a", encoding="utf-8") as log:
            log.write(f"Backup creado el {fecha}: {destino_backup}\n")

        print(f"Backup completo creado exitosamente en: {destino_backup}")
        print(f"Registro actualizado en: {ruta_log}")

    except Exception as e:
        print(f"Ocurrió un error durante el backup: {e}")


if __name__ == "__main__":
    backup_completo()
