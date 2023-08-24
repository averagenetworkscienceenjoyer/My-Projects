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

file_path = "output.txt"

with open(file_path, "w") as file:
    response = function_that_reads_the_content_of_an_image(image_path=".\filepathhere.jpg")
    texts = response.text_annotations
    for text in texts:
             file.write(text.description)

    