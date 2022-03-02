import json
from flask import jsonify, send_from_directory
import os

ALLOWED_EXTENSIONS = os.getenv("ALLOWED_EXTENSIONS")
FILES_DIRECTORY = os.getenv("FILES_DIRECTORY")
ABS_PATH = os.path.abspath(FILES_DIRECTORY)

def all_images():
    result = []

    tmp_list = []

    list_items = os.walk("./images")

    for item in list_items:
        for file in item[2]:
            tmp_list.append({"Name": file})
        
        if len(tmp_list) > 0:
            result.append({f'{item[0]}': tmp_list})
        tmp_list = []

    if len(result) > 0:
        return jsonify(result), 200
    
    return {"msg":"No files"}, 404

def selected_images(type):
    if type in ALLOWED_EXTENSIONS:
        
        result = []

        list_items = os.walk(f"./images/{type}")

        for item in list_items:
            for file in item[2]:
                result.append({"Name": file})

        if len(result) > 0:

            return jsonify(result), 200
    
    return {"msg":f"No '{type}' files"}, 404



def download_image(image):
    *name, extension = image.split(".")

    if extension in ALLOWED_EXTENSIONS:
        
        path, dire, files = next(os.walk(f'{FILES_DIRECTORY}/{extension}'))
        
        if image in files:
            return send_from_directory(
                directory=f'../images/{extension}',
                path= image,
                as_attachment=True
            )

    return {"msg": f"No '{'.'.join(name)}' in '{extension}' folder"}, 404


def upload_image(image):
    file = image
    *name, extension = image.filename.split(".")

    if extension in ALLOWED_EXTENSIONS:

        *_, files = next(os.walk(f'{ABS_PATH}/{extension}'))

        if not file.filename in files:
            file.save(os.path.join(f'{ABS_PATH}/{extension}', file.filename))

            return {"Msg": f"success uploading '{'.'.join(name)}' in '{extension}' folder."}
        else:
            return {"Msg": f"file '{'.'.join(name)}' already exist in '{extension}' folder."}

    return {"Msg": f"Extension '{extension}' not allowed."}