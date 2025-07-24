import streamlit as st

st.title("Stadtplan: City Map Generator")
st.write("Enter a city name and generate a beautiful map!")

city = st.text_input("City name", placeholder="e.g. Rabat, Morocco")

if st.button("Generate Map"):
    if city:
        st.write(f"Generating map for: {city}")
    else:
        st.error("Please enter a city name.")

