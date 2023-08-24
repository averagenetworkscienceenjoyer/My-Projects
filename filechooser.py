
from tkinter import *
from PIL import ImageTk, Image 
from tkinter import filedialog
import os 
import subprocess

root = Tk()
root.title("File Dialog")
def open():
    global my_image 
    root.filename = filedialog.askopenfilename(initialdir="/",title = "select file", filetypes = (("png files",".png"),("all files","*.*")))
    my_label = Label(root, text = root.filename).pack()
    my_image = ImageTk.PhotoImage(Image.open(root.filename))
    my_image_label = Label(image = my_image).pack()
my_btn = Button(root, text="analyse image", command=open).pack()
#function to save the image in the ocr directory so it can be analysed 
def save_image():
    # Specify the target directory where you want to save the image
    target_directory = ".\pythonproject1"

    if my_image:
        image_filename = root.filename.split("/")[-1]
        target_path = os.path.join(target_directory, image_filename)

        # Open the image using PIL and save it with the correct format
        img = Image.open(root.filename)
        img.save(target_directory, format=image_filename.split(".")[-1])
        print("Image saved:", target_directory)
        #this bit runs the ocr code once weve saved the file
        subprocess.run(["python", "bestocrfileversion.py"])
    else:
        print("No image to save.")
save_button = Button(root, text="Save Image", command=save_image)
save_button.pack()

root.mainloop()
#this works but now we need to make it so its integrated with the rest of the ui and that we have another button 
#so you can click on it and it saves the image to the same directory as the ocr code and then runs it with that
#path! making progress tho!

#running this file opens up the file chooser, so we want to make it so clicking on "analyse a saved picture"
#causes this code to run 