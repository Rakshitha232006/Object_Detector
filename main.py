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
# Custom CSS
# --------------------------------------------------

st.markdown(
    """
    <style>

    /* Main page */
    .stApp {
        background-color: #0E1117;
    }

    /* File uploader */
    [data-testid="stFileUploader"] {
        border: 2px dashed #4A4A4A;
        border-radius: 8px;
        background-color: #262730;
        padding: 20px;
    }

    /* Submit button */
    div.stButton > button[kind="primary"] {
        background-color: #FF5722 !important;
        color: white !important;
        border-radius: 8px;
        height: 3em;
        width: 100%;
        border: none;
    }

    /* Clear button */
    div.stButton > button[kind="secondary"] {
        background-color: #4A4A4A !important;
        color: white !important;
        border-radius: 8px;
        height: 3em;
        width: 100%;
        border: none;
    }

    /* Camera button */
    div.stButton > button {
        border-radius: 8px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# Session state
# --------------------------------------------------

if "processed_images" not in st.session_state:
    st.session_state.processed_images = []


# --------------------------------------------------
# Heading
# --------------------------------------------------

st.markdown("# 🔍 Object Detection")

st.write(
    "Upload images or use the camera to detect objects using DETR."
)


# --------------------------------------------------
# Image upload
# --------------------------------------------------

st.markdown("**Select image(s)**")

uploaded_files = st.file_uploader(
    "Drop Image Here - or - Click to Upload",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True,
    label_visibility="collapsed"
)


# --------------------------------------------------
# Camera
# --------------------------------------------------

camera_image = st.camera_input(
    "📷 Take a picture",
    label_visibility="visible"
)


col1, col2 = st.columns(2)


with col1:
    clear_clicked = st.button(
        "Clear",
        type="secondary",
        use_container_width=True
    )


with col2:
    submit_clicked = st.button(
        "Submit",
        type="primary",
        use_container_width=True
    )



if clear_clicked:

    st.session_state.processed_images = []

    st.rerun()


if submit_clicked:


    if uploaded_files:

        st.session_state.processed_images = []

        for uploaded_file in uploaded_files:

            image = Image.open(uploaded_file).convert("RGB")

            processed_image = detect_objects(image)

            st.session_state.processed_images.append(
                processed_image
            )



    elif camera_image is not None:

        st.session_state.processed_images = []

        image = Image.open(camera_image).convert("RGB")

        processed_image = detect_objects(image)

        st.session_state.processed_images.append(
            processed_image
        )



    else:

        st.warning(
            "Please upload an image or take a picture using the camera."
        )


if st.session_state.processed_images:

    st.markdown("### Processed Image(s)")

    for i, processed_image in enumerate(
        st.session_state.processed_images
    ):

        st.image(
            processed_image,
            caption=f"Processed Image {i + 1}",
            use_container_width=True
        )
