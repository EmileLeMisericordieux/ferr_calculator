from helper_functions import *
import plotly.express as px
import streamlit as st
import pandas as pd


st.set_page_config(layout="wide")

with st.sidebar:
    st.image(r"streamlit_app\static\1743878344560-26372b5e-087c-4937-b368-72e4aa19caae_1.jpg", width=500)
    st.title("Versement de FERR")

    start_value = st.number_input("Valeur du FERR", value=200_000)
    start_age = st.number_input("Début du FERR à l'âge de", value=71)
    end_age = st.number_input("Fin du FERR à l'âge de", value=90)
    interest_rate = st.number_input("Taux de rendement", value=6.00, min_value=0.0, max_value=100.0)
    start_paying_on_year = st.number_input("Commencer les versements durant l'année", value=1, min_value=1, max_value=10)

    paying_type = st.selectbox("Type de versement", ("Minimum", "Fixe"))

    if paying_type == "Fixe":
        fix_value = st.number_input("Versement fixe", value=15_000)
        inflation_rate = st.number_input("Taux d'inflation", value=1.5)
    else:
        fix_value=0
        inflation_rate=1.5

calc = FerrCalculator(
    start_value=start_value,
    start_age=start_age,
    end_age=end_age,
    interest_rate=interest_rate,
    start_paying_on_year=start_paying_on_year,
    paying_type=paying_type,
    fix_value=fix_value,
    inflation_rate=inflation_rate
)

df = calc.calculate()

st.write("Résultats du FERR")
st.write(df)

fig = px.line(df, x="Age", y="Valeur à la fin de l'année", title="Valeur du FERR à la fin de l'année")
st.plotly_chart(fig)
