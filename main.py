import streamlit as st
from PIL import Image
from object_detector import detect_objects

st.title("Object Detection")
st.write("Upload an image or take a photo to detect objects using DETR.")

uploaded_file = st.file_uploader(
    "Upload an image",
    type=["jpg", "jpeg", "png"]
)

camera_image = st.camera_input("Take a picture")

image = None

if uploaded_file is not None:
    image = Image.open(uploaded_file)

elif camera_image is not None:
    image = Image.open(camera_image)

if image is not None:
    st.image(image, caption="Input image")

    if st.button("Detect Objects"):
        with st.spinner("Detecting objects..."):
            processed_image = detect_objects(image)

        st.image(
            processed_image,
            caption="Processed image"
        )