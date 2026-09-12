import streamlit as st
from PIL import Image
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
import av
import numpy as np

from object_detector import detect_objects


# ==================================================
# PAGE
# ==================================================

st.set_page_config(
    page_title="Object Detection",
    page_icon="🔍",
    layout="centered"
)


# ==================================================
# CSS
# ==================================================

st.markdown(
    """
    <style>

    /* ---------------- PAGE ---------------- */

    .stApp {
        background: #0B0F19;
    }

    .main .block-container {
        max-width: 880px;
        padding-top: 35px;
    }


    /* ---------------- LABEL ---------------- */

    .field-label {
        color: #E5E7EB;
        font-size: 15px;
        margin-bottom: 7px;
    }


    /* ---------------- DROPZONE ---------------- */

    .dropzone {
        height: 310px;
        background: #24262C;
        border: 1px dashed #4D5057;
        border-radius: 6px;

        display: flex;
        flex-direction: column;

        align-items: center;
        justify-content: center;

        text-align: center;

        color: #E5E7EB;
    }

    .upload-arrow {
        font-size: 48px;
        font-weight: 300;
        line-height: 1;
        margin-bottom: 12px;
    }

    .drop-title {
        font-size: 17px;
        font-weight: 500;
    }

    .drop-or {
        font-size: 17px;
        margin: 6px 0;
    }


    /* ---------------- ICONS ---------------- */

    .icon-space {
        height: 45px;
        display: flex;
        justify-content: center;
        align-items: center;
    }


    /* ---------------- BUTTONS ---------------- */

    div.stButton > button {
        border-radius: 7px !important;
        border: none !important;
        height: 52px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
    }

    div.stButton > button[kind="secondary"] {
        background: #555761 !important;
        color: white !important;
    }

    div.stButton > button[kind="primary"] {
        background: #FF5200 !important;
        color: white !important;
    }


    /* ---------------- HIDE FILE UPLOADER ---------------- */

    .hidden-uploader {
        display: none;
    }


    /* ---------------- CAMERA ---------------- */

    .camera-box {
        margin-top: 15px;
        padding: 10px;
        background: #24262C;
        border-radius: 7px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# SESSION STATE
# ==================================================

if "processed_images" not in st.session_state:
    st.session_state.processed_images = []

if "show_camera" not in st.session_state:
    st.session_state.show_camera = False

if "camera_frame" not in st.session_state:
    st.session_state.camera_frame = None


# ==================================================
# CAMERA PROCESSOR
# ==================================================

class CameraProcessor(VideoProcessorBase):

    def __init__(self):
        self.frame = None

    def recv(self, frame):

        img = frame.to_ndarray(format="rgb24")

        self.frame = img

        return av.VideoFrame.from_ndarray(
            img,
            format="rgb24"
        )


# ==================================================
# LABEL
# ==================================================

st.markdown(
    '<div class="field-label">🖼️ Select an image</div>',
    unsafe_allow_html=True
)


# ==================================================
# CUSTOM DROPZONE
# ==================================================

st.markdown(
    """
    <div class="dropzone">

        <div class="upload-arrow">↑</div>

        <div class="drop-title">
            Drop Image Here
        </div>

        <div class="drop-or">
            - or -
        </div>

        <div class="drop-title">
            Click to Upload
        </div>

    </div>
    """,
    unsafe_allow_html=True
)

# ==================================================
# REAL FILE UPLOADER
# ==================================================

uploaded_files = st.file_uploader(
    "Upload",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True,
    label_visibility="collapsed"
)


# ==================================================
# ICON ROW
# ==================================================

st.markdown(
    '<div class="icon-space">',
    unsafe_allow_html=True
)

c1, c2, c3 = st.columns(
    [0.47, 0.06, 0.47]
)

with c1:
    pass

with c2:

    camera_clicked = st.button(
        "📷",
        key="camera_button"
    )

with c3:
    pass

st.markdown(
    '</div>',
    unsafe_allow_html=True
)


# ==================================================
# CAMERA
# ==================================================

if camera_clicked:

    st.session_state.show_camera = True


if st.session_state.show_camera:

    st.markdown(
        '<div class="camera-box">',
        unsafe_allow_html=True
    )

    ctx = webrtc_streamer(
        key="object-detection-camera",
        video_processor_factory=CameraProcessor,
        media_stream_constraints={
            "video": True,
            "audio": False
        },
        async_processing=True,
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )

    if ctx.video_processor:

        frame = ctx.video_processor.frame

        if frame is not None:

            if st.button(
                "Capture Image",
                use_container_width=True
            ):

                st.session_state.camera_frame = frame.copy()

                st.success(
                    "Image captured successfully!"
                )


# ==================================================
# SHOW CAPTURED CAMERA IMAGE
# ==================================================

if st.session_state.camera_frame is not None:

    camera_image = Image.fromarray(
        st.session_state.camera_frame
    )

    st.image(
        camera_image,
        caption="Captured Image",
        use_container_width=True
    )

else:

    camera_image = None


# ==================================================
# CLEAR / SUBMIT
# ==================================================

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


# ==================================================
# CLEAR
# ==================================================

if clear_clicked:

    st.session_state.processed_images = []

    st.session_state.camera_frame = None

    st.session_state.show_camera = False

    st.rerun()


# ==================================================
# SUBMIT
# ==================================================

if submit_clicked:

    st.session_state.processed_images = []


    # ---------------- UPLOAD ----------------

    if uploaded_files:

        for uploaded_file in uploaded_files:

            image = Image.open(
                uploaded_file
            ).convert("RGB")

            processed_image = detect_objects(
                image
            )

            st.session_state.processed_images.append(
                processed_image
            )


    # ---------------- CAMERA ----------------

    elif st.session_state.camera_frame is not None:

        image = Image.fromarray(
            st.session_state.camera_frame
        ).convert("RGB")

        processed_image = detect_objects(
            image
        )

        st.session_state.processed_images.append(
            processed_image
        )


    # ---------------- NOTHING ----------------

    else:

        st.warning(
            "Please upload an image or capture one using the camera."
        )


# ==================================================
# RESULTS
# ==================================================

if st.session_state.processed_images:

    st.markdown("### Processed Image(s)")

    for i, image in enumerate(
        st.session_state.processed_images
    ):

        st.image(
            image,
            caption=f"Processed Image {i + 1}",
            use_container_width=True
        )