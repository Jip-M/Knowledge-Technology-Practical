import streamlit as st

st.title("House price inference engine")

st.markdown(
    """
Welcome world! :)

This is our inference engine.
    """
)


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
