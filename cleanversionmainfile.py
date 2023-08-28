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

    def build(self):
        self.sm = ScreenManager()

        # Create Main Screen: (put this as a kv file. not been able to do this yet!)
        main_screen = Screen(name="main")
        main_layout = BoxLayout(orientation='vertical')
        take_notes_button = Button(text="Take Notes", on_press=self.goto_intermediary_screen)
        view_notes_button = Button(text= "View Notes", on_press=self.open_notes_folder)#some new code here
        main_layout.add_widget(take_notes_button)
        main_layout.add_widget(view_notes_button)
        main_screen.add_widget(main_layout)
        self.sm.add_widget(main_screen)
#camera code is here 
        self.camera = Camera(
            resolution=(640, 480),
            play=True #we put this as false if we want a play button to toggle it on and off
        )

        self.capture_button = Button(
            text='Capture',
            size_hint_y=None,
            height='48dp'
        )
        self.capture_button.bind(on_press=self.capture)
#camera code ends here 

        

# Create the intermediary screen
        intermediary_screen = Screen(name="intermediary")
        intermediary_layout = BoxLayout(orientation='vertical')
        take_picture_button = Button(text="Take a picture and Analyse it", on_press=self.goto_action_screen)
        analyse_image_button = Button(text="Analyse a saved Image")
        analyse_image_button.bind(on_press=self.run_analyse_file)

# Add both buttons to the intermediary layout. Note that you have to add the widgets in the same 
#order that you defined them in, otherwise only one widget will get shown.
        intermediary_layout.add_widget(take_picture_button)
        intermediary_layout.add_widget(analyse_image_button)

# Add the intermediary layout to the intermediary screen
        intermediary_screen.add_widget(intermediary_layout)

# Add the intermediary screen to the screen manager
        self.sm.add_widget(intermediary_screen)


        # Create Action Screen
        action_screen = Screen(name="action")
        action_layout = BoxLayout(orientation='vertical')
        action_layout.add_widget(Label(text="Choose an action:"))
        
        #this is the widget that shows the camera ie what the camera is seeing 
        action_layout.add_widget(self.camera)
        #action_layout.add_widget(self.play_button)
        #note that the capture button is defined in the camera code above this 
        action_layout.add_widget(self.capture_button)

        #take_picture_button = Button(text="take a picture")
        analyse_button = Button(text="Analyse")
        #implementing the back button
        back_button = Button(text="Back", on_press=self.goto_main_screen)
        #this runs the AnalyseButtonFile file, using the method we defined above.
        analyse_button.bind(on_press=self.run_analyse_file)
        #crop_button = Button(text="Crop", on_press=self.crop)
        
        #action_layout.add_widget(take_picture_button)
        action_layout.add_widget(analyse_button)
        #action_layout.add_widget(crop_button)
        action_layout.add_widget(back_button)
        
        action_screen.add_widget(action_layout)
        self.sm.add_widget(action_screen)

        # Create Picture Screen. this is the screen we are sent to when we take a picture
        #with the camera.
        picture_screen = Screen(name="picture")
        picture_layout = BoxLayout(orientation='vertical')
        
        self.picture = Image(source="", size_hint=(1, 1))
        self.analyse_picture_button = Button(text="Analyse this picture?", on_press=self.analyse_picture)
        self.choose_another_button = Button(text="No, choose another!", on_press=self.goto_action_screen)
       
        picture_layout.add_widget(self.picture)
        picture_layout.add_widget(self.analyse_picture_button)
        picture_layout.add_widget(self.choose_another_button)
        
        picture_screen.add_widget(picture_layout)

        self.sm.add_widget(picture_screen)

        self.picture_screen = picture_screen

        return self.sm
#this is the open notes folder method we called earlier! it works!
      #this is the method that calls on the AnalyseButtonFile file when we click on the analyse button.
    def run_analyse_file(self, instance):
        try:
            subprocess.Popen(["python", "AnalyseButtonFile.py"])
        except Exception as e:
            print("Error:", e)
    #method that defines the camera call

    def toggle_camera_play(self, instance):
        self.camera.play = not self.camera.play
#the original version of this method is in the other main app file
    def capture(self, instance):
        timestr = time.strftime("%Y%m%d_%H%M%S")
        image_path = "IMG_{}.png".format(timestr)
        self.camera.export_to_png(image_path)
        print("Captured")
        self.picture.source = image_path
    # Navigate to the Picture Display Screen
        self.sm.current = "picture"

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

    def goto_intermediary_screen(self,instance):
        self.sm.current = "intermediary"

    def analyse_picture(self, instance):
        self.sm.current = "picture"
        # Set the picture source to the selected image path
        self.picture.source = "path_to_selected_image.jpg"

if __name__ == '__main__':
    app = CameraApp()
    app.run()