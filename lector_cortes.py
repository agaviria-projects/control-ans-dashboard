from pathlib import Path

def obtener_ultimo_corte():
    RUTA_BASE = Path("data")

    if not RUTA_BASE.exists():
        raise Exception("❌ La carpeta 'data' no existe en el proyecto.")

    # Aceptar .xlsx y .xlsm
    patrones = ["*.xlsx", "*.xlsm"]
    archivos = []

    for p in patrones:
        archivos.extend(list(RUTA_BASE.glob(p)))

    if not archivos:
        raise Exception("❌ No hay archivos .xlsx o .xlsm en la carpeta 'data'.")

    # Archivo más reciente
    archivo_reciente = max(archivos, key=lambda x: x.stat().st_mtime)
    return archivo_reciente


# ===== PRUEBA LOCAL =====
if __name__ == "__main__":
    ruta = obtener_ultimo_corte()
    print("📌 Último corte encontrado:")
    print(ruta)

