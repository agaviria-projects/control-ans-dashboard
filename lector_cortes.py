import os
from pathlib import Path

RUTA_BASE = Path(r"D:\CONTROL_ANS_INF")

def obtener_ultimo_corte():
    carpetas = [c for c in RUTA_BASE.iterdir() if c.is_dir()]
    if not carpetas:
        raise Exception("No hay carpetas de fechas en CONTROL_ANS_INF")

    carpeta_reciente = max(carpetas, key=lambda x: x.stat().st_mtime)

    archivos = list(carpeta_reciente.glob("*.xlsx"))
    if not archivos:
        raise Exception(f"No hay archivos en la carpeta {carpeta_reciente}")

    archivo_reciente = max(archivos, key=lambda x: x.stat().st_mtime)
    return archivo_reciente

# ======== PRUEBA ========
if __name__ == "__main__":
    ruta = obtener_ultimo_corte()
    print("📌 Último corte encontrado:")
    print(ruta)
