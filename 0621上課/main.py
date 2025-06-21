import streamlit as st

def main():
    st.title("My Streamlit App")
    st.write("Welcome to my basic Streamlit application!")

    # You can add more Streamlit components here
    name = st.text_input("Enter your name:")
    if name:
        st.write(f"Hello, {name}!")

if __name__ == "__main__":
    main()
    import pandas as pd
    st.header("Taiwan Data")
    try:
        df = pd.read_csv("taiwan.csv")
        st.dataframe(df)
    except FileNotFoundError:
        st.error("taiwan.csv not found. Please make sure the file is in the same directory.")