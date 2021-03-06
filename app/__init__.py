from flask import Flask, request
import os
from .kenzie.image import all_images, selected_images, download_image, upload_image, download_zip

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024 

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

@app.get("/files")
def files():
    return all_images()

@app.get("/files/<extension>")
def files_extension(extension):
    return selected_images(extension)

@app.post("/upload")
def upload():
    file = request.files["file"]
    return upload_image(file)

@app.get("/download/<file_name>")
def download_file(file_name):
    return(download_image(file_name))

@app.get("/download-zip")
def download_zip_files():
    file_extension = request.args.get("file_extension")
    compression_ratio = request.args.get("compression_ratio")

    return download_zip(file_extension, compression_ratio)
