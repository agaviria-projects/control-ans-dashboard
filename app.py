import streamlit as st
import pandas as pd
from lector_cortes import obtener_ultimo_corte
import plotly.express as px

# ======================================
# CONFIGURACIÓN DEL DASHBOARD
# ======================================
st.set_page_config(page_title="Dashboard ANS", layout="wide")
st.title("📊 Dashboard Control ANS")

# ======================================
# OBTENER ARCHIVO MÁS RECIENTE
# ======================================
try:
    ruta_excel = obtener_ultimo_corte()

    st.markdown(
        f"""
        <div style='font-size:14px; color:#6c757d; margin-bottom:20px;'>
            📌 Corte activo → <b>{ruta_excel.name}</b>
        </div>
        """,
        unsafe_allow_html=True
    )

except Exception as e:
    st.error(f"❌ Error cargando archivo: {str(e)}")
    st.stop()

# ======================================
# LEER DATOS_ANS
# ======================================
try:
    df = pd.read_excel(ruta_excel, sheet_name="DATOS_ANS", header=3)
    df = df.loc[:, ~df.columns.str.contains("Unnamed")]
    df.reset_index(drop=True, inplace=True)

    # NORMALIZAR NOMBRES DE COLUMNAS
    df.columns = (
        df.columns.str.strip()
                  .str.upper()
                  .str.replace(" ", "_")
    )

    rename_dict = {
        "COORDENADAX": "X",
        "COORDENADA_X": "X",
        "LONGITUD": "X",
        "LON": "X",

        "COORDENADAY": "Y",
        "COORDENADA_Y": "Y",
        "LATITUD": "Y",
        "LAT": "Y",
    }

    df.rename(columns=rename_dict, inplace=True)

    # Convertir coordenadas coma → punto
    df["X"] = pd.to_numeric(df["X"].astype(str).str.replace(",", "."), errors="coerce")
    df["Y"] = pd.to_numeric(df["Y"].astype(str).str.replace(",", "."), errors="coerce")

    # ======================================================
    # NORMALIZACIÓN DEFINITIVA DE ESTADOS (CORRECCIÓN COLOR)
    # ======================================================
    def normalizar_estado(x):
        x = str(x).strip().upper()

        # ALERTA_0 en todas sus variantes
        if "ALERTA_0" in x:
            return "ALERTA_0"

        # A TIEMPO
        if "A TIEMPO" in x or "ATIEMPO" in x:
            return "A TIEMPO"

        # VENCIDO
        if "VENCIDO" in x:
            return "VENCIDO"

        # ALERTA (que no sea alerta 0)
        if "ALERTA" in x and "0" not in x:
            return "ALERTA"

        # SIN FECHA
        if "SIN FECHA" in x:
            return "SIN FECHA"

        return x

    df["ESTADO"] = df["ESTADO"].apply(normalizar_estado)

except Exception as e:
    st.error("❌ No se pudo leer DATOS_ANS.")
    st.write(str(e))
    st.stop()


# ======================================
# FUNCIONES DE FORMATO
# ======================================
def color_estado(val):
    colors = {
        "A TIEMPO": "#9FE2BF",
        "VENCIDO": "#FF6961",
        "ALERTA": "#FDFD96",
        "ALERTA_0": "#FFA500"
    }
    if val in colors:
        return f"background-color: {colors[val]}; color: black;"
    return ""


def estilo_bordes(df):
    return df.style.set_table_styles(
        [
            {"selector": "th",
             "props": [
                 ("background-color", "#E8E8E8"),
                 ("color", "black"),
                 ("font-weight", "bold"),
                 ("border", "1px solid #BFBFBF"),
                 ("padding", "6px")
             ]},
            {"selector": "td",
             "props": [
                 ("border", "1px solid #D9D9D9"),
                 ("padding", "6px")
             ]},
            {"selector": "tr:nth-child(even)",
             "props": [("background-color", "#FAFAFA")]},
            {"selector": "tr:nth-child(odd)",
             "props": [("background-color", "white")]}
        ]
    )

# ======================================
# FILTROS
# ======================================
st.sidebar.header("🔎 Filtros ANS")

def get_unique(col):
    return df[col].dropna().unique().tolist() if col in df.columns else []

f_municipio = st.sidebar.multiselect("🏙️ Municipio", get_unique("MUNICIPIO"))
f_actividad = st.sidebar.multiselect("⚒️ Actividad", get_unique("ACTIVIDAD"))
f_estado = st.sidebar.multiselect("🟩 Estado ANS", get_unique("ESTADO"))
f_subzona = st.sidebar.multiselect("🗺️ Subzona", get_unique("SUBZONA"))

df_f = df.copy()
if f_municipio: df_f = df_f[df_f["MUNICIPIO"].isin(f_municipio)]
if f_actividad: df_f = df_f[df_f["ACTIVIDAD"].isin(f_actividad)]
if f_estado: df_f = df_f[df_f["ESTADO"].isin(f_estado)]
if f_subzona: df_f = df_f[df_f["SUBZONA"].isin(f_subzona)]


# ======================================
# KPIs
# ======================================
st.subheader("📌 Indicadores ANS")

total = len(df_f)
atiempo = len(df_f[df_f["ESTADO"] == "A TIEMPO"])
alerta = len(df_f[df_f["ESTADO"] == "ALERTA"])
alerta0 = len(df_f[df_f["ESTADO"] == "ALERTA_0"])
vencido = len(df_f[df_f["ESTADO"] == "VENCIDO"])
sinfecha = len(df_f[df_f["ESTADO"] == "SIN FECHA"])

k1, k2, k3, k4, k5, k6 = st.columns(6)

def tarjeta_kpi(color, titulo, valor, icono):
    return f"""
    <div style='background-color:{color};
                padding:12px; border-radius:10px;
                text-align:center; color:white;
                font-size:16px; font-weight:bold;
                box-shadow:0px 2px 6px rgba(0,0,0,0.15);'>
        <div style='font-size:22px; margin-bottom:5px;'>{icono} {valor}</div>
        <div style='font-size:13px; opacity:.9;'>{titulo}</div>
    </div>
    """

k1.markdown(tarjeta_kpi("#6c757d", "Total pedidos", total, "📦"), unsafe_allow_html=True)
k2.markdown(tarjeta_kpi("#28a745", "A tiempo", atiempo, "🟢"), unsafe_allow_html=True)
k3.markdown(tarjeta_kpi("#ffc107", "Alerta", alerta, "🟡"), unsafe_allow_html=True)
k4.markdown(tarjeta_kpi("#fd7e14", "Alerta 0 días", alerta0, "🟠"), unsafe_allow_html=True)
k5.markdown(tarjeta_kpi("#dc3545", "Vencidos", vencido, "🔴"), unsafe_allow_html=True)
k6.markdown(tarjeta_kpi("#0d6efd", "Sin fecha", sinfecha, "🔵"), unsafe_allow_html=True)

# ======================================
# TABS PRINCIPALES
# ======================================
tab1, tab2, tab3 = st.tabs(["📄 Vista de Datos", "📊 Gráficas ANS", "🗺️ Mapa ANS"])

# TAB 1 — DATOS
with tab1:
    st.subheader("📄 Vista de DATOS_ANS")
    styled_df = estilo_bordes(df_f).applymap(color_estado, subset=["ESTADO"])
    st.dataframe(styled_df, use_container_width=True)

# TAB 2 — GRÁFICAS
with tab2:
    st.subheader("📊 Gráficas ANS")

    import plotly.express as px
    import plotly.graph_objects as go

    df_estado = df_f["ESTADO"].value_counts().reset_index()
    df_estado.columns = ["ESTADO", "CANTIDAD"]

    fig_estado = px.bar(
        df_estado, x="ESTADO", y="CANTIDAD",
        color="ESTADO",
        title="Distribución de Estados ANS",
        color_discrete_map={
            "A TIEMPO": "#28a745",
            "ALERTA": "#ffc107",
            "ALERTA_0": "#fd7e14",
            "VENCIDO": "#dc3545",
            "SIN_FECHA": "#0d6efd"
        }
    )
    fig_estado.update_layout(template="plotly_white")
    st.plotly_chart(fig_estado, use_container_width=True)

    st.subheader("🏙️ Distribución por Municipio")
    if "MUNICIPIO" in df_f.columns:
        df_mun = df_f["MUNICIPIO"].value_counts().reset_index()
        df_mun.columns = ["MUNICIPIO", "CANTIDAD"]

        fig_mun = px.bar(
            df_mun,
            x="MUNICIPIO", y="CANTIDAD",
            color="MUNICIPIO",
            title="Cantidad de pedidos por Municipio",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_mun.update_layout(
            template="plotly_white",
            xaxis_tickangle=-45,
            showlegend=False
        )

        st.plotly_chart(fig_mun, use_container_width=True)

    st.subheader("🥧 Distribución porcentual ANS")
    fig_pie = go.Figure(
        data=[go.Pie(
            labels=df_estado["ESTADO"],
            values=df_estado["CANTIDAD"],
            hole=0.45,
            marker=dict(
                colors=[
                    "#28a745",
                    "#ffc107",
                    "#fd7e14",
                    "#dc3545",
                    "#0d6efd"
                ],
                line=dict(color="white", width=2)
            )
        )]
    )
    fig_pie.update_layout(template="plotly_white")
    st.plotly_chart(fig_pie, use_container_width=True)


# TAB 3 — MAPA
with tab3:
    st.subheader("🗺️ Mapa ANS geolocalizado")

    import folium
    from folium.plugins import Fullscreen
    from streamlit_folium import st_folium

    # ============================
    # INPUT CONTROLADO REAL
    # ============================
    if "buscar_pedido" not in st.session_state:
        st.session_state.buscar_pedido = ""

    st.text_input("🔍 Buscar pedido:", key="buscar_pedido")

    # ============================
    # VALIDAR COORDENADAS
    # ============================
    if not {"X", "Y"}.issubset(df_f.columns):
        st.warning("⚠️ No existen columnas X/Y válidas.")
        st.stop()

    # ============================
    # BASE DEL MAPA
    # ============================
    df_map = df_f.dropna(subset=["X", "Y"]).copy()
    pedido_encontrado = None
    bus = st.session_state.buscar_pedido.strip()

    # ============================
    # FILTRO POR PEDIDO
    # ============================
    if bus != "":
        df_bus = df_map[df_map["PEDIDO"].astype(str) == bus]
        if df_bus.empty:
            st.warning("⚠️ Pedido no encontrado.")
            st.stop()
        df_map = df_bus
        pedido_encontrado = df_bus.iloc[0]

    # ============================
    # CENTRAR MAPA
    # ============================
    if pedido_encontrado is not None:
        lat_c = float(pedido_encontrado["Y"])
        lon_c = float(pedido_encontrado["X"])
        zoom = 17
    else:
        lat_c = df_map["Y"].mean()
        lon_c = df_map["X"].mean()
        zoom = 12

    # ============================
    # MAPA PROFESIONAL — CARTO VOYAGER (SIN AUTENTICACIÓN)
    # ============================
    m = folium.Map(
        location=[lat_c, lon_c],
        zoom_start=zoom,
        tiles="https://cartodb-basemaps-a.global.ssl.fastly.net/rastertiles/voyager/{z}/{x}/{y}.png",
        attr="© CARTO © OpenStreetMap contributors"
    )

    Fullscreen().add_to(m)

    # ============================
    # ICONOS PERSONALIZADOS (GOTAS)
    # ============================
    def color_hex(estado):
        colores = {
            "A TIEMPO": "#28a745",
            "ALERTA": "#ffc107",
            "ALERTA_0": "#fd7e14",
            "VENCIDO": "#dc3545",
            "SIN FECHA": "#0d6efd"
        }
        return colores.get(estado, "#8e8e8e")

    def crear_icono(color):
        return folium.DivIcon(html=f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 24 24">
        <path fill="{color}" stroke="black" stroke-width="1"
              d="M12 2C8 2 5 5 5 9c0 5 7 13 7 13s7-8 7-13c0-4-3-7-7-7zm0 9.5
                 c-1.4 0-2.5-1.1-2.5-2.5S10.6 6.5 12 6.5s2.5 1.1 2.5 2.5S13.4 11.5 12 11.5z"/>
        </svg>
        """)

    # ============================
    # MARCADORES
    # ============================
    for _, r in df_map.iterrows():
        popup = f"""
        <b>Pedido:</b> {r['PEDIDO']}<br>
        <b>Actividad:</b> {r['ACTIVIDAD']}<br>
        <b>Estado:</b> {r['ESTADO']}<br>
        <b>Cliente:</b> {r.get('NOMBRE_CLIENTE','')}<br>
        <b>Municipio:</b> {r.get('MUNICIPIO','')}
        """
        folium.Marker(
            location=[r["Y"], r["X"]],
            popup=popup,
            icon=crear_icono(color_hex(r["ESTADO"]))
        ).add_to(m)

    st_folium(m, width=1100, height=600)


