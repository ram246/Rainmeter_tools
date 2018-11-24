import os
import sys
import win32com.client

import util

rainmeter_home = str(os.environ['RAINMETER_HOME'])
desktop = "C:\\Users\\aramg\\Desktop"
resources_folder = util.get_resources_path()


def print_usage():
    print ("Usage: python " + str(sys.argv[0]) + " <app_name> <desktop_shortcut> <icon_url> <background_url>")
    print ("For parameters with special charecters please use \"")

def make_req_dirs(app_name):
    # Create directory for icon .ini file
    new_icon_dir = rainmeter_home + "\\Skins\\Honeycomb\\" + app_name
    if not os.path.isdir(new_icon_dir):
        os.mkdir(new_icon_dir)

    # Create directory for background .ini file
    new_background_dir = rainmeter_home + "\\Skins\\Wallpaper\\" + app_name
    if not os.path.isdir(new_background_dir):
        os.mkdir(new_background_dir)
    
    return (new_icon_dir, new_background_dir)

def get_app_path(shortcut_name):
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(desktop + "\\" + shortcut_name + ".lnk")
    return shortcut.Targetpath

def download_images(app_name, icon, background):
    print ("ICON: " + icon)
    # Download the icon image to the right place
    icon_image_type = util.get_filename_ext(icon)
    icon_name = app_name + "_icon." + icon_image_type
    icon_file_path = rainmeter_home + "\\Skins\\Honeycomb\\@Resources\\Images\\" + icon_name
    print ("PATH: " + icon_file_path)
    util.download_image_to(icon, icon_file_path)

    # Download the background image to the right place
    bgd_image_type = util.get_filename_ext(icon)
    bgd_name =  app_name + "_background." + bgd_image_type
    bgd_file_path = rainmeter_home + "\\Skins\\Wallpaper\\" + app_name + "\\" + bgd_name

    util.download_image_to(background, bgd_file_path)

    return (icon_name, bgd_name)

def create_honeycomb_shortcut(app_name, desktop_shortcut, icon_url, background_url):
    # Make th enew directories for this app
    print ("Making app folders...")
    (icon_dir, background_dir) = make_req_dirs(app_name)

    # Get the path of the executable from the shortcut link
    executable_app_path = get_app_path(desktop_shortcut)

    # Download the images to the correct folder
    print ("Downloading images...")
    (icon_filename, background_filename) =  download_images(app_name, icon_url, background_url)

    # Create mapping dictionaries
    icon_ini_dict = {"<app_name>": app_name, "<app_icon>": icon_filename, 
        "<path_to_app>": executable_app_path, }

    background_ini_dict = {"<image_name>": background_filename}

    print ("Creating ini files...")
    # Generate icon.ini file
    util.edit_template(resources_folder + "\\icon_template.ini", icon_dir + "\\" + app_name + ".ini", icon_ini_dict)

    # Generate background.ini file
    util.edit_template(resources_folder + "\\background_template.ini", background_dir + "\\background.ini", background_ini_dict)

    print ("Done!")

if __name__ == '__main__':
    if (len(sys.argv) != 5):
        sys.exit (print_usage())

    if (sys.argv[1] == "--help"):
        print_usage()
        exit()

    # Define all the input parameters
    create_honeycomb_shortcut(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]), str(sys.argv[4]))
