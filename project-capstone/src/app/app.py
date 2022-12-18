import streamlit as st
import requests

st.title('Beans Classification')

st.markdown("""
Enter an image URL or upload an image file to classify it.
""")
service_url = "http://localhost:9696/predict"

image_url = st.text_input("Image URL:")
# image_file = st.file_uploader("Image file")

if "visiblilt" not in st.session_state:
    st.session_state.visiblilt = "visible"
    st.session_state.disabled = False

loading_indicator = st.empty()
loading_indicator.text("Loading image..")

try:
    if not image_url:
        st.write("Please enter a image URL.")
    else:        
        data = {
            "url": image_url
        }
        result = requests.post(service_url, json=data).json()
        st.write(f"The image class is a: {result}.")
except JSONDecodeError as je:
    st.write(f"Error loading image: {je}")
except NameError as ne:
    st.write(f"Image URL does not provide yet {ne}")

loading_indicator.empty()

