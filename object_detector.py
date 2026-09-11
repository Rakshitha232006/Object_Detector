from PIL import Image, ImageDraw, ImageFont
from transformers import pipeline


# Load DETR model
object_detector = pipeline(
    "object-detection",
    model="facebook/detr-resnet-50"
)


def draw_boundaring_boxes(image, detections):

    draw_image = image.copy()
    draw = ImageDraw.Draw(draw_image)

    # Medium-sized font
    font_size = max(24, int(draw_image.width / 60))

    try:
        font = ImageFont.truetype("arial.ttf", font_size)
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

        # Put label at the top of the bounding box
        text_x = xmin
        text_y = ymin

        # Keep label inside image
        if text_x + text_width > draw_image.width:
            text_x = draw_image.width - text_width

        if text_y + text_height > draw_image.height:
            text_y = draw_image.height - text_height

        # Avoid overlapping labels
        while any(
            abs(text_y - previous_y) < text_height + 5
            and abs(text_x - previous_x) < text_width
            for previous_x, previous_y in label_positions
        ):
            text_y += text_height + 5

            if text_y + text_height > draw_image.height:
                text_y = ymin
                break

        # Label background
        draw.rectangle(
            [
                text_x,
                text_y,
                text_x + text_width,
                text_y + text_height
            ],
            fill="red"
        )

        # Label text
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

    if image is None:
        return None

    output = object_detector(image)

    processed_image = draw_boundaring_boxes(
        image,
        output
    )

    return processed_image
