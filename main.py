import streamlit as st
from engine import Engine
from enum import Enum


class states(Enum):
    START = "start"
    THINK = "think"


DEBUG = False


def change_state(state):
    st.session_state.state = state


if "state" not in st.session_state:
    st.session_state.state = states.START

st.logo("maomao-testing-food-with-vignette.jpg")
st.title("House Price Indicator")
st.markdown("### Get your house price indication [:red[TODAY!]](https://www.calendardate.com/todays.htm)")
st.markdown("### Please answer the questions below to get an estimation.")
st.markdown(":small[Made by Matei, Sara and Oscrawr]")


if st.session_state.state.value == states.START.value:
    st.button("Begin", on_click=change_state, args=[states.THINK], icon="🚀")
if st.session_state.state.value == states.THINK.value:
    st.button("Reset", on_click=change_state, args=[states.START], icon="🔄")

    e = Engine("knowledge.json")
    e.forward_inf()

    if DEBUG:
        for fact in e.kb["facts"]:
            if fact["name"] == "Good location":
                st.write("GOOD: ", fact["value"])
            if fact["name"] == "Bad location":
                st.write("BAD: ", fact["value"])
            if fact["name"] == "Many":
                st.write("Many: ", fact["value"])
            if fact["name"] == "Big":
                st.write("Big: ", fact["value"])
            if fact["name"] == "Efficient":
                st.write("Efficient: ", fact["value"])
