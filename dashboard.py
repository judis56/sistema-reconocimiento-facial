import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Dashboard para asistencia",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Dashboard inteligente de asistencia")
st.markdown("---")
try:

    df = pd.read_csv(
        "asistencia.csv",
        header=None,
        names=["Nombre", "Fecha", "Hora"]
    )

except:

    st.error("No existe asistencia.csv")

    st.stop()

total_registros = len(df)

personas_unicas = df["Nombre"].nunique()

ultima_persona = df.iloc[-1]["Nombre"]
col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Registros",
    total_registros
)

col2.metric(
    "Personas Detectadas",
    personas_unicas
)

col3.metric(
    "Última Persona",
    ultima_persona
)

st.markdown("---")
st.subheader("📋 Tabla de Asistencia")

st.dataframe(
    df,
    use_container_width=True
)
st.subheader("Asistencias por Persona")

conteo = df["Nombre"].value_counts().reset_index()

conteo.columns = ["Nombre", "Cantidad"]

fig = px.bar(
    conteo,
    x="Nombre",
    y="Cantidad",
    text="Cantidad",
    color="Nombre"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
st.subheader("Últimos Registros")

st.table(
    df.tail(5)
)