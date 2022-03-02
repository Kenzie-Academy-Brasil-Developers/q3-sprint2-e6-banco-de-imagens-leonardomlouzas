from flask import jsonify
import os

ALLOWED_EXTENSIONS = os.getenv("ALLOWED_EXTENSIONS")

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


#TODO: CREATE UPLOAD/DOWNLOAD FUNCTIONS