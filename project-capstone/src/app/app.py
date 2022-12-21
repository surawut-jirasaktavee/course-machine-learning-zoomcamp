import streamlit as st
from PIL import Image
import requests
import os

bean_rust = Image.open('./images/bean_rust.jpg')
healthy = Image.open('./images/healthy.jpg')
angular_leaf_spot = Image.open('./images/angular_leaf_spot.jpg')

# Put your serving gateway here
service_url = os.getenv("url", "")

# Add a logo to the top of the page
st.image("./images/beans.jpeg", width=200)

st.title("Beans Classification")

# Add a sidebar for additional options or information
st.sidebar.markdown("""
Enter an image URL or upload an image file to classify it.
""")

input_method = st.sidebar.selectbox("Select input method", ["Image URL", "Image file"])

if input_method == "Image URL":
    image_url = st.sidebar.text_input("Image URL:")
elif input_method == "Image file":
    st.write("🚨 Upload image file still not support yet!")
    image_file = st.sidebar.file_uploader("Image file")
else:
    st.sidebar.write("Please select an input method.")


# Use the st.empty() function to create a loading indicator
with st.spinner("✅ Loading image.."):
    try:
        if input_method == "Image URL" and image_url:        
            data = {
                "url": image_url
            }
            result = requests.post(service_url, json=data).json()
            # Use the st.success() or st.error() functions to display the result
            if result:
                st.success(f"The image class is a: {result}.")
                if result == "healthy":
                    st.image(healthy, caption="Here is healthy bean.")
                elif result == "bean_rust":
                   st.image(bean_rust, caption="Here is a bean rust.")
                else:
                    st.image(angular_leaf_spot, caption="Here is a example of angular leaf spot.")
            else:
                st.error("Error loading image. Please try again.")
        elif input_method == "Image file" and image_file:
            # Handle image file upload here
            data = {
                "url": image_file
            }
            result = requests.post(service_url, json=data).json()
    # except JSONDecodeError as je:
    #     st.error(f"Error loading image: {je}")
    except NameError as ne:
        st.error(f"Image URL does not provide yet {ne}")

