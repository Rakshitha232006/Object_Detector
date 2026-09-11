import streamlit as st
from PIL import Image

from object_detector import detect_objects


st.set_page_config(
    page_title="Object Detection",
    page_icon="🔎",
    layout="centered"
)


st.title("🔎 Object Detection")

st.write(
    "Upload an image or turn on the camera when you want to detect objects."
)


# -----------------------------
# INPUT AREA
# -----------------------------

st.markdown("### Select image(s)")

# Main upload box
uploaded_files = st.file_uploader(
    "Upload",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True,
    label_visibility="collapsed"
)


# Small camera button
st.markdown(
    """
    <style>
    div[data-testid="stFileUploader"] {
        margin-bottom: 5px;
    }

    .camera-title {
        font-size: 14px;
        margin-top: 5px;
        margin-bottom: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

camera_button = st.button(
    "📷 Open Camera",
    use_container_width=False
)


camera_image = None

if camera_button:
    st.session_state["camera_open"] = True


if "camera_open" not in st.session_state:
    st.session_state["camera_open"] = False


# Camera is ONLY created after clicking the button
if st.session_state["camera_open"]:

    st.markdown("### 📷 Camera")

    camera_image = st.camera_input(
        "Take a picture",
        label_visibility="collapsed"
    )

    if st.button("Close Camera"):
        st.session_state["camera_open"] = False
        st.rerun()


# -----------------------------
# DETECTION BUTTON
# -----------------------------

st.write("")

detect_button = st.button(
    "🔍 Detect Objects",
    type="primary",
    use_container_width=True
)


# -----------------------------
# DETECTION
# -----------------------------

if detect_button:

    images_to_process = []

    # Uploaded images
    if uploaded_files:

        for uploaded_file in uploaded_files:

            image = Image.open(uploaded_file).convert("RGB")

            images_to_process.append(
                (uploaded_file.name, image)
            )


    # Camera image
    if camera_image is not None:

        image = Image.open(camera_image).convert("RGB")

        images_to_process.append(
            ("Camera Image", image)
        )


    # Nothing selected
    if not images_to_process:

        st.warning(
            "Please upload an image or take a picture using the camera."
        )

    else:

        st.success(
            f"{len(images_to_process)} image(s) selected."
        )


        # Process every image
        for image_name, image in images_to_process:

            st.subheader(image_name)

            with st.spinner("Detecting objects..."):

                processed_image = detect_objects(image)


            st.image(
                processed_image,
                caption="Processed image",
                use_container_width=True
            )
