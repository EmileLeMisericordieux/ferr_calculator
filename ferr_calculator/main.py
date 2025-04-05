from helper_functions import *
import plotly.express as px
import streamlit as st
import pandas as pd
from report_template import report_template
import markdown2


st.set_page_config(layout="wide")

with st.sidebar:
    st.image(r"ferr_calculator\static\1743878344560-26372b5e-087c-4937-b368-72e4aa19caae_1.jpg", width=500)
    st.title("Versement de FERR")

    start_value = st.number_input("Valeur du FERR", value=200_000)
    start_age = st.number_input("Début du FERR à l'âge de", value=71, min_value=50)
    end_age = st.number_input("Fin du FERR à l'âge de", value=90, max_value=100)
    interest_rate = st.number_input("Taux de rendement", value=6.00, min_value=0.0, max_value=100.0)
    start_paying_on_year = st.number_input("Commencer les versements durant l'année", value=1, min_value=1, max_value=10)

    paying_type = st.selectbox("Type de versement", ("Minimum", "Fixe"))

    if paying_type == "Fixe":
        fix_value = st.number_input("Versement fixe", value=15_000)
        inflation_rate = st.number_input("Taux d'inflation", value=1.5)
    else:
        fix_value = 0
        inflation_rate = 1.5

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

st.title("Versement de FERR")
st.data_editor(
    df,
    column_config={
        "Age": st.column_config.NumberColumn(
            "Age",
        ),
        "Valeur au début de l'année": st.column_config.NumberColumn(
            "Valeur au début de l'année",
            format="dollar",
        ),
        "Versement Annuel": st.column_config.NumberColumn(
            "Versement Annuel",
            format="dollar",
        ),
        "Pourcentage de Retrait": st.column_config.NumberColumn(
            "Pourcentage de Retrait",
            format="percent",
        ),
        "Valeur à la fin de l'année": st.column_config.NumberColumn(
            "Valeur à la fin de l'année",
            format="dollar",
        ),
    },
    hide_index=True
)

fig = px.line(
    df,
    x="Age",
    y="Valeur à la fin de l'année",
    title="Valeur du FERR en fonction du temps"
)

st.plotly_chart(fig)

for col in ["Valeur au début de l'année", "Versement Annuel", "Valeur à la fin de l'année"]:
    df = add_thousand_separator_with_dollar(df, col)

df = format_percent_column(df, "Pourcentage de Retrait", 2)

report = markdown2.markdown(
    report_template(
        start_value=start_value,
        start_age=start_age,
        end_age=end_age,
        interest_rate=interest_rate,
        start_paying_on_year=start_paying_on_year,
        paying_type=paying_type,
        fix_value=fix_value,
        inflation_rate=inflation_rate,
        df=df,
        fig=fig
    )
)

st.download_button(
    label="Download report",
    data=report,
    file_name="report.html",
    mime="text/html",
    icon=":material/download:",
)
