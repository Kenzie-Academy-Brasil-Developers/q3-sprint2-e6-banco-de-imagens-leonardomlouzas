# Image Database

Small Flask API for upload/download of image files. 

## Routes
| Endpoint                | Methods | Rule                     |
| :---------------------- | :-----: | :----------------------: |
| download                | GET     | /download/<file_name>    |
| download_dir_as_zip     | GET     | /download-zip            |
| list_files              | GET     | /files                   |
| list_files_by_extension | GET     | /files/<extension_name>  |
| static                  | GET     | /static/<_path:file_name>|
| upload                  | POST    | /upload                  |

**This project was made for the Kenzie Academy Brasil bootcamp.
