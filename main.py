import streamlit as st
from PIL import Image

from object_detector import detect_objects


# -----------------------------------------
# Page configuration
# -----------------------------------------

st.set_page_config(
    page_title="Object Detection",
    page_icon="🔍",
    layout="centered"
)


# -----------------------------------------
# Session state
# -----------------------------------------

if "show_camera" not in st.session_state:
    st.session_state.show_camera = False

if "processed_images" not in st.session_state:
    st.session_state.processed_images = []


# -----------------------------------------
# Title
# -----------------------------------------

st.title("🔍 Object Detection")

st.write("Upload an image or use your camera to detect objects.")


# -----------------------------------------
# Upload images
# -----------------------------------------

st.subheader("Upload Images")

uploaded_files = st.file_uploader(
    "Choose image(s)",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)


# -----------------------------------------
# Camera button
# -----------------------------------------

if st.button(
    "📷 Open Camera",
    use_container_width=True
):

    st.session_state.show_camera = True


# -----------------------------------------
# Camera
# -----------------------------------------

camera_image = None

if st.session_state.show_camera:

    st.subheader("Camera")

    camera_image = st.camera_input(
        "Take a picture"
    )


# -----------------------------------------
# Clear and Submit
# -----------------------------------------

col1, col2 = st.columns(2)


with col1:

    clear_button = st.button(
        "Clear",
        use_container_width=True
    )


with col2:

    submit_button = st.button(
        "Submit",
        type="primary",
        use_container_width=True
    )


# -----------------------------------------
# Clear
# -----------------------------------------

if clear_button:

    st.session_state.processed_images = []
    st.session_state.show_camera = False

    st.rerun()


# -----------------------------------------
# Submit
# -----------------------------------------

if submit_button:

    st.session_state.processed_images = []

    # Uploaded images
    if uploaded_files:

        for uploaded_file in uploaded_files:

            image = Image.open(
                uploaded_file
            ).convert("RGB")

            result = detect_objects(image)

            st.session_state.processed_images.append(
                result
            )

    # Camera image
    elif camera_image is not None:

        image = Image.open(
            camera_image
        ).convert("RGB")

        result = detect_objects(image)

        st.session_state.processed_images.append(
            result
        )

    else:

        st.warning(
            "Please upload an image or open the camera."
        )


# -----------------------------------------
# Results
# -----------------------------------------

if st.session_state.processed_images:

    st.subheader("Results")

    for i, image in enumerate(
        st.session_state.processed_images
    ):

        st.image(
            image,
            caption=f"Processed Image {i + 1}",
            use_container_width=True
        )