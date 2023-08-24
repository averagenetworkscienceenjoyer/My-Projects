import os 
from google.cloud import vision 

def function_that_reads_the_content_of_an_image(image_path):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ".\credentials.json"
    client = vision.ImageAnnotatorClient()
    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)
    texts = response.text_annotations 

    return response 
#this is the improvement:we now can save as many files as we like!
base_filename = "output"
file_number = 1
output_folder = "Notes"  # Name of the folder where you want to save the output files
os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist

while True:
    file_path = os.path.join(output_folder, f"{base_filename}({file_number}).txt")
    if not os.path.exists(file_path):
        break
    file_number += 1

#improvement ends here 
with open(file_path, "w") as file:
    response = function_that_reads_the_content_of_an_image(image_path=".\pythonproject1")
    texts = response.text_annotations
    for text in texts:
             file.write(text.description)