from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import ttk
import zipfile
import custom_errors as ce
from time import time
import os
import yaml
import webbrowser

# default variables

version = "pr1.0.0"
debug_mode = True # change this when releasing!
supported_version = "v0.3.6f5"
start_time = round(time(), 3)

program_config = f"{os.path.dirname(os.path.realpath(__file__))}/config.yaml"

default_config = {
    "version": 1,
    "debug_mode": False
}

def debug_message(message: str) -> None: # custom debug messages cause i can.
    if debug_mode:
        print(f"[{round(time()-start_time, 3)}] {message}")

# loading config info

debug_message(f"Finding config file at {program_config}...")

if os.path.isfile(program_config):
    debug_message("Found config file! Loading it...")
    try:
        config_file_data = yaml.load(open(program_config, "r"), Loader=yaml.FullLoader)
        change_flag = False
        for setting in default_config:
            if setting in config_file_data:
                if not isinstance(config_file_data[setting], type(default_config[setting])):
                    config_file_data[setting] = default_config[setting]
                    change_flag = True

            else:
                debug_message(f"{setting} not found in existing config! Adding it from the default config...")
                config_file_data[setting] = default_config[setting]
                change_flag = True

        if default_config["version"] != config_file_data["version"]:
            debug_message(f"Existing config file seems to be from a different version (currently: {config_file_data['version']}, but it is supposed to be: {default_config['version']})...")
            config_file_data["version"] = default_config["version"]
            change_flag = True

        if change_flag:
            debug_message("Existing config file seems to have some info that had to be changed, updated or added! Saving config...")
            with open(program_config, "w") as f:
                yaml.dump(config_file_data, f)
                f.close()
                debug_message("Config updated!")

        debug_message("Printing current config info...")
        debug_message(f"debug_mode = {config_file_data['debug_mode']}")
        debug_mode = config_file_data["debug_mode"]
        if not debug_mode:
            print(f"Stopped priting debug messages! Since debug mode is turned off in the config. To change this, go to: {program_config}")

            # rest of the config variables go here!
    
    except Exception as e:
        print(e)
        debug_message("Some error occured while loading config file! Re-writing the config...")
        with open(program_config, "w") as f:
            yaml.dump(default_config, f)
            f.close()
            debug_message("Config updated! Using default config for this session.")

        debug_message("Printing current config info...")
        debug_message(f"debug_mode = {config_file_data['debug_mode']}")
        debug_mode = config_file_data["debug_mode"]
        if not debug_mode:
            print(f"Stopped priting debug messages! Since debug mode is turned off in the config. To change this, go to: {program_config}")

else:
    debug_message("Can't find old config file. Creating a new config file...")
    with open(program_config, "w") as f:
            yaml.dump(default_config, f)
            f.close()
            debug_message("Config created! Using default config for this session.")

# program gui logic

window = Tk()
window.geometry("100x100")

save_file_selected = None
save_file_root = ""
window.title(f"Schedule 1 Save Editor - {version} - {save_file_selected}")

debug_message("Window initialized")

def open_save_file(selected_path: str) -> None:
    debug_message("open_save_file called...")
    if zipfile.is_zipfile(selected_path):
        save_file_selected = zipfile.ZipFile(selected_path, "r")
        debug_message("opened file successfully!")

        initial_file_list = save_file_selected.namelist()
        
        if len(initial_file_list) == 1:
            save_file_root = initial_file_list[0]
            debug_message(f"Root directory within the zip is: {root_file}")

        else:
            raise ce.SelectedFileMightNotBeSupported(f"Save file not supported! Expected directory structure within the zip file was wrong. More than one directory detected! Can't process this save file properly!")

    else:
        raise ce.SelectedFileIsNotZipArchive(f"File at {selected_path} is not a zip archive!")

def open_command() -> None:
    open_path = askopenfilename(title="Select the save zip file...")
    if isinstance(open_path, str):
        print("selected")

    else:
        debug_message("No file selected for opening, keeping the old opened save file...")

def save_command() -> None:
    save_path = asksaveasfilename(title="Save the save file as....")
    print(save_path)

def wiki_command() -> None:
    webbrowser.open("https://github.com/sid-the-loser/Schedule-1-Save-Editor", 2, True)

def support_command() -> None:
    webbrowser.open("https://ko-fi.com/sidtheloser", 2, True)

menu = Menu(window)

window.config(menu=menu)

file_menu = Menu(menu, tearoff=False)
file_menu.add_command(label="Open", command=open_command)
file_menu.add_command(label="Save", command=save_command)

help_menu = Menu(menu, tearoff=False)
help_menu.add_command(label="Wiki (opens a web page)", command=wiki_command)
help_menu.add_command(label="Support me (opens a web page)", command=support_command)

menu.add_cascade(label="File", menu=file_menu)
menu.add_cascade(label="Help", menu=help_menu)

main_tabs = ttk.Notebook(window)

main_tabs.pack(expand=1, fill="both")

# frames go here

debug_message("Mainloop has begun...")

window.mainloop()

debug_message("Program closed successfully!")