# 🔍 Object Detection using DETR

A simple image object detection web application built using **Python, Streamlit, and Hugging Face Transformers**.

The application allows users to upload one or more images or use their device camera to detect objects. Detected objects are highlighted with bounding boxes and confidence scores.

## 🚀 Live Application

https://objectdetector-bb8fzbam2csvsnam8noqxw.streamlit.app/

The application is deployed using **Streamlit Community Cloud**.

## ✨ Features

- 📁 Upload one or multiple images
- 📷 Capture an image using the device camera
- 🔍 Detect objects automatically
- 📦 Draw bounding boxes around detected objects
- 📊 Display confidence scores
- ⚠️ Inform the user when no recognizable objects are detected
- 🧹 Clear uploaded images and results
- 🌐 Live Streamlit web application

## 🧠 Model Used

This project uses **DETR (DEtection TRansformer)** with a ResNet-50 backbone.

**Model:** `facebook/detr-resnet-50`

The model is loaded using the Hugging Face Transformers pipeline:

```python
pipeline(
    "object-detection",
    model="facebook/detr-resnet-50"
)
🛠️ Technologies Used
Python
Streamlit
Hugging Face Transformers
PyTorch
Torchvision
Pillow
Timm
📂 Project Structure
Object_Detector/
│
├── main.py
├── object_detector.py
├── requirements.txt
└── README.md
⚙️ How It Works
User
 │
 ├── Upload Image
 │
 └── Open Camera
          │
          ▼
      Input Image
          │
          ▼
    DETR Object Detector
          │
          ▼
    Detect Objects
          │
          ▼
   Draw Bounding Boxes
          │
          ▼
   Display Result Image
💻 Run Locally
1. Clone the repository
git clone https://github.com/Rakshitha232006/Object_Detector.git
2. Navigate to the project
cd Object_Detector
3. Create a virtual environment
python -m venv .venv
4. Activate the virtual environment

Windows:

.venv\Scripts\activate
5. Install dependencies
pip install -r requirements.txt
6. Run the application
streamlit run main.py
📸 Using the Application
Upload an Image
Open the application.
Select one or more JPG, JPEG, or PNG images.
Click Submit.
The images are processed using DETR.
Detected objects are displayed with bounding boxes and confidence scores.
Use the Camera
Click Open Camera.
Allow camera access when prompted.
Take a picture.
Click Submit.
The captured image is processed by the object detector.

The camera is not activated when the application initially opens. It is activated only after clicking the Open Camera button.

📊 Detection Results

When an object is detected, the application displays its name and confidence score.

Example:

person 0.97
car 0.91
dog 0.86

Detected objects are highlighted using red bounding boxes.

If no recognizable object is detected, the application displays a message informing the user.

⚠️ Limitations

The model is trained on the COCO dataset, so it can recognize a fixed set of common object categories.

It may not recognize:

Mountains
Lakes
Clouds
Lightning
Certain types of plants
Uncommon objects
Objects that are too small or unclear

Therefore, an image can be successfully processed even when no bounding boxes are produced.

🔮 Future Improvements
Add confidence threshold controls
Support more object detection models
Add object counting
Improve bounding box visualization
Add image download functionality
Add support for video detection
Add real-time camera detection
Improve detection accuracy
Add detection history
👩‍💻 Author

Rakshitha Donthireddy

GitHub:
https://github.com/Rakshitha232006

🌐 Project Links

GitHub Repository:
https://github.com/Rakshitha232006/Object_Detector

Live Application:
https://objectdetector-bb8fzbam2csvsnam8noqxw.streamlit.app/