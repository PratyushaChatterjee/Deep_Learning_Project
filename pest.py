import cv2
import math
from ultralytics import YOLO
import tkinter as tk
from PIL import Image, ImageTk

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Load the YOLOv5 model
model = YOLO(r"C:\Users\unrul\Downloads\best (9).pt")

class App:
    def __init__(self, window, window_title, video_source, bg_image_path):
        self.window = window
        self.window.title(window_title)
        self.window.attributes('-fullscreen', True)  # Set fullscreen

        # Open background image and resize to fit the screen
        self.bg_image = Image.open(bg_image_path)
        self.bg_image = self.bg_image.resize((self.window.winfo_screenwidth(), self.window.winfo_screenheight()), resample=Image.BICUBIC)
        self.bg_image = ImageTk.PhotoImage(self.bg_image)

        # Open video source
        self.cap = cv2.VideoCapture(video_source)

        # Create a canvas that can fit the above video source size
        self.canvas = tk.Canvas(window, bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)

        # Slider for width adjustment
        self.width_label = tk.Label(window, text="Video Width:", bg="black", fg="white")
        self.width_label.pack(side=tk.LEFT, padx=20, pady=10)
        self.width_slider = tk.Scale(window, from_=50, to=self.window.winfo_screenwidth(), orient=tk.HORIZONTAL)
        self.width_slider.set(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.width_slider.pack(side=tk.LEFT, padx=20, pady=10)

        # Slider for height adjustment
        self.height_label = tk.Label(window, text="Video Height:", bg="black", fg="white")
        self.height_label.pack(side=tk.LEFT, padx=20, pady=10)
        self.height_slider = tk.Scale(window, from_=50, to=self.window.winfo_screenheight(), orient=tk.HORIZONTAL)
        self.height_slider.set(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.height_slider.pack(side=tk.LEFT, padx=20, pady=10)

        # Button to apply size adjustments
        self.apply_btn = tk.Button(window, text="Apply", command=self.apply_size, bg="blue", fg="white")
        self.apply_btn.pack(side=tk.LEFT, padx=20, pady=10)

        # Button to close the program
        self.btn_close = tk.Button(window, text="Close", command=self.close, bg="red", fg="white")
        self.btn_close.pack(side=tk.BOTTOM, fill=tk.X)

        # Pest detection label
        self.pest_label = tk.Label(window, text="Pest Detection", font=("Arial", 30), bg="black", fg="white")
        self.pest_label.pack(side=tk.TOP, fill=tk.X)

        # After setting up the GUI, call the update method
        self.update()

    def apply_size(self):
        # Apply size adjustments
        new_width = int(self.width_slider.get())
        new_height = int(self.height_slider.get())
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, new_width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, new_height)

    def update(self):
        # Get a frame from the video source
        ret, frame = self.cap.read()

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
                org = (x1, y1)
                font = cv2.FONT_HERSHEY_SIMPLEX
                fontScale = 1
                color = (255, 0, 0)
                thickness = 2
                cv2.putText(frame, "pest", org, font, fontScale, color, thickness)

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
        self.cap.release()

# Create a window and pass it to the App class
root = tk.Tk()
app = App(root, "Pest Detection App", 1, r"C:\Users\unrul\OneDrive\Desktop\Picture1.png")
root.mainloop()
