import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuración inicial de la página en formato ancho
st.set_page_config(page_title="Dashboard interactivo de notas", layout="wide")

# Título principal y descripción
st.title("Dashboard interactivo de notas")
st.write("Explora los resultados de un curso combinando filtros. Promedio: 50% de cada evaluación. Aprobación del ejercicio: promedio mayor o igual a 4.0. Datos ficticios.")

# Cargar los datos desde el archivo CSV subido
@st.cache_data
def cargar_datos():
    return pd.read_csv("estudiantes_notas.csv")

try:
    df = cargar_datos()
except FileNotFoundError:
    st.error("No se encontró el archivo 'estudiantes_notas.csv'. Asegúrate de haberlo subido al repositorio.")
    st.stop()

# ----------------------------------------------------
# BARRA LATERAL (SIDEBAR) - FILTROS
# ----------------------------------------------------
st.sidebar.header("Datos y filtros")
st.sidebar.subheader("Carga el archivo de estudiantes")
st.sidebar.write("estudiantes_notas.csv")

st.sidebar.subheader("Sexo")
sexo_opciones = ["Todos"] + list(df["sexo"].unique())
sexo_seleccionado = st.sidebar.selectbox("Selecciona sexo", sexo_opciones)

st.sidebar.subheader("Sección")
seccion_opciones = ["Todas"] + list(df["seccion"].unique())
seccion_seleccionada = st.sidebar.selectbox("Selecciona sección", seccion_opciones)

st.sidebar.subheader("Rango del promedio")
rango_promedio = st.sidebar.slider("Rango de notas", 1.0, 7.0, (1.0, 7.0))

st.sidebar.subheader("Asistencia mínima (%)")
asistencia_minima = st.sidebar.slider("Porcentaje mínimo", 0, 100, 0)

# Aplicar los filtros sobre el DataFrame
df_filtrado = df.copy()

if sexo_seleccionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["sexo"] == sexo_seleccionado]

if seccion_seleccionada != "Todas":
    df_filtrado = df_filtrado[df_filtrado["seccion"] == seccion_seleccionada]

df_filtrado = df_filtrado[
    (df_filtrado["promedio"] >= rango_promedio[0]) & 
    (df_filtrado["promedio"] <= rango_promedio[1]) &
    (df_filtrado["asistencia"] >= asistencia_minima)
]

# Resumen de filtros activos
st.write(f"**Filtros activos:** Sexo: {sexo_seleccionado} - Sección: {seccion_seleccionada} - Promedio: {rango_promedio[0]} a {rango_promedio[1]} - Asistencia mínima: {asistencia_minima}%")

# ----------------------------------------------------
# MÉTRICAS PRINCIPALES
# ----------------------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Estudiantes seleccionados", len(df_filtrado))

with col2:
    promedio_general = round(df_filtrado["promedio"].mean(), 2) if len(df_filtrado) > 0 else 0
    st.metric("Promedio general", promedio_general)

with col3:
    if len(df_filtrado) > 0:
        aprobados_count = len(df_filtrado[df_filtrado["promedio"] >= 4.0])
        porcentaje_aprobacion = round((aprobados_count / len(df_filtrado)) * 100, 2)
    else:
        porcentaje_aprobacion = 0
    st.metric("Aprobación", f"{porcentaje_aprobacion}%")

st.markdown("---")

# ----------------------------------------------------
# VISUALIZACIÓN DE NOTAS (GRÁFICO Y TABLA)
# ----------------------------------------------------
st.subheader("Visualización de notas")

# Opciones de gráfico
tipo_grafico = st.radio("Gráfico", ["Notas por estudiante", "Promedio por sección"], horizontal=True)

if len(df_filtrado) > 0:
    fig, ax = plt.subplots(figsize=(10, 4))
    
    if tipo_grafico == "Notas por estudiante":
        ax.bar(df_filtrado["estudiante"], df_filtrado["promedio"], color="#1f77b4")
        ax.axhline(4.0, color="red", linestyle="--", label="Aprobación: 4.0")
        ax.set_ylabel("Promedio de notas")
        ax.set_xlabel("Estudiante")
        plt.xticks(rotation=45, ha="right")
        ax.legend()
    else:
        promedios_seccion = df_filtrado.groupby("seccion")["promedio"].mean()
        ax.bar(promedios_seccion.index, promedios_seccion.values, color="#ff7f0e")
        ax.set_ylabel("Promedio")
        ax.set_xlabel("Sección")
    
    st.pyplot(fig)
else:
    st.warning("No hay datos que coincidan con los filtros seleccionados.")

st.subheader("Estudiantes seleccionados")
st.dataframe(df_filtrado)

# Botón para descargar selección en CSV
if len(df_filtrado) > 0:
    csv = df_filtrado.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Descargar selección CSV",
        data=csv,
        file_name='estudiantes_filtrados.csv',
        mime='text/csv',
    )
