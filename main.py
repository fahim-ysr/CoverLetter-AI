import streamlit as st

st.title("CoverLetterAI")

input_url = st.text_input("Enter URL: ")
submit = st.button("Submit")

if submit:
    st.code("Welcome to CoverLetter AI. I am your Assistant", language="markdown")