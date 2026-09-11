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
# CSS
# --------------------------------------------------

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background-color: #0B0F19;
    }

    .main .block-container {
        max-width: 760px;
        padding-top: 35px;
    }


    /* Label */
    .field-label {
        color: #E5E7EB;
        font-size: 15px;
        margin-bottom: 6px;
    }


    /* --------------------------------------------
       FILE UPLOADER
       -------------------------------------------- */

    [data-testid="stFileUploader"] {
        background-color: #24262C !important;
        border: 1px dashed #4D5057 !important;
        border-radius: 6px !important;
        padding: 0 !important;
    }

    [data-testid="stFileUploaderDropzone"] {
        background-color: #24262C !important;
        border: none !important;
        min-height: 250px !important;

        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }


    /* Hide Streamlit's default text */

    [data-testid="stFileUploaderDropzoneInstructions"] span {
        display: none !important;
    }

    [data-testid="stFileUploaderDropzoneInstructions"] div {
        display: none !important;
    }


    /* Upload arrow */

    [data-testid="stFileUploaderDropzoneInstructions"]::before {
        content: "↑";
        display: block;
        text-align: center;

        color: #E5E7EB;
        font-size: 42px;
        font-weight: 300;

        margin-bottom: 8px;
    }


    /* Upload text */

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


    /* Hide Browse button */

    [data-testid="stFileUploaderDropzone"] button {
        display: none !important;
    }


    /* --------------------------------------------
       ICON BAR
       -------------------------------------------- */

    .icon-bar {
        height: 40px;

        background-color: #24262C;

        border-top: 1px solid #373A40;

        display: flex;
        align-items: center;
        justify-content: center;

        gap: 24px;

        color: #9CA3AF;
    }


    /* --------------------------------------------
       ICON BUTTONS
       -------------------------------------------- */

    div.stButton > button {
        border: none !important;
        box-shadow: none !important;
    }


    .icon-button button {
        background: transparent !important;

        color: #9CA3AF !important;

        font-size: 20px !important;

        padding: 0 !important;

        height: 30px !important;

        min-height: 30px !important;
    }


    .icon-button button:hover {
        color: #FF5200 !important;
    }


    /* --------------------------------------------
       CAMERA
       -------------------------------------------- */

    [data-testid="stCameraInput"] {
        margin-top: 10px;
    }


    /* --------------------------------------------
       ACTION BUTTONS
       -------------------------------------------- */

    div.stButton > button[kind="secondary"] {
        background-color: #555761 !important;
        color: white !important;

        border-radius: 6px !important;

        height: 42px !important;

        font-size: 16px !important;
        font-weight: 600 !important;
    }


    div.stButton > button[kind="primary"] {
        background-color: #FF5200 !important;
        color: white !important;

        border-radius: 6px !important;

        height: 42px !important;

        font-size: 16px !important;
        font-weight: 600 !important;
    }


    /* Remove unnecessary uploader bottom spacing */

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

if "show_camera" not in st.session_state:
    st.session_state.show_camera = False


# --------------------------------------------------
# Label
# --------------------------------------------------

st.markdown(
    '<div class="field-label">🖼️ Select an image</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# File uploader
# --------------------------------------------------

uploaded_files = st.file_uploader(
    "Upload Image",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True,
    label_visibility="collapsed"
)


# --------------------------------------------------
# Icon bar
# --------------------------------------------------

icon_col1, icon_col2, icon_col3 = st.columns(
    [1, 1, 1]
)

with icon_col1:

    upload_clicked = st.button(
        "📤",
        key="upload_icon"
    )

with icon_col2:

    camera_clicked = st.button(
        "📷",
        key="camera_icon"
    )

with icon_col3:

    gallery_clicked = st.button(
        "📋",
        key="gallery_icon"
    )


# --------------------------------------------------
# Camera button
# --------------------------------------------------

if camera_clicked:

    st.session_state.show_camera = True


# --------------------------------------------------
# Camera input
# --------------------------------------------------

camera_image = None

if st.session_state.show_camera:

    st.markdown("#### Take a picture")

    camera_image = st.camera_input(
        "Camera",
        label_visibility="collapsed"
    )


# --------------------------------------------------
# Action buttons
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

    st.session_state.show_camera = False

    st.rerun()


# --------------------------------------------------
# Submit
# --------------------------------------------------

if submit_clicked:

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

    elif camera_image:

        image = Image.open(
            camera_image
        ).convert("RGB")

        processed_image = detect_objects(image)

        st.session_state.processed_images.append(
            processed_image
        )


    # ----------------------------------------------
    # Nothing selected
    # ----------------------------------------------

    else:

        st.warning(
            "Please upload an image or take a picture."
        )


# --------------------------------------------------
# Display processed images
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
