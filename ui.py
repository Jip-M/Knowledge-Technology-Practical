import streamlit as st

st.title("House price inference engine")

st.markdown(
    """
Welcome world! :)

This is our inference engine.
    """
)


def general_ui():
    st.header("House Price Indicator")
    st.markdown("Get your house price indication :red[TODAY]")
    st.markdown(":small[Made by Matei, Sara and Oscar]")


def multiselect(question, options, key):
    st.markdown(f"**{question}**")
    selected = []

    for opt in options:
        if st.checkbox(opt, key=f"{key}_{opt}"):
            selected.append(opt)

    return selected


def uniselect(question, options, key):
    st.markdown(f"**{question}**")
    selected = []

    selected.append(st.radio("", options, key=key, index=None))
    return selected


def next_question(key):
    return st.button("Next", key=key)
