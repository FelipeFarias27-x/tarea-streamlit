import streamlit as st

# Configuración de la página
st.title("Mi primera aplicación de Streamlit")

# ----------------------------------------------------
# ÁREA PRINCIPAL
# ----------------------------------------------------
st.subheader("¡Hola, Streamlit!")
st.write("Esta es una aplicación simple")
st.write("Haz clic")

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
st.sidebar.write("Haz clic pero en la barra lateral")

# Campo de texto en la barra lateral
texto_lateral = st.sidebar.text_input("Escribe algo en la barra:", key="lateral")

if texto_lateral:
    st.sidebar.write(f"Escribiste en la barra: {texto_lateral}")
