from pathlib import Path

def obtener_ultimo_corte():
    # Ruta base SIEMPRE relativa al proyecto
    RUTA_BASE = Path("data")

    if not RUTA_BASE.exists():
        raise Exception("❌ La carpeta 'data' no existe en el proyecto.")

    # Buscar archivos .xlsx dentro de /data
    archivos = list(RUTA_BASE.glob("*.xlsx"))
    if not archivos:
        raise Exception("❌ No hay archivos .xlsx en la carpeta 'data'.")

    # Tomar el archivo más reciente
    archivo_reciente = max(archivos, key=lambda x: x.stat().st_mtime)
    return archivo_reciente


# ===== PRUEBA LOCAL =====
if __name__ == "__main__":
    ruta = obtener_ultimo_corte()
    print("📌 Último corte encontrado:")
    print(ruta)
