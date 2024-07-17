import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from PIL import Image, ImageTk

# Load the dataset
data_path = "D:\SMART_BENGAL\Crop_recommendation.csv"
data = pd.read_csv(data_path)

# Assuming the dataset contains relevant columns

X = data[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
y = data['label']

# Create a Random Forest Classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Set feature names for the RandomForestClassifier
feature_names = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
model.feature_names = feature_names


# Crop recommendation function
def recommend_crop(N, P, K, temperature, humidity, ph, rainfall):
    input_data = pd.DataFrame([[N, P, K, temperature, humidity, ph, rainfall]], columns=feature_names)
    predicted_crop = model.predict(input_data)
    return predicted_crop[0]


# Function to handle button click
def on_submit():
    global entries  # Declare entries as global

    N = float(entries["Nitrogen Value:"].get())
    P = float(entries["Phosphorus Value:"].get())
    K = float(entries["Potassium Value:"].get())
    temperature = float(entries["Temperature (°C):"].get())
    humidity = float(entries["Humidity (%):"].get())
    ph = float(entries["pH Value:"].get())
    rainfall = float(entries["Rainfall (mm):"].get())

    inputs = [N, P, K, temperature, humidity, ph, rainfall]

    # Check if any input is None (indicating an error)
    if None in inputs:
        return

    recommended_crop = recommend_crop(N, P, K, temperature, humidity, ph, rainfall)
    output_label.config(text=f"Recommended Crop: {recommended_crop}")


# Create GUI window
root = ThemedTk(theme="arc")
root.title("Crop Recommendation System")

# Set window size and position
window_width = root.winfo_screenwidth()
window_height = root.winfo_screenheight()
root.geometry(f"{window_width}x{window_height}+0+0")

# Load the background image
background_image = Image.open(r"C:\Users\unrul\OneDrive\Desktop\Picture1.png")
background_image = background_image.resize((window_width, window_height))

background_photo = ImageTk.PhotoImage(background_image)

# Set background image
background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Set window to transparent
root.attributes('-alpha', 0.95)

# Create labels and input fields
labels = ["Nitrogen Value:", "Phosphorus Value:", "Potassium Value:", "Temperature (°C):", "Humidity (%):", "pH Value:",
          "Rainfall (mm):"]
entries = {}

bold_font = ('Arial', 30, 'bold')  # Bold font
color = '#000000'  # Green color

for i, label_text in enumerate(labels):
    label = ttk.Label(root, text=label_text, font=bold_font, foreground=color, background='#FFFF00')
    label.grid(row=i, column=0, padx=20, pady=10, sticky='w')
    entry = ttk.Entry(root, font=bold_font)
    entry.grid(row=i, column=1, padx=20, pady=10, sticky='ew')
    entries[label_text] = entry

# Create submit button
submit_btn = ttk.Button(root, text="Recommend Crop", command=on_submit, style='Bold.TButton')
submit_btn.grid(row=len(labels), column=0, columnspan=2, padx=20, pady=20, sticky='ew')

# Create label to display output
output_label = ttk.Label(root, text="", anchor='center', font=bold_font, foreground=color,
                         background='#FFFF00')
output_label.grid(row=len(labels) + 1, column=0, columnspan=2, padx=20, pady=20, sticky='ew')

# Configure grid weights to make the widgets expand
for i in range(len(labels) + 2):
    root.grid_rowconfigure(i, weight=1)

for i in range(2):
    root.grid_columnconfigure(i, weight=1)

# Configure button style
style = ttk.Style()
style.configure('Bold.TButton', font=bold_font, foreground=color, background='#FFFF00')

root.mainloop()
