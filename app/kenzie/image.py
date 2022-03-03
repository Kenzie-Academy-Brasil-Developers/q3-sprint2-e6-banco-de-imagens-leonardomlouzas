from flask import jsonify, send_from_directory
import os
import shutil
from zipfile import ZipFile


ALLOWED_EXTENSIONS = os.getenv("ALLOWED_EXTENSIONS")
FILES_DIRECTORY = os.getenv("FILES_DIRECTORY")
ABS_PATH = os.path.abspath(FILES_DIRECTORY)
TMP_PATH = os.path.abspath("/tmp")

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
    
    return {"Msg":"No files"}, 404

def selected_images(type):
    if type in ALLOWED_EXTENSIONS:
        
        result = []

        list_items = os.walk(f"./images/{type}")

        for item in list_items:
            for file in item[2]:
                result.append({"Name": file})

        if len(result) > 0:

            return jsonify(result), 200
        else:
            return {"Msg": f"The folder '{type}' is empty."}
    
    return {"Msg":f"There is no '{type}' folder."}, 404



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
    else:
        return {"Msg":f"There is no '{extension}' folder."}, 404


    return {"Msg": f"There is no '{'.'.join(name)}' in '{extension}' folder"}, 404


def upload_image(image):
    file = image
    *name, extension = image.filename.split(".")

    if extension in ALLOWED_EXTENSIONS:

        *_, files = next(os.walk(f'{ABS_PATH}/{extension}'))

        if not file.filename in files:
            file.save(os.path.join(f'{ABS_PATH}/{extension}', file.filename))

            return {"Msg": f"Success uploading '{'.'.join(name)}' in '{extension}' folder."}, 201
        else:
            return {"Msg": f"File '{'.'.join(name)}' already exist in '{extension}' folder."}, 409

    return {"Msg": f"Extension '{extension}' not supported."}, 415

def download_zip(extension, compression = 6):

    compression = -6 if not compression else compression

    if not extension:
        return {"Msg": "Extension type must be declared."}

    if not extension in ALLOWED_EXTENSIONS:
        return {"Msg": f"Extension '{extension}' not supported."}

    path, directory, files = next(os.walk(f'{FILES_DIRECTORY}/{extension}'))
    
    final_name = f'images {extension}.zip'

    with ZipFile(final_name, mode='w', compresslevel= abs(int(compression))) as zip:
        
        for file in files:
            zip.write(os.path.join(path, file))
    
        if os.path.exists(f'/tmp/{final_name}'):
            os.remove(f'/tmp/{final_name}')

        shutil.move(f'./{final_name}', "/tmp")

        completed = True

    if completed:
        return send_from_directory(
                directory="/tmp",
                path= final_name,
                as_attachment=True
            )
    return {"Msg": "An error ocurred."}