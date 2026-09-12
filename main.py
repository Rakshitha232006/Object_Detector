import streamlit as st
from PIL import Image

from object_detector import detect_objects


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="Object Detection",
    page_icon="🔍",
    layout="centered"
)


# ==================================================
# SESSION STATE
# ==================================================

if "show_camera" not in st.session_state:

    st.session_state.show_camera = False


if "processed_images" not in st.session_state:

    st.session_state.processed_images = []


# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown(
    """
    <style>

    /* --------------------------------------------
       Main page
       -------------------------------------------- */

    .stApp {
        background-color: #0B0F19;
    }


    .main .block-container {

        max-width: 800px;

        padding-top: 40px;
        padding-bottom: 40px;
    }


    /* --------------------------------------------
       Title
       -------------------------------------------- */

    h1 {

        text-align: center;

        color: white;

        margin-bottom: 10px;
    }


    /* --------------------------------------------
       Description
       -------------------------------------------- */

    .description {

        text-align: center;

        color: #AEB4C0;

        font-size: 16px;

        margin-bottom: 30px;
    }


    /* --------------------------------------------
       Upload area
       -------------------------------------------- */

    [data-testid="stFileUploader"] {

        background-color: #24262C !important;

        border-radius: 8px !important;

        padding: 15px !important;

        border: 1px solid #3B3E46 !important;
    }


    /* --------------------------------------------
       Camera section
       -------------------------------------------- */

    .camera-title {

        color: white;

        font-size: 20px;

        font-weight: 600;

        margin-top: 20px;

        margin-bottom: 10px;
    }


    /* --------------------------------------------
       Buttons
       -------------------------------------------- */

    div.stButton > button {

        height: 45px !important;

        border-radius: 7px !important;

        font-size: 16px !important;

        font-weight: 600 !important;
    }


    /* Camera button */

    div.stButton > button[kind="secondary"] {

        background-color: #555761 !important;

        color: white !important;

        border: none !important;
    }


    /* Submit button */

    div.stButton > button[kind="primary"] {

        background-color: #FF5200 !important;

        color: white !important;

        border: none !important;
    }


    /* --------------------------------------------
       Result heading
       -------------------------------------------- */

    .result-title {

        color: white;

        font-size: 22px;

        font-weight: 600;

        margin-top: 30px;

        margin-bottom: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# TITLE
# ==================================================

st.title("🔍 Object Detection")

st.markdown(
    """
    <div class="description">
        Upload an image or use your camera to detect objects.
    </div>
    """,
    unsafe_allow_html=True
)


# ==================================================
# UPLOAD IMAGES
# ==================================================

st.subheader("📁 Upload Images")

uploaded_files = st.file_uploader(
    "Choose image(s)",
    type=[
        "jpg",
        "jpeg",
        "png"
    ],
    accept_multiple_files=True
)


# ==================================================
# CAMERA BUTTON
# ==================================================

st.write("")

camera_button = st.button(
    "📷 Open Camera",
    type="secondary",
    use_container_width=True
)


# ==================================================
# OPEN CAMERA ONLY AFTER BUTTON CLICK
# ==================================================

if camera_button:

    st.session_state.show_camera = True


# ==================================================
# CAMERA
# ==================================================

camera_image = None


if st.session_state.show_camera:

    st.markdown(
        '<div class="camera-title">📷 Camera</div>',
        unsafe_allow_html=True
    )

    camera_image = st.camera_input(
        "Take a picture",
        label_visibility="collapsed"
    )


# ==================================================
# CLEAR AND SUBMIT
# ==================================================

st.write("")

col1, col2 = st.columns(
    2,
    gap="medium"
)


# --------------------------------------------------
# Clear
# --------------------------------------------------

with col1:

    clear_button = st.button(
        "Clear",
        type="secondary",
        use_container_width=True
    )


# --------------------------------------------------
# Submit
# --------------------------------------------------

with col2:

    submit_button = st.button(
        "Submit",
        type="primary",
        use_container_width=True
    )


# ==================================================
# CLEAR
# ==================================================

if clear_button:

    st.session_state.processed_images = []

    st.session_state.show_camera = False

    st.rerun()


# ==================================================
# SUBMIT
# ==================================================

if submit_button:

    # Clear previous results

    st.session_state.processed_images = []


    # =================================================
    # UPLOADED IMAGES
    # =================================================

    if uploaded_files:

        for uploaded_file in uploaded_files:

            image = Image.open(
                uploaded_file
            ).convert("RGB")


            # Run object detection

            result, detections = detect_objects(
                image
            )


            # Save result

            st.session_state.processed_images.append(
                result
            )


            # Show detection status

            if detections:

                st.success(
                    f"Detected {len(detections)} object(s) "
                    f"in {uploaded_file.name}"
                )

            else:

                st.info(
                    f"No recognizable objects were "
                    f"detected in {uploaded_file.name}."
                )


    # =================================================
    # CAMERA IMAGE
    # =================================================

    elif camera_image is not None:

        image = Image.open(
            camera_image
        ).convert("RGB")


        # Run object detection

        result, detections = detect_objects(
            image
        )


        # Save result

        st.session_state.processed_images.append(
            result
        )


        # Show detection status

        if detections:

            st.success(
                f"Detected {len(detections)} object(s)."
            )

        else:

            st.info(
                "No recognizable objects were detected "
                "in this image."
            )


    # =================================================
    # NOTHING SELECTED
    # =================================================

    else:

        st.warning(
            "Please upload an image or open the camera "
            "and take a picture."
        )


# ==================================================
# DISPLAY RESULTS
# ==================================================

if st.session_state.processed_images:

    st.markdown(
        '<div class="result-title">Processed Images</div>',
        unsafe_allow_html=True
    )


    for i, processed_image in enumerate(
        st.session_state.processed_images
    ):

        st.image(
            processed_image,
            caption=f"Processed Image {i + 1}",
            use_container_width=True
        )