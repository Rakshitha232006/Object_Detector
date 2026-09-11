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

    /* ================================
       MAIN BACKGROUND
       ================================ */

    .stApp {
        background-color: #0B0F19;
    }

    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 900px;
    }


    /* ================================
       LABEL
       ================================ */

    .field-label {
        color: #C9D1D9;
        font-size: 14px;
        margin-bottom: 6px;
    }


    /* ================================
       MAIN DROPZONE
       ================================ */

    [data-testid="stFileUploader"] {
        background-color: #21252D !important;
        border: 1px dashed #4E5157 !important;
        border-radius: 6px !important;
        min-height: 280px !important;
        padding: 0 !important;
    }

    [data-testid="stFileUploaderDropzone"] {
        background-color: #21252D !important;
        border: none !important;
        min-height: 230px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }


    /* Hide default Streamlit text */

    [data-testid="stFileUploaderDropzoneInstructions"] span {
        display: none !important;
    }

    [data-testid="stFileUploaderDropzoneInstructions"] div {
        display: none !important;
    }


    /* Our upload area text */

    [data-testid="stFileUploaderDropzoneInstructions"]::before {
        content: "↑";
        display: block;
        color: #E5E7EB;
        font-size: 42px;
        font-weight: 300;
        margin-bottom: 8px;
    }

    [data-testid="stFileUploaderDropzoneInstructions"]::after {
        content: "Drop Image Here\\A - or -\\A Click to Upload";
        white-space: pre-wrap;
        display: block;
        text-align: center;
        color: #E5E7EB;
        font-size: 16px;
        font-weight: 500;
        line-height: 1.6;
    }


    /* Hide browse button */

    [data-testid="stFileUploaderDropzone"] button {
        display: none !important;
    }


    /* ================================
       FOOTER ICON AREA
       ================================ */

    .icon-area {
        height: 42px;
        background-color: #21252D;
        border-top: 1px solid #363940;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 30px;
    }


    /* ================================
       CAMERA WIDGET
       ================================ */

    [data-testid="stCameraInput"] {
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }

    [data-testid="stCameraInput"] label {
        display: none !important;
    }

    [data-testid="stCameraInput"] button {
        background: transparent !important;
        border: none !important;
        color: #9CA3AF !important;
        font-size: 24px !important;
        padding: 2px !important;
    }


    /* ================================
       BUTTONS
       ================================ */

    div.stButton > button {
        height: 42px !important;
        border-radius: 6px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
    }


    /* Clear */

    div.stButton > button[kind="secondary"] {
        background-color: #555761 !important;
        color: white !important;
        border: none !important;
    }


    /* Submit */

    div.stButton > button[kind="primary"] {
        background-color: #FF5200 !important;
        color: white !important;
        border: none !important;
    }


    /* ================================
       REMOVE EXTRA SPACING
       ================================ */

    [data-testid="stFileUploader"] section {
        padding-bottom: 0 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# Session State
# --------------------------------------------------

if "processed_images" not in st.session_state:
    st.session_state.processed_images = []

if "camera_open" not in st.session_state:
    st.session_state.camera_open = False


# --------------------------------------------------
# Label
# --------------------------------------------------

st.markdown(
    '<div class="field-label">🖼️ Select an image</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# File Upload
# --------------------------------------------------

uploaded_files = st.file_uploader(
    "Upload Image",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True,
    label_visibility="collapsed"
)


# --------------------------------------------------
# Camera
# --------------------------------------------------

camera_image = st.camera_input(
    "Take a picture",
    label_visibility="collapsed"
)


# --------------------------------------------------
# Action Buttons
# --------------------------------------------------

st.write("")

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


# --------------------------------------------------
# Clear
# --------------------------------------------------

if clear_clicked:

    st.session_state.processed_images = []

    st.rerun()


# --------------------------------------------------
# Submit
# --------------------------------------------------

if submit_clicked:

    st.session_state.processed_images = []

    # Uploaded images
    if uploaded_files:

        for uploaded_file in uploaded_files:

            image = Image.open(
                uploaded_file
            ).convert("RGB")

            processed_image = detect_objects(image)

            st.session_state.processed_images.append(
                processed_image
            )

    # Camera image
    elif camera_image:

        image = Image.open(
            camera_image
        ).convert("RGB")

        processed_image = detect_objects(image)

        st.session_state.processed_images.append(
            processed_image
        )

    else:

        st.warning(
            "Please upload an image or take a picture."
        )


# --------------------------------------------------
# Display Results
# --------------------------------------------------

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
