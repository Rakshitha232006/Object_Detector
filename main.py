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
# Custom CSS (Matches Gradio dark theme layout)
# --------------------------------------------------

st.markdown(
    """
    <style>
    /* Main app background */
    .stApp {
        background-color: #0E1117;
    }

    /* Container border & styling for uploader */
    [data-testid="stFileUploader"] {
        background-color: #2B2D30;
        border: 2px dashed #4E5157;
        border-radius: 12px;
        padding: 2rem 1rem;
    }

    /* Hide default Streamlit subtext inside dropzone (200MB per file...) */
    [data-testid="stFileUploaderDropzoneInstructions"] > div:nth-child(2) {
        display: none !important;
    }

    /* Custom label styling */
    .field-label {
        color: #E0E0E0;
        font-weight: 500;
        font-size: 0.95rem;
        margin-bottom: 6px;
    }

    /* Submit button (Orange) */
    div.stButton > button[kind="primary"] {
        background-color: #FF5200 !important;
        color: #FFFFFF !important;
        border-radius: 8px;
        height: 3.2em;
        font-size: 1.1rem;
        font-weight: 600;
        border: none;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #E04800 !important;
    }

    /* Clear button (Gray) */
    div.stButton > button[kind="secondary"] {
        background-color: #4E5157 !important;
        color: #FFFFFF !important;
        border-radius: 8px;
        height: 3.2em;
        font-size: 1.1rem;
        font-weight: 600;
        border: none;
    }
    div.stButton > button[kind="secondary"]:hover {
        background-color: #3D4045 !important;
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
# UI Component Layout
# --------------------------------------------------

# Header label
st.markdown('<div class="field-label">Select an image</div>', unsafe_allow_html=True)

# Image upload dropzone
uploaded_files = st.file_uploader(
    "Drop Image Here\n- or -\nClick to Upload",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True,
    label_visibility="collapsed"
)

# Optional Camera Input
camera_image = st.camera_input(
    "📷 Take a picture",
    label_visibility="visible"
)

st.write("")

# Side-by-side action buttons
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
# Logic Execution
# --------------------------------------------------

if clear_clicked:
    st.session_state.processed_images = []
    st.rerun()

if submit_clicked:
    if uploaded_files:
        st.session_state.processed_images = []
        for uploaded_file in uploaded_files:
            image = Image.open(uploaded_file).convert("RGB")
            processed_image = detect_objects(image)
            st.session_state.processed_images.append(processed_image)

    elif camera_image is not None:
        st.session_state.processed_images = []
        image = Image.open(camera_image).convert("RGB")
        processed_image = detect_objects(image)
        st.session_state.processed_images.append(processed_image)

    else:
        st.warning("Please upload an image or take a picture using the camera.")

if st.session_state.processed_images:
    st.markdown("### Processed Image(s)")
    for i, processed_image in enumerate(st.session_state.processed_images):
        st.image(
            processed_image,
            caption=f"Processed Image {i + 1}",
            use_container_width=True
        )
