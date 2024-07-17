import cv2
import math
from ultralytics import YOLO
import tkinter as tk
from PIL import Image, ImageTk
from flask import Flask, Response
import numpy as np

app = Flask(__name__)

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Load the YOLOv5 model
model = YOLO(r"C:\Users\unrul\Downloads\best (7).pt")

# Object classes
classNames = ['Apple Scab Leaf', 'Apple leaf', 'Apple rust leaf', 'Bell_pepper leaf spot', 'Bell_pepper leaf', 'Blueberry leaf', 'Cherry leaf', 'Corn Gray leaf spot', 'Corn leaf blight', 'Corn rust leaf', 'Peach leaf', 'Potato leaf early blight', 'Potato leaf late blight', 'Potato leaf', 'Raspberry leaf', 'Soyabean leaf', 'Squash Powdery mildew leaf', 'Strawberry leaf', 'Tomato Early blight leaf', 'Tomato Septoria leaf spot', 'Tomato leaf bacterial spot', 'Tomato leaf late blight', 'Tomato leaf mosaic virus', 'Tomato leaf yellow virus', 'Tomato leaf', 'Tomato mold leaf', 'Tomato two spotted spider mites leaf', 'grape leaf black rot', 'grape leaf']

class App:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        self.window.attributes('-fullscreen', True)  # Set fullscreen

        # Open background image and resize to fit the screen
        self.bg_image_path = r"C:\Users\unrul\OneDrive\Desktop\Picture1.png"
        self.bg_image = Image.open(self.bg_image_path)
        self.bg_image = self.bg_image.resize((self.window.winfo_screenwidth(), self.window.winfo_screenheight()), resample=Image.BICUBIC)
        self.bg_image = ImageTk.PhotoImage(self.bg_image)

        # Create a canvas that can fit the video feed size
        self.canvas = tk.Canvas(window, bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)

        # Plant Disease Detection label
        self.disease_label = tk.Label(window, text="Plant Disease Detection", font=("Arial", 30), bg="black", fg="white")
        self.disease_label.pack(side=tk.TOP, fill=tk.X, padx=20, pady=10)

        # Slider for width adjustment
        self.width_label = tk.Label(window, text="Video Width:", bg="black", fg="white")
        self.width_label.pack(side=tk.LEFT, padx=20, pady=10)
        self.width_slider = tk.Scale(window, from_=50, to=self.window.winfo_screenwidth(), orient=tk.HORIZONTAL)
        self.width_slider.set(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.width_slider.pack(side=tk.LEFT, padx=20, pady=10)

        # Slider for height adjustment
        self.height_label = tk.Label(window, text="Video Height:", bg="black", fg="white")
        self.height_label.pack(side=tk.LEFT, padx=20, pady=10)
        self.height_slider = tk.Scale(window, from_=50, to=self.window.winfo_screenheight(), orient=tk.HORIZONTAL)
        self.height_slider.set(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.height_slider.pack(side=tk.LEFT, padx=20, pady=10)

        # Button to apply size adjustments
        self.apply_btn = tk.Button(window, text="Apply", command=self.apply_size, bg="blue", fg="white")
        self.apply_btn.pack(side=tk.LEFT, padx=20, pady=10)

        # Close button
        self.btn_close = tk.Button(window, text="Close", command=self.close, bg="red", fg="white")
        self.btn_close.pack(side=tk.BOTTOM, fill=tk.X)

        # After setting up the GUI, call the update method
        self.update()

    def apply_size(self):
        # Apply size adjustments
        new_width = int(self.width_slider.get())
        new_height = int(self.height_slider.get())
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, new_width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, new_height)

    def update(self):
        # Get a frame from the video source
        ret, frame = cap.read()

        # Perform object detection
        results = model(frame)

        # Draw the bounding boxes and class labels on the frame
        for box in results[0].boxes:
            if box.conf[0] > 0.8:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)
                confidence = math.ceil((box.conf[0] * 100)) / 100
                print("Confidence --->", confidence)
                cls = int(box.cls[0])
                print("Class name -->", classNames[cls])
                org = (x1, y1)
                font = cv2.FONT_HERSHEY_SIMPLEX
                fontScale = 1
                color = (255, 0, 0)
                thickness = 2
                cv2.putText(frame, classNames[cls], org, font, fontScale, color, thickness)

        # Convert the frame to RGB format and then to ImageTk format
        self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))

        # Add background image
        self.canvas.create_image(0, 0, image=self.bg_image, anchor=tk.NW)

        # Scale video feed size
        x = (self.window.winfo_screenwidth() - self.width_slider.get()) // 2
        y = (self.window.winfo_screenheight() - self.height_slider.get()) // 2

        # Add scaled video feed
        self.canvas.create_image(x, y, image=self.photo, anchor=tk.NW)

        self.window.after(10, self.update)

    def close(self):
        self.window.destroy()
        cap.release()

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                     mimetype='multipart/x-mixed-replace; boundary=frame')

def main():
    root = tk.Tk()
    app = App(root, "Plant Disease Detection App")
    root.mainloop()

main()
