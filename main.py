import streamlit as st
from PIL import Image

from object_detector import detect_objects


st.title("Object Detection")

st.write(
    "Upload an image to detect objects using DETR."
)

uploaded_file = st.file_uploader(
    "Select an image",
    type=["jpg", "jpeg", "png"]
)


if uploaded_file is not None:

    image = Image.open(uploaded_file)

    st.subheader("Input Image")

    st.image(
        image,
        use_container_width=True
    )

    if st.button("Detect Objects"):

        with st.spinner("Detecting objects..."):

            processed_image = detect_objects(image)

        st.subheader("Processed Image")

        st.image(
            processed_image,
            use_container_width=True
        )