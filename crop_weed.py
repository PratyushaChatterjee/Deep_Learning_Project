import cv2
import math
from ultralytics import YOLO
from flask import Flask, Response
import webbrowser
import numpy as np

app = Flask(__name__)

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Load the YOLOv5 model
model = YOLO(r"C:\Users\unrul\Downloads\best (13).pt")

# Object classes
classNames = ['crop', 'weed']

def gen_frames():
    while True:
        # Read the frame from the webcam
        ret, frame = cap.read()

        # Perform object detection
        results = model(frame)

        # Draw the bounding boxes and class labels on the frame
        for box in results[0].boxes:
            # Confidence check
            if box.conf[0] > 0.8:  # Adjust threshold here
                # Bounding box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)

                # Confidence
                confidence = math.ceil((box.conf[0]*100))/100
                print("Confidence --->",confidence)

                # Class label and its index
                cls = int(box.cls[0])
                print("Class name -->", classNames[cls])

                # Text display on frame
                org = (x1, y1)
                font = cv2.FONT_HERSHEY_SIMPLEX
                fontScale = 1
                color = (255, 0, 0)
                thickness = 2
                cv2.putText(frame, classNames[cls], org, font, fontScale, color, thickness)

        # Convert the frame to JPEG
        ret, jpeg = cv2.imencode('.jpg', frame)

        # Yield the JPEG data to the webpage
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

@app.route('/video_feed2')
def video_feed():
    return Response(gen_frames(),
                     mimetype='multipart/x-mixed-replace; boundary=frame')

def main():
    html_file = r"D:\SMART_BENGAL\crop and weed.HTML"
    webbrowser.open(html_file)
    app.run(host='0.0.0.0', debug=True, threaded=True)
main()