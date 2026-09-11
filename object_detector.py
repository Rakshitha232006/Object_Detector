import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from transformers import pipeline


model_path = "facebook/detr-resnet-50"

object_detector = pipeline(
    "object-detection",
    model=model_path
)

def draw_boundaring_boxes(image, detections):

    draw_image = image.copy()
    draw = ImageDraw.Draw(draw_image)

    # Use a smaller font
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 50)
    except:
        font = ImageFont.load_default()

    label_positions = []

    for detection in detections:

        box = detection["box"]

        xmin = int(box["xmin"])
        ymin = int(box["ymin"])
        xmax = int(box["xmax"])
        ymax = int(box["ymax"])

        # Bounding box
        draw.rectangle(
            [(xmin, ymin), (xmax, ymax)],
            outline="red",
            width=4
        )

        label = detection["label"]
        score = detection["score"]

        text = f"{label} {score:.2f}"

        bbox = draw.textbbox(
            (0, 0),
            text,
            font=font
        )

        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Start above the bounding box
        text_x = xmin
        text_y = ymin - text_height - 5

        # If there isn't enough space above,
        # put the label inside the box
        if text_y < 0:
            text_y = ymin + 5

        # Avoid overlapping labels
        while any(
            abs(text_y - previous_y) < text_height + 5
            and abs(text_x - previous_x) < text_width
            for previous_x, previous_y in label_positions
        ):
            text_y += text_height + 5

        # Keep label inside image
        if text_y + text_height > image.height:
            text_y = image.height - text_height - 5

        # Label background
        draw.rectangle(
            [
                text_x,
                text_y,
                text_x + text_width + 8,
                text_y + text_height + 5
            ],
            fill="red"
        )

        # Label text
        draw.text(
            (text_x + 4, text_y + 2),
            text,
            fill="white",
            font=font
        )

        label_positions.append(
            (text_x, text_y)
        )

    return draw_image


def detect_objects(image):

    if image is None:
        return None

    output = object_detector(image)

    processed_image = draw_boundaring_boxes(
        image,
        output
    )

    return processed_image


st.set_page_config(
    page_title="Object Detection",
    page_icon="🔍",
    layout="centered"
)

st.title("🔍 Object Detection")

st.write(
    "Upload an image or turn on the camera when you want to detect objects."
)


input_method = st.radio(
    "Choose input method:",
    ["Upload Image", "Camera"],
    horizontal=True
)


if input_method == "Upload Image":

    uploaded_files = st.file_uploader(
        "Select image(s)",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True
    )

    if uploaded_files:

        if st.button("Detect Objects", type="primary"):

            for uploaded_file in uploaded_files:

                image = Image.open(uploaded_file).convert("RGB")

                st.subheader(uploaded_file.name)

                processed_image = detect_objects(image)

                st.image(
                    processed_image,
                    use_container_width=True
                )


else:

    st.write("📷 Turn on your camera only when you want to detect an object.")

    camera_image = st.camera_input(
        "Take a picture"
    )

    if camera_image:

        image = Image.open(camera_image).convert("RGB")

        if st.button("Detect Object", type="primary"):

            processed_image = detect_objects(image)

            st.image(
                processed_image,
                use_container_width=True
            )
