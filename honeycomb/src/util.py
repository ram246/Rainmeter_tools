import os
import sys
import requests

def get_filename_ext(filename):
    file_list = filename.split('.')
    return file_list[len(file_list ) - 1]

def get_filename_from_path(path, delimeter = '\\'):
    path_list = path.split(delimeter)
    return path_list[len(path_list) - 1]

def edit_template(template, source, mapping):
    # If the source is a directory make a file with the same name as the template
    if os.path.isdir(source):
        source = source + get_filename_from_path(template)
    template_file = open(template)
    template_text = template_file.read()
    template_file.close()
    
    for key in mapping:
        template_text = template_text.replace(key, mapping[key])
    
    source_file = open(source, 'w')
    source_file.write(template_text)
    source_file.close()

def get_resources_path():
    curr_file = os.path.abspath(sys.argv[0])
    curr_file = curr_file[:curr_file.rfind("\\")]
    return  curr_file[:curr_file.rfind("\\")] + "\\resources"

def download_image_to(target, source):
    req = requests.get(target)

    source_file = open(source, 'wb')
    source_file.write(req.content)
    source_file.close()


    

#edit_template("create_homeycomb_app.py", "sd", "s")