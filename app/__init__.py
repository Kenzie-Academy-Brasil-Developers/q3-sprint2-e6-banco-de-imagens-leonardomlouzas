from flask import Flask, request
import os
from .kenzie.image import all_images, selected_images

app = Flask(__name__)


def initial_config():

    FILES_DIRECTORY=os.getenv("FILES_DIRECTORY")
    ALLOWED_EXTENSIONS=os.getenv("ALLOWED_EXTENSIONS")

    directories = os.listdir("./")

    if FILES_DIRECTORY not in directories:
        os.mkdir(FILES_DIRECTORY)
        os.chdir(FILES_DIRECTORY)
        os.system(f"mkdir {ALLOWED_EXTENSIONS}")
    else:
        directories = os.listdir(FILES_DIRECTORY)

        if not "jpg" in directories:
            os.mkdir(f"{FILES_DIRECTORY}/jpg")
        
        if not "png" in directories:
            os.mkdir(f"{FILES_DIRECTORY}/png")
        
        if not "gif" in directories:
            os.mkdir(f"{FILES_DIRECTORY}/gif")
        

initial_config()

@app.get("/")
def home():
    return "home"

@app.get("/files")
def files():
    return all_images()

@app.get("/files/<extension>")
def files2(extension):
    return selected_images(extension)

@app.post("/upload")
def upload():
    data = request.get_json()
    return (f"upload: {data}")

@app.get("/download/<file_name>")
def download1(file_name):
    return(f"download1: {file_name}")

@app.get("/download-zip")
def download2():
    file_extension = request.args.get("file_extension")
    compression_ratio = request.args.get("compression_ratio")

    return(f"file_extension: {file_extension}. compression_ratio: {compression_ratio}")
