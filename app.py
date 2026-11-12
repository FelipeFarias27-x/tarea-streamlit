import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configuración inicial de la página en formato ancho
st.set_page_config(page_title="Dashboard interactivo de notas", layout="wide")

# Título principal y descripción
st.title("Panel interactivo de notas")
st.write("Explora los resultados de un curso combinando filtros. Promedio: 50% de cada evaluación. Aprobación del ejercicio: promedio mayor o igual a 4.0. Datos ficticios.")

# ----------------------------------------------------
# BARRA LATERAL (SIDEBAR) - CARGA DE ARCHIVO Y FILTROS
# ----------------------------------------------------
st.sidebar.header("Datos y filtros")
st.sidebar.subheader("Carga el archivo de estudiantes")

# Widget interactivo para subir el archivo CSV (tal como pide la pauta)
archivo_subido = st.sidebar.file_uploader("Sube tu archivo CSV", type=["csv"])

if archivo_subido is not None:
    df = pd.read_csv(archivo_subido)
else:
    # Si no se ha subido uno nuevo, intenta cargar el que está por defecto en el repositorio
    try:
        df = pd.read_csv("estudiantes_notas.csv")
    except FileNotFoundError:
        st.warning("Por favor, sube el archivo 'estudiantes_notas.csv' usando el botón de la barra lateral o el repositorio.")
        st.stop()

# Calcular el promedio institucional si no viene listo (50% nota_1 y 50% nota_2)
if "promedio" not in df.columns and "nota_1" in df.columns and "nota_2" in df.columns:
    df["promedio"] = (df["nota_1"] * 0.5) + (df["nota_2"] * 0.5)

st.sidebar.subheader("Sexo")
sexo_opciones = ["Todos"] + list(df["sexo"].unique()) if "sexo" in df.columns else ["Todos"]
sexo_seleccionado = st.sidebar.selectbox("Selecciona sexo", sexo_opciones)

st.sidebar.subheader("Sección")
seccion_opciones = ["Todas"] + list(df["seccion"].unique()) if "seccion" in df.columns else ["Todas"]
seccion_seleccionada = st.sidebar.selectbox("Selecciona sección", seccion_opciones)

st.sidebar.subheader("Rango del promedio")
rango_promedio = st.sidebar.slider("Rango de notas", 1.0, 7.0, (1.0, 7.0))

st.sidebar.subheader("Asistencia mínima (%)")
asistencia_minima = st.sidebar.slider("Porcentaje mínimo", 0, 100, 0)

# Aplicar los filtros sobre el DataFrame
df_filtrado = df.copy()

if sexo_seleccionado != "Todos" and "sexo" in df_filtrado.columns:
    df_filtrado = df_filtrado[df_filtrado["sexo"] == sexo_seleccionado]

if seccion_seleccionada != "Todas" and "seccion" in df_filtrado.columns:
    df_filtrado = df_filtrado[df_filtrado["seccion"] == seccion_seleccionada]

if "promedio" in df_filtrado.columns:
    df_filtrado = df_filtrado[
        (df_filtrado["promedio"] >= rango_promedio[0]) & 
        (df_filtrado["promedio"] <= rango_promedio[1])
    ]

if "asistencia" in df_filtrado.columns:
    df_filtrado = df_filtrado[df_filtrado["asistencia"] >= asistencia_minima]

# Resumen de filtros activos
st.write(f"**Filtros activos:** Sexo: {sexo_seleccionado} - Sección: {seccion_seleccionada} - Promedio: {rango_promedio[0]} a {rango_promedio[1]} - Asistencia mínima: {asistencia_minima}%")

# ----------------------------------------------------
# MÉTRICAS PRINCIPALES
# ----------------------------------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Estudiantes seleccionados", len(df_filtrado))

with col2:
    promedio_general = round(df_filtrado["promedio"].mean(), 2) if len(df_filtrado) > 0 and "promedio" in df_filtrado.columns else 0
    st.metric("Promedio general", promedio_general)

with col3:
    if len(df_filtrado) > 0 and "promedio" in df_filtrado.columns:
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

tipo_grafico = st.radio("Gráfico", ["Notas por estudiante", "Promedio por sección"], horizontal=True)

if len(df_filtrado) > 0:
    fig, ax = plt.subplots(figsize=(10, 4))
    
    if tipo_grafico == "Notas por estudiante" and "estudiante" in df_filtrado.columns and "promedio" in df_filtrado.columns:
        ax.bar(df_filtrado["estudiante"], df_filtrado["promedio"], color="#1f77b4")
        ax.axhline(4.0, color="red", linestyle="--", label="Aprobación: 4.0")
        ax.set_ylabel("Promedio de notas")
        ax.set_xlabel("Estudiante")
        plt.xticks(rotation=45, ha="right")
        ax.legend()
    elif "seccion" in df_filtrado.columns and "promedio" in df_filtrado.columns:
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
