import streamlit as st
from PIL import Image

from object_detector import detect_objects


st.set_page_config(
    page_title="Object Detection",
    page_icon="🔍",
    layout="centered"
)

st.title("Object Detection")
st.write(
    "Upload images or use the camera to detect objects using DETR."
)


if "camera_on" not in st.session_state:
    st.session_state.camera_on = False


uploaded_files = st.file_uploader(
    "Upload images",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)



if not st.session_state.camera_on:

    if st.button("📷 Open Camera"):
        st.session_state.camera_on = True
        st.rerun()

else:

    st.write("### 📷 Camera")

    camera_file = st.camera_input(
        "Take a picture"
    )

    if camera_file is not None:

        if st.button("❌ Close Camera"):
            st.session_state.camera_on = False
            st.rerun()

    else:

        if st.button("❌ Close Camera"):
            st.session_state.camera_on = False
            st.rerun()



images = []


# Uploaded images
if uploaded_files:

    for uploaded_file in uploaded_files:

        image = Image.open(
            uploaded_file
        ).convert("RGB")

        images.append(
            (uploaded_file.name, image)
        )


# Camera image
if (
    st.session_state.camera_on
    and "camera_file" in locals()
    and camera_file is not None
):

    camera_image = Image.open(
        camera_file
    ).convert("RGB")

    images.append(
        ("Camera image", camera_image)
    )


if images:

    st.subheader(
        f"{len(images)} image(s) selected"
    )

    for name, image in images:

        st.image(
            image,
            caption=name,
            width=500
        )



if images:

    st.write("")

    if st.button(
        "🔍 Detect Objects",
        use_container_width=True
    ):

        for name, image in images:

            with st.spinner(
                f"Detecting objects in {name}..."
            ):

                processed_image = detect_objects(
                    image
                )

            st.subheader(
                f"Result: {name}"
            )

            st.image(
                processed_image,
                caption="Processed image",
                width=700
            )
