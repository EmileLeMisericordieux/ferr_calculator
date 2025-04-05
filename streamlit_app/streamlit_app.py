import plotly.express as px
import streamlit as st
import pandas as pd


df = pd.DataFrame({
    'age': [
        65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75,
        76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86,
        87, 88, 89, 90, 91, 92, 93, 94, 95
    ],
    'min_withdraw': [
        4.00, 4.17, 4.35, 4.55, 4.76, 5.00, 5.28,
        5.40, 5.53, 5.67, 5.82, 5.98, 6.17, 6.36,
        6.58, 6.82, 7.08, 7.38, 7.71, 8.08, 8.51,
        8.99, 9.55, 10.21, 10.99, 11.92, 13.06,
        14.49, 16.34, 18.79, 20.00
    ]
})

st.write("Streamlit testing")
st.write(df)

fig = px.line(df, x="age", y="min_withdraw", title='Withdrawals')
st.plotly_chart(fig)
