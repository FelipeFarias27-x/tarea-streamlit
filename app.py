import streamlit as st

# Configuración de la página
st.title("Mi primera aplicación de Streamlit")

# ----------------------------------------------------
# ÁREA PRINCIPAL
# ----------------------------------------------------
st.subheader("¡Hola, Streamlit!")
st.write("Esta es una aplicación simple")

# Agregamos el logo de la USS
st.image("descarga.jpg", width=150)

# Botón interactivo oficial
if st.button("Haz clic"):
    st.write("¡Hiciste clic en el botón!")

# Campo de texto en el área principal
texto_principal = st.text_input("Escribe algo:", key="principal")

if texto_principal:
    st.write(f"Escribiste: {texto_principal}")


# ----------------------------------------------------
# BARRA LATERAL (SIDEBAR)
# ----------------------------------------------------
st.sidebar.title("Mi primera barra lateral de Streamlit")
st.sidebar.write("¡Hola, Barra Lateral!")
st.sidebar.write("Esto es una barra lateral")

# Agregamos el logo en la barra lateral
st.sidebar.image("descarga.jpg", width=100)

# Botón interactivo en la barra lateral
if st.sidebar.button("Haz clic pero en la barra lateral"):
    st.sidebar.write("¡Hiciste clic en la barra lateral!")

# Campo de texto en la barra lateral
texto_lateral = st.sidebar.text_input("Escribe algo en la barra:", key="lateral")

if texto_lateral:
    st.sidebar.write(f"Escribiste en la barra: {texto_lateral}")
