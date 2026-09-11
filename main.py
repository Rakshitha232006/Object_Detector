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
# Custom CSS for exact Gradio-style Dropzone
# --------------------------------------------------
st.markdown(
    """
    <style>
    /* Dark background matching Gradio */
    .stApp {
        background-color: #0B0F19;
    }

    /* Container for file uploader */
    [data-testid="stFileUploader"] {
        background-color: #21252D !important;
        border: 1px dashed #4E5157 !important;
        border-radius: 8px !important;
        padding: 30px 20px !important;
        text-align: center !important;
    }

    /* Hide Streamlit's default "Browse files" button and text */
    [data-testid="stFileUploaderDropzone"] button {
        display: none !important;
    }
    [data-testid="stFileUploaderDropzoneInstructions"] > div:nth-child(2) {
        display: none !important;
    }

    /* Add Upload Icon & format prompt text */
    [data-testid="stFileUploaderDropzoneInstructions"]::before {
        content: "⬆";
        display: block;
        font-size: 32px;
        color: #A0AAB8;
        margin-bottom: 8px;
    }
    
    [data-testid="stFileUploaderDropzoneInstructions"]::after {
        content: "Drop Image Here\\A - or -\\A Click to Upload";
        white-space: pre-wrap;
        display: block;
        color: #E0E0E0;
        font-size: 18px;
        font-weight: 500;
        line-height: 1.5;
    }

    /* Hide the original label text inside instructions */
    [data-testid="stFileUploaderDropzoneInstructions"] span {
        display: none !important;
    }

    /* Label styling above component */
    .field-label {
        color: #C9D1D9;
        font-size: 0.9rem;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* Buttons */
    div.stButton > button[kind="primary"] {
        background-color: #FF5200 !important;
        color: #FFFFFF !important;
        border-radius: 6px;
        height: 3.2em;
        font-size: 1.05rem;
        font-weight: 600;
        border: none;
    }
    div.stButton > button[kind="secondary"] {
        background-color: #373A40 !important;
        color: #FFFFFF !important;
        border-radius: 6px;
        height: 3.2em;
        font-size: 1.05rem;
        font-weight: 600;
        border: none;
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
# Header & File Uploader
# --------------------------------------------------
st.markdown('<div class="field-label">🖼️ Select an image</div>', unsafe_allow_html=True)

uploaded_files = st.file_uploader(
    "",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True,
    label_visibility="collapsed"
)

# Optional Camera Input
camera_image = st.camera_input("📷 Take a picture", label_visibility="visible")

st.write("")

# Action Buttons
col1, col2 = st.columns(2)

with col1:
    clear_clicked = st.button("Clear", type="secondary", use_container_width=True)

with col2:
    submit_clicked = st.button("Submit", type="primary", use_container_width=True)

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
        st.image(processed_image, caption=f"Processed Image {i + 1}", use_container_width=True)
