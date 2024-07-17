import cv2
import math
import sys
from ultralytics import YOLO
import tkinter as tk
from PIL import Image, ImageTk
import numpy as np

def main(a):
    if a=="cow":
        c=19
    if a=="horse":
        c=17
    if a=="sheep":
        c=18

    # Initialize the webcam
    cap = cv2.VideoCapture(1)

    model = YOLO("yolov8n.pt")

    # Object classes
    classNames = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
                  'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
                  'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
                  'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
                  'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
                  'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
                  'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard',
                  'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors',
                  'teddy bear', 'hair drier', 'toothbrush']

    # Define the classes to detect
    classes_to_detect = [c]

    class App:
        def __init__(self, window, window_title):
            self.window = window
            self.window.title(window_title)
            self.window.attributes('-fullscreen', True)  # Set fullscreen

            # Open background image and resize to fit the screen
            self.bg_image_path = R"C:\Users\unrul\OneDrive\Desktop\Picture1.png"
            self.bg_image = Image.open(self.bg_image_path)
            self.bg_image = self.bg_image.resize((self.window.winfo_screenwidth(), self.window.winfo_screenheight()), resample=Image.BICUBIC)
            self.bg_image = ImageTk.PhotoImage(self.bg_image)

            # Create a canvas that can fit the video feed size
            self.canvas = tk.Canvas(window, bg="black", highlightthickness=0)
            self.canvas.pack(fill=tk.BOTH, expand=tk.YES)

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

            # Label for cattle detection
            self.pest_label = tk.Label(window, text="CATTLE DETECTION", font=("Arial", 30), bg="black", fg="white")
            self.pest_label.pack(side=tk.TOP, fill=tk.X)

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

            results = model(frame, stream=True)

            # Draw the bounding boxes and class labels on the frame
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    if int(box.cls[0]) in classes_to_detect:
                        x1, y1, x2, y2 = box.xyxy[0]
                        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)

                        confidence = math.ceil((box.conf[0] * 100)) / 100
                        cls = int(box.cls[0])
                        class_name = classNames[cls]

                        org = (x1, y1)
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        fontScale = 1
                        color = (255, 0, 0)
                        thickness = 2
                        cv2.putText(frame, class_name, org, font, fontScale, color, thickness)

            # Resize the frame to the adjusted size
            resized_frame = cv2.resize(frame, (self.width_slider.get(), self.height_slider.get()))

            # Convert the resized frame to RGB format and then to ImageTk format
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)))

            # Add background image
            self.canvas.create_image(0, 0, image=self.bg_image, anchor=tk.NW)

            # Calculate the coordinates to center the video frame
            center_x = (self.window.winfo_screenwidth() - self.width_slider.get()) // 2
            center_y = (self.window.winfo_screenheight() - self.height_slider.get()) // 2

            # Add video feed at the center
            self.canvas.create_image(center_x, center_y, image=self.photo, anchor=tk.NW)

            self.window.after(10, self.update)

        def close(self):
            self.window.destroy()
            cap.release()

    root = tk.Tk()
    app = App(root, "Cattle Detection App")
    root.mainloop()

a=sys.argv[1]
main(a)
