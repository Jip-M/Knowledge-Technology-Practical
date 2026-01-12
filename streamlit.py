import streamlit as st
from enigne import Engine

st.logo("maomao-testing-food-with-vignette.jpg")
st.title("House Price Indicator")
st.markdown("### Get your house price indication [:red[TODAY!]](https://www.calendardate.com/todays.htm)")
st.markdown("### Please answer the questions below to get an estimation.")
st.markdown(":small[Made by Matei, Sara and Oscrawr]")

e = Engine("knowledge.json")
e.forward_inf()
