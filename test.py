import streamlit as st

def multiselect(question, options, key):
    st.markdown(f"**{question}**")
    selected = []

    for opt in options:
        if st.checkbox(opt, key=f"{key}_{opt}"):
            selected.append(opt)

    return selected


def uniselect(question, options):
    st.markdown(f"**{question}**")
    selected = []

    selected.append(st.radio("", options, index=None))
    return selected


st.markdown("### Survey")

color = uniselect(
    "Which color do you like most?",
    ["Red", "Blue", "Green"],
)

if color[0] == "Red":
    st.write("Oohhh I like red too!")

if color[0] == "Blue":
    st.write("Ughh.. Basic")

if color[0] == "Green":
    st.write("Dah Bestuhh")

fruits = multiselect(
    "Which fruits do you like?",
    ["Apple", "Banana", "Orange"],
    key="fruits",
)

for fruit in fruits:
    if fruit == "Apple":
        st.write("Tasty!")
    else:
        st.write("Good choice")
