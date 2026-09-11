import streamlit as st
from PIL import Image

from object_detector import detect_objects


st.set_page_config(
    page_title="Object Detection",
    page_icon="🔍",
    layout="centered"
)


st.title("Object Detection")

st.write(
    "Upload multiple images or take a picture "
    "to detect objects using DETR."
)


# --------------------------------------------------
# INPUT SECTION
# --------------------------------------------------

upload_column, camera_column = st.columns([3, 1])


with upload_column:

    uploaded_files = st.file_uploader(
        "Upload images",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True
    )


with camera_column:

    camera_file = st.camera_input(
        "Camera"
    )


# --------------------------------------------------
# COLLECT IMAGES
# --------------------------------------------------

images = []

# Add uploaded images
if uploaded_files:

    for uploaded_file in uploaded_files:

        image = Image.open(uploaded_file).convert("RGB")

        images.append(
            (uploaded_file.name, image)
        )


# Add camera image
if camera_file is not None:

    camera_image = Image.open(
        camera_file
    ).convert("RGB")

    images.append(
        ("Camera image", camera_image)
    )


# --------------------------------------------------
# SHOW SELECTED IMAGES
# --------------------------------------------------

if images:

    st.subheader(
        f"{len(images)} image(s) selected"
    )

    for name, image in images:

        st.image(
            image,
            caption=name,
            width=500
        )


# --------------------------------------------------
# DETECT BUTTON
# --------------------------------------------------

if images:

    if st.button(
        "🔍 Detect Objects",
        use_container_width=True
    ):

        for name, image in images:

            with st.spinner(
                f"Detecting objects in {name}..."
            ):

                processed_image = detect_objects(
                    image
                )

            st.subheader(
                f"Result: {name}"
            )

            st.image(
                processed_image,
                caption="Processed image",
                width=700
            )
