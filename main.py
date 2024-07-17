import threading
import subprocess
from kivy.core.audio import SoundLoader

import sys
import pyttsx3
from gtts import gTTS
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

from kivy.uix.screenmanager import ScreenManager, Screen
Window.size=(1000,600)

class HomeScreen(Screen):
    sound = SoundLoader.load('voice.mp3')
    if sound:
        sound.play()

    def start_ml_program(self,filename):

        self.ml_process = subprocess.Popen(["python", filename])  # Replace with your ML program command
        self.ml_thread = threading.Thread(target=self.ml_process.communicate)
        self.ml_thread.start()

    def stop_ml_program(self):
        pass

    def toggle_weed(self):
        if not hasattr(self, 'ml_process'):  # If ML program is not running
            self.start_ml_program("D:\SMART_BENGAL\crop_weed.py")
        else:  # If ML program is running
            self.stop_ml_program()

    def toggle_pest(self):
        if not hasattr(self, 'ml_process'):  # If ML program is not running
            self.start_ml_program(r"D:\SMART_BENGAL\pest.py")
        else:  # If ML program is running
            self.stop_ml_program()

class FirstScreen(Screen):
    pass

class Manager(ScreenManager):
    pass

class BoxLayoutEg(BoxLayout):
    def start_ml_program(self,filename,animal):
            self.ml_process = subprocess.Popen(["python", filename,animal])  # Replace with your ML program command
            self.ml_thread = threading.Thread(target=self.ml_process.communicate)
            self.ml_thread.start()

    def stop_ml_program(self):
        pass
    def cow(self,widget):
        if not hasattr(self, 'ml_process'):  # If ML program is not running
            self.start_ml_program(r"D:\SMART_BENGAL\cattle.py","cow")
        else:  # If ML program is running
            self.stop_ml_program()

    def goat(self,widget):
        if not hasattr(self, 'ml_process'):  # If ML program is not running
            self.start_ml_program(r"D:\SMART_BENGAL\cattle.py", "sheep")
        else:  # If ML program is running
            self.stop_ml_program()

    def horse(self,widget):
        if not hasattr(self, 'ml_process'):  # If ML program is not running
            self.start_ml_program(r"D:\SMART_BENGAL\cattle.py", "horse")
        else:  # If ML program is running
            self.stop_ml_program()

class GridLayoutEg(GridLayout):
    def start_ml_program(self,filename):
            self.ml_process = subprocess.Popen(["python", filename])  # Replace with your ML program command
            self.ml_thread = threading.Thread(target=self.ml_process.communicate)
            self.ml_thread.start()

    def stop_ml_program(self):
        pass

    def croprecommendation(self):
        if not hasattr(self, 'ml_process'):
            sound = SoundLoader.load(r'D:\SMART_BENGAL\Farm Monitoring\1 (2).mp3')
            if sound:
                sound.play()
            # If ML program is not running
            self.start_ml_program(r"D:\SMART_BENGAL\Farm Monitoring\croprecommendation.py")
        else:  # If ML program is running
            self.stop_ml_program()

    def toggle_disease(self):
        if not hasattr(self, 'ml_process'):  # If ML program is not running
            self.start_ml_program(r"D:\SMART_BENGAL\plant-disease.py")
        else:  # If ML program is running
            self.stop_ml_program()

class FarmMonitoringApp(App):

    def build(self):
        self.icon=r"farm.png"


    def stop(self):
        print("Stop")

FarmMonitoringApp().run()
