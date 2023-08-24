import os
import subprocess
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen, ScreenManager

class CameraApp(App):
    def run_file(self, instance):
        try:
            subprocess.Popen(["python", "filechooser.py"])
        except Exception as e:
            print("Error:", e)

    def build(self):
        self.sm = ScreenManager()

        # Create Main Screen: put this as a kv file 
        main_screen = Screen(name="main")
        main_layout = BoxLayout(orientation='vertical')
        take_notes_button = Button(text="Take Notes", on_press=self.goto_action_screen)
        view_notes_button = Button(text= "View Notes")
        main_layout.add_widget(take_notes_button)
        main_layout.add_widget(view_notes_button)
        main_screen.add_widget(main_layout)
        self.sm.add_widget(main_screen)

        # Create Action Screen
        action_screen = Screen(name="action")
        action_layout = BoxLayout(orientation='vertical')
        action_layout.add_widget(Label(text="Choose an action:"))
        
        take_picture_button = Button(text="Take Picture", on_press=self.take_picture)
        analyse_button = Button(text="Analyse")
        #this runs the filechooser file.
        analyse_button.bind(on_press=self.run_file)
        crop_button = Button(text="Crop", on_press=self.crop)
        
        action_layout.add_widget(take_picture_button)
        action_layout.add_widget(analyse_button)
        action_layout.add_widget(crop_button)
        
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
