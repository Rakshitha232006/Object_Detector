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

    /* ============================================
       PAGE
       ============================================ */

    .stApp {
        background-color: #0B0F19;
    }

    .main .block-container {
        max-width: 880px;
        padding-top: 35px;
        padding-bottom: 30px;
    }


    /* ============================================
       LABEL
       ============================================ */

    .field-label {
        color: #E5E7EB;
        font-size: 15px;
        margin-bottom: 7px;
    }


    /* ============================================
       UPLOAD BOX
       ============================================ */

    [data-testid="stFileUploader"] {
        background-color: #24262C !important;
        border: 1px dashed #4D5057 !important;
        border-radius: 6px !important;
        padding: 0 !important;
        overflow: hidden !important;
    }


    [data-testid="stFileUploaderDropzone"] {
        background-color: #24262C !important;
        border: none !important;

        height: 310px !important;
        min-height: 310px !important;

        position: relative !important;

        display: block !important;
    }


    /* ============================================
       CENTER UPLOAD MESSAGE
       ============================================ */

    [data-testid="stFileUploaderDropzoneInstructions"] {

        position: absolute !important;

        left: 0 !important;
        right: 0 !important;

        top: 50% !important;

        transform: translateY(-50%) !important;

        width: 100% !important;

        display: block !important;

        text-align: center !important;

        margin: 0 !important;
        padding: 0 !important;
    }


    /* Hide Streamlit's original text */

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

        font-size: 44px;

        font-weight: 300;

        line-height: 1;

        margin-bottom: 10px;
    }


    /* Upload text */

    [data-testid="stFileUploaderDropzoneInstructions"]::after {

        content: "Drop Image Here\\A - or -\\A Click to Upload";

        white-space: pre-wrap;

        display: block;

        text-align: center;

        color: #E5E7EB;

        font-size: 17px;

        font-weight: 500;

        line-height: 1.65;
    }


    /* Hide default Browse button */

    [data-testid="stFileUploaderDropzone"] button {
        display: none !important;
    }


    /* ============================================
       ICON ROW
       ============================================ */

    .icon-row {
        margin-top: 0px;
        margin-bottom: 20px;
    }


    /* Icon buttons */

    .icon-row button {

        width: 54px !important;
        height: 54px !important;

        min-height: 54px !important;

        background-color: #555761 !important;

        color: #E5E7EB !important;

        border: none !important;

        border-radius: 7px !important;

        padding: 0 !important;

        font-size: 20px !important;

        box-shadow: none !important;
    }


    .icon-row button:hover {

        background-color: #62646E !important;

        color: #FFFFFF !important;
    }


    /* ============================================
       ACTION BUTTONS
       ============================================ */

    .action-row {
        margin-top: 8px;
    }


    div.stButton > button[kind="secondary"] {

        background-color: #555761 !important;

        color: #FFFFFF !important;

        border: none !important;

        border-radius: 7px !important;

        height: 52px !important;

        min-height: 52px !important;

        font-size: 16px !important;

        font-weight: 600 !important;
    }


    div.stButton > button[kind="primary"] {

        background-color: #FF5200 !important;

        color: #FFFFFF !important;

        border: none !important;

        border-radius: 7px !important;

        height: 52px !important;

        min-height: 52px !important;

        font-size: 16px !important;

        font-weight: 600 !important;
    }


    /* ============================================
       CAMERA
       ============================================ */

    [data-testid="stCameraInput"] {
        margin-top: 10px;
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
# Icon row
# --------------------------------------------------

st.markdown('<div class="icon-row">', unsafe_allow_html=True)

# Empty space + 3 small columns + empty space
c1, c2, c3, c4, c5 = st.columns(
    [1, 0.12, 0.12, 0.12, 1],
    gap="small"
)


with c2:

    upload_clicked = st.button(
        "📤",
        key="upload_icon",
        use_container_width=True
    )


with c3:

    camera_clicked = st.button(
        "📷",
        key="camera_icon",
        use_container_width=True
    )


with c4:

    gallery_clicked = st.button(
        "📋",
        key="gallery_icon",
        use_container_width=True
    )

st.markdown('</div>', unsafe_allow_html=True)


# --------------------------------------------------
# Camera
# --------------------------------------------------

if camera_clicked:

    st.session_state.show_camera = True


camera_image = None

if st.session_state.show_camera:

    camera_image = st.camera_input(
        "Take a picture",
        label_visibility="collapsed"
    )


# --------------------------------------------------
# Clear + Submit
# --------------------------------------------------

st.markdown(
    '<div class="action-row">',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2, gap="medium")


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

st.markdown('</div>', unsafe_allow_html=True)


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
# Results
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
