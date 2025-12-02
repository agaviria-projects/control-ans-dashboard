from pathlib import Path
import re

def obtener_ultimo_corte():
    RUTA_BASE = Path("data")

    if not RUTA_BASE.exists():
        raise Exception("❌ La carpeta 'data' no existe en el proyecto.")

    # ================================================
    # 1) Buscar carpetas con formato de fecha (dd-mm-yyyy)
    # ================================================
    carpetas_fecha = [
        p for p in RUTA_BASE.iterdir()
        if p.is_dir() and re.match(r"\d{2}-\d{2}-\d{4}", p.name)
    ]

    archivos = []

    # ================================================
    # 2) Si existen carpetas por fecha → buscar allí
    # ================================================
    if carpetas_fecha:
        # Ordenar por nombre para tomar la fecha más reciente
        carpeta_reciente = sorted(carpetas_fecha)[-1]

        # Extensiones permitidas
        patrones = ["*.xlsx", "*.xlsm"]

        for patron in patrones:
            archivos.extend(list(carpeta_reciente.glob(patron)))

        if not archivos:
            raise Exception(f"❌ No hay archivos Excel dentro de {carpeta_reciente}")

        # Tomar el archivo más reciente por fecha de modificación
        return max(archivos, key=lambda x: x.stat().st_mtime)

    # ================================================
    # 3) Si NO hay carpetas por fecha → buscar en data/
    # ================================================
    patrones = ["*.xlsx", "*.xlsm"]
    archivos = []

    for patron in patrones:
        archivos.extend(list(RUTA_BASE.glob(patron)))

    if not archivos:
        raise Exception("❌ No hay archivos Excel en la carpeta 'data'.")

    return max(archivos, key=lambda x: x.stat().st_mtime)


# ===== PRUEBA LOCAL =====
if __name__ == "__main__":
    ruta = obtener_ultimo_corte()
    print("📌 Último corte encontrado:")
    print(ruta)
