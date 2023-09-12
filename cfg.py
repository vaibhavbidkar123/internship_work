import os

#absolute path of the directory
absolute_path=os.path.dirname(os.path.realpath(__file__))

#icon path to use for setting window icon
icon_relative_path="cfg\icon\icon.ico"
icon_path=os.path.normpath(os.path.join(absolute_path, icon_relative_path))

#packages dependencies
user_package={}
user_package_keys=[]
user_package_selected_indices=[]
user_selected_packages=[]