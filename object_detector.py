from PIL import Image, ImageDraw, ImageFont
from transformers import pipeline


# Load the model
model_path = "facebook/detr-resnet-50"

object_detector = pipeline(
    "object-detection",
    model=model_path
)


def draw_boundaring_boxes(image, detections):
    draw_image = image.copy()
    draw = ImageDraw.Draw(draw_image)

    font = ImageFont.truetype("arial.ttf", 80)

    label_positions = []

    for detection in detections:
        box = detection["box"]

        xmin = box["xmin"]
        ymin = box["ymin"]
        xmax = box["xmax"]
        ymax = box["ymax"]

        draw.rectangle(
            [(xmin, ymin), (xmax, ymax)],
            outline="red",
            width=8
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

        text_x = xmin
        text_y = ymin - text_height

        while any(
            abs(text_y - previous_y) < text_height
            and abs(text_x - previous_x) < text_width
            for previous_x, previous_y in label_positions
        ):
            text_y += text_height + 10

        if text_y < 0:
            text_y = ymin

        draw.rectangle(
            [
                text_x,
                text_y,
                text_x + text_width,
                text_y + text_height
            ],
            fill="red"
        )

        draw.text(
            (text_x, text_y),
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