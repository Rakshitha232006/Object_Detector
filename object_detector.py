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

    # Medium-sized font
    font = ImageFont.load_default(size=32)

    label_positions = []

    for detection in detections:
        box = detection["box"]

        xmin = int(box["xmin"])
        ymin = int(box["ymin"])
        xmax = int(box["xmax"])
        ymax = int(box["ymax"])

        # Draw bounding box
        draw.rectangle(
            [(xmin, ymin), (xmax, ymax)],
            outline="red",
            width=5
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
        text_y = ymin - text_height

        # If there isn't enough room above,
        # put the label below the top of the box
        if text_y < 0:
            text_y = ymin

        # Prevent labels from overlapping
        while any(
            abs(text_y - previous_y) < text_height + 5
            and abs(text_x - previous_x) < text_width
            for previous_x, previous_y in label_positions
        ):
            text_y += text_height + 5

        # Keep label inside image
        image_height = draw_image.height

        if text_y + text_height > image_height:
            text_y = max(0, ymin)

        # Label background
        draw.rectangle(
            [
                text_x,
                text_y,
                text_x + text_width + 6,
                text_y + text_height + 4
            ],
            fill="red"
        )

        # Label text
        draw.text(
            (text_x + 3, text_y + 2),
            text,
            fill="white",
            font=font
        )

        label_positions.append(
            (text_x, text_y)
        )

    return draw_image


def detect_objects(image):
    output = object_detector(image)

    processed_image = draw_boundaring_boxes(
        image,
        output
    )

    return processed_image
