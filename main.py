import streamlit as st
from PIL import Image

from object_detector import detect_objects


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Object Detection",
    page_icon="🔍",
    layout="centered"
)


# --------------------------------------------------
# Session State
# --------------------------------------------------

if "show_camera" not in st.session_state:
    st.session_state.show_camera = False

if "processed_images" not in st.session_state:
    st.session_state.processed_images = []


# --------------------------------------------------
# CSS
# --------------------------------------------------

st.markdown("""
<style>

.stApp {
    background-color: #0B0F19;
}

.main .block-container {
    max-width: 800px;
    padding-top: 40px;
}


/* Title */

.title {
    color: white;
    font-size: 28px;
    font-weight: 600;
    text-align: center;
    margin-bottom: 30px;
}


/* Upload box */

[data-testid="stFileUploader"] {
    background-color: #24262C;
    border-radius: 8px;
    padding: 15px;
}


/* Buttons */

div.stButton > button {
    height: 45px;
    border-radius: 6px;
    font-size: 16px;
    font-weight: 600;
}


/* Submit */

div.stButton > button[kind="primary"] {
    background-color: #FF5200;
    color: white;
    border: none;
}


/* Clear */

div.stButton > button[kind="secondary"] {
    background-color: #555761;
    color: white;
    border: none;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# Title
# --------------------------------------------------

st.markdown(
    '<div class="title">🔍 Object Detection</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# Upload Images
# --------------------------------------------------

st.subheader("Upload Images")

uploaded_files = st.file_uploader(
    "Choose image files",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)


# --------------------------------------------------
# Camera Button
# --------------------------------------------------

st.write("")

camera_button = st.button(
    "📷 Open Camera",
    use_container_width=True
)


if camera_button:
    st.session_state.show_camera = True


# --------------------------------------------------
# Camera
# --------------------------------------------------

camera_image = None

if st.session_state.show_camera:

    st.subheader("Camera")

    camera_image = st.camera_input(
        "Take a picture",
        label_visibility="collapsed"
    )


# --------------------------------------------------
# Buttons
# --------------------------------------------------

st.write("")

col1, col2 = st.columns(2)


with col1:

    clear_button = st.button(
        "Clear",
        type="secondary",
        use_container_width=True
    )


with col2:

    submit_button = st.button(
        "Submit",
        type="primary",
        use_container_width=True
    )


# --------------------------------------------------
# Clear
# --------------------------------------------------

if clear_button:

    st.session_state.processed_images = []
    st.session_state.show_camera = False

    st.rerun()


# --------------------------------------------------
# Submit
# --------------------------------------------------

if submit_button:

    st.session_state.processed_images = []

    # ----------------------------------------------
    # Uploaded images
    # ----------------------------------------------

    if uploaded_files:

        for uploaded_file in uploaded_files:

            image = Image.open(
                uploaded_file
            ).convert("RGB")

            processed_image = detect_objects(image)

            st.session_state.processed_images.append(
                processed_image
            )


    # ----------------------------------------------
    # Camera image
    # ----------------------------------------------

    elif camera_image is not None:

        image = Image.open(
            camera_image
        ).convert("RGB")

        processed_image = detect_objects(image)

        st.session_state.processed_images.append(
            processed_image
        )


    # ----------------------------------------------
    # No image
    # ----------------------------------------------

    else:

        st.warning(
            "Please upload an image or open the camera and take a picture."
        )


# --------------------------------------------------
# Display Results
# --------------------------------------------------

if st.session_state.processed_images:

    st.subheader("Processed Image(s)")

    for i, processed_image in enumerate(
        st.session_state.processed_images
    ):

        st.image(
            processed_image,
            caption=f"Processed Image {i + 1}",
            use_container_width=True
        )