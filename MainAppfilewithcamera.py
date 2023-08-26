import os
import subprocess
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen, ScreenManager
#part of the preamble that the camera needs 
from kivy.logger import Logger
import logging
Logger.setLevel(logging.TRACE)
from kivy.uix.camera import Camera
from kivy.uix.togglebutton import ToggleButton
import time 
#creating the camera layout.

class CameraApp(App):
    #this is the method that calls on the AnalyseButtonFile file when we click on the analyse button.
    def run_analyse_file(self, instance):
        try:
            subprocess.Popen(["python", "AnalyseButtonFile.py"])
        except Exception as e:
            print("Error:", e)
    #method that defines the camera call

    
    def build(self):
        self.sm = ScreenManager()

        # Create Main Screen: put this as a kv file. not been able to do this yet!
        main_screen = Screen(name="main")
        main_layout = BoxLayout(orientation='vertical')
        take_notes_button = Button(text="Take Notes", on_press=self.goto_action_screen)
        view_notes_button = Button(text= "View Notes", on_press=self.open_notes_folder)#some new code here
        main_layout.add_widget(take_notes_button)
        main_layout.add_widget(view_notes_button)
        main_screen.add_widget(main_layout)
        self.sm.add_widget(main_screen)
#camera code is here 
        self.camera = Camera(
            resolution=(640, 480),
            play=False
        )

        self.play_button = ToggleButton(
            text='Play',
            size_hint_y=None,
            height='48dp'
        )
        self.play_button.bind(on_press=self.toggle_camera_play)

        self.capture_button = Button(
            text='Capture',
            size_hint_y=None,
            height='48dp'
        )
        self.capture_button.bind(on_press=self.capture)

        # Create Action Screen
        action_screen = Screen(name="action")
        action_layout = BoxLayout(orientation='vertical')
        action_layout.add_widget(Label(text="Choose an action:"))
        
        action_layout.add_widget(self.camera)
        action_layout.add_widget(self.play_button)
        action_layout.add_widget(self.capture_button)

        take_picture_button = Button(text="take a picture")
        analyse_button = Button(text="Analyse")
        #implementing the back button
        back_button = Button(text="Back", on_press=self.goto_main_screen)
        #this runs the AnalyseButtonFile file, using the method we defined above.
        analyse_button.bind(on_press=self.run_analyse_file)
        crop_button = Button(text="Crop", on_press=self.crop)
        
        action_layout.add_widget(take_picture_button)
        action_layout.add_widget(analyse_button)
        action_layout.add_widget(crop_button)
        action_layout.add_widget(back_button)
        
        action_screen.add_widget(action_layout)
        self.sm.add_widget(action_screen)

        # Create Picture Screen
        self.picture_screen = Screen(name="picture")
        self.picture_layout = BoxLayout(orientation='vertical')
        self.picture = Image(source="", size_hint=(1, 1))
        self.analyse_button = Button(text="Analyse this picture?", on_press=self.analyse_picture)
        self.choose_another_button = Button(text="No, choose another!", on_press=self.goto_action_screen)
        self.picture_layout.add_widget(self.picture)
        self.picture_layout.add_widget(self.analyse_button)
        self.picture_layout.add_widget(self.choose_another_button)
        self.picture_screen.add_widget(self.picture_layout)
        self.sm.add_widget(self.picture_screen)

        return self.sm
#this is the open notes folder method we called earlier! it works!
    def toggle_camera_play(self, instance):
        self.camera.play = not self.camera.play

    def capture(self, instance):
        timestr = time.strftime("%Y%m%d_%H%M%S")
        self.camera.export_to_png("IMG_{}.png".format(timestr))
        print("Captured")


    def open_notes_folder(self,instance):
        script_path = os.path.abspath(__file__)
        
        # Get the parent directory (containing folder) of the script file
        app_directory = os.path.dirname(script_path)
        
        # Create the path to the "notes" folder
        notes_folder_path = os.path.join(app_directory, 'notes')
        
        # Open the "notes" folder using the default file explorer
        os.system(f'explorer {notes_folder_path}') 

    def goto_main_screen(self,instance):
        self.sm.current = "main"

    def goto_action_screen(self, instance):
        self.sm.current = "action"

    def take_picture(self, instance):
        print("Taking Picture")

    def crop(self, instance):
        print("Cropping")

    def analyse_picture(self, instance):
        self.sm.current = "picture"
        # Set the picture source to the selected image path
        self.picture.source = "path_to_selected_image.jpg"

if __name__ == '__main__':
    app = CameraApp()
    app.run()
