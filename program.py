import os
from SavedWorkingPaths import SavedWorkingPaths
from JSONFileManager import JSONFileManager
from ColorText import print_colored_text
from RenderWindow import RenderWindow
from WorkingDirectory import WorkingDirectory

# TODO: Refactor code to classes and different files
# TODO: UI Manager class
# TODO: Systems container class maybe as project grows need maybe there?
# TODO: Input manager class for commands to be more refined
# TODO: Add a boot folder


def g_boot_path(value):
    global boot_path
    boot_path = value


def saved_paths():
    global saved_working_paths


def prompt_user(_working_directory):
    RenderWindow.clear_console()

    # Define the welcome message
    welcome_message = """\n
     ::::::::      :::   :::     ::::    :::     :::::::::::     :::    :::     
    :+:    :+:     :+:   :+:     :+:+:   :+:         :+:         :+:    :+:     
    +:+             +:+ +:+      :+:+:+  +:+         +:+         +:+    +:+     
    +#++:++#++       +#++:       +#+ +:+ +#+         +#+         +#++:++#++     
           +#+        +#+        +#+  +#+#+#         +#+         +#+    +#+     
    #+#    #+# #+#    #+#    #+# #+#   #+#+# #+#     #+#     #+# #+#    #+# #+# 
    #########  ###    ###    ### ###    #### ###     ###     ### ###    ### ### 

    Welcome to S.Y.N.T.H. - Systematic Yielding for Navigating and Transforming Hierarchies
    """

    # Print the styled welcome message
    print_colored_text(welcome_message, "MAGENTA")

    # Print the styled menu options
    print_colored_text("How can I assist you with: ", "YELLOW")
    print_colored_text(_working_directory.to_string(), "MAGENTA")
    print_colored_text("\n\nDirectory contents:", "YELLOW")
    WorkingDirectory.print_folder(_working_directory.to_string())

    print_colored_text("\nMenu of commands:", "YELLOW")
    print_colored_text("quit: Quit S.Y.N.T.H.", "RED")
    print_colored_text("goto <pre-saved directory>: Change working directory", "CYAN")
    print_colored_text("create <action>: <create dir package>, <create dir>", "CYAN")
    print_colored_text("pack <file name> or <all>: Zip all folders in a directory", "CYAN")
    print_colored_text("unpack <file name> or <all>: Unzip folder in a directory", "CYAN")
    print_colored_text("rename <filename> or <all>: Rename file in the working directory", "CYAN")
    print_colored_text("delete <filename>: deletes requited file or folder in the working directory", "CYAN")
    print_colored_text("open: Open working directory", "CYAN")

    return input("\nEnter your command: ")


def quit_command(value, _working_dir):
    global quit_flag
    quit_flag = True


def rename_command(value, _working_directory):
    command_str = value.upper()

    words = value.split()
    # command = words[0]  # Access the first word (command)

    if command_str == "RENAME ALL":
        _working_directory.rename_files()

    if len(words) > 1:
        _working_directory.rename_file_by_name(words[1])


def default_case(value, _working_directory):
    print("Invalid Input Please Try Again : " + value + " is not known")


def make_command(value, _working_directory):
    command_str = value.upper()

    words = value.split()
    command = words[0]  # Access the first word (command)

    if command_str == "CREATE DIR PACKAGE":
        # Prompt the user for the folder name and location
        folder_name = input("Enter the name of the Main Directory : ")
        amount = input("How many sub directories? : ")
        _working_directory.make_folder_of_folders(folder_name, int(amount))

    if words[1].upper() == "DIR":
        print_colored_text("Enter a name for the new folder: ", "YELLOW")
        folder_name = input()
        _working_directory.create_folder(folder_name)


def go_to_command(value, _working_directory):

    words = value.split()
    command = words[0]  # Access the first word (command)

    if command == 'BOOT':
        if boot_path:
            _working_directory.set_working_dir(boot_path)
            return

    # If passed just a command and no target
    if len(words) == 1:
        print_colored_text("Would you like to use a pre-saved file path? Enter n = No y = Yes: ", "YELLOW")
        user_path = input()

        if user_path == "n":
            print_colored_text("Enter a new path to a working directory: ", "YELLOW")
            user_path = input()
            _working_directory.set_working_dir(user_path)

            print_colored_text("Would you like to save path for later? Enter n = No y = Yes: ", "YELLOW")
            user_path = input()

            if user_path == "y":
                print_colored_text("What should we call this saved path: ", "YELLOW")
                user_path = input()
                saved_working_paths[user_path] = _working_directory.m_working_dir
            else:
                return

        if user_path == "y":
            print_colored_text("No problem saved directories are as follows: \n", "YELLOW")
            print_colored_text(saved_working_paths, "BLUE")

            print_colored_text("Enter the name of a working directory from the saved list: ", "YELLOW")
            user_path = input()
            saved_path = saved_working_paths.get(user_path)
            if saved_path:
                _working_directory.set_working_dir(saved_path)
            else:
                print_colored_text("Invalid saved path. Please try again.", "RED")
                go_to_command("junk", _working_directory)  # Recursively redo if bad input
    else:
        target = saved_working_paths.get(words[1])
        _working_directory.set_working_dir(target)


def pack_command(value, _working_dir):
    command_str = value.upper()

    words = value.split()
    command = words[0]  # Access the first word (command)

    if command_str == "PACK ALL":
        _working_dir.zip_all_folders_in_dir()
        return

    if len(words) > 1:
        _working_dir.zip_file_by_name(words[1])


def unpack_command(value, _working_dir):

    command_str = value.upper()

    words = value.split()
    command = words[0]  # Access the first word (command)

    if command_str == "UNPACK ALL":
        _working_dir.unzip_all_folders_in_dir()
        return

    if len(words) > 1:
        _working_dir.unzip_file_by_name(words[1])


def delete_command(value, _working_dir):
    words = value.split()
    to_delete_name = words[1]  # Access the second word (target)

    _working_dir.delete_by_name(to_delete_name)


def open_command(value, _working_dir):
    _working_dir.open_in_explorer()


def set_command(value, _working_dir):
    cases = {
        'BOOT': boot_command
    }

    # Convert the value to uppercase for case-insensitive matching
    upper_value = value.upper()
    words = upper_value.split()
    command = words[1]  # Access the second word (sub-command)
    # Get the function associated with the value, or default_case if not found
    handler = cases.get(command, default_case)
    # Call the retrieved function
    handler(value, _working_dir)


def boot_command(value, _working_dir):
    print_colored_text("What Saved path would you like to set as a boot folder? ", "YELLOW")
    input_response = input()

    if input_response != 'reset':
        g_boot_path(saved_working_paths[input_response])
    else:
        g_boot_path({})


def process_input(value, _working_dir):
    cases = {
        'GOTO': go_to_command,
        'CREATE': make_command,                 # 'CREATE <action>'
        'PACK': pack_command,                   # 'PACK <target>'
        'UNPACK': unpack_command,               # 'UNPACK <target>'
        'RENAME': rename_command,               # 'RENAME <target>'
        'QUIT': quit_command,                   # 'QUIT'
        'DELETE': delete_command,               # 'DELETE'
        'OPEN': open_command,                   # 'OPEN'
        'SET': set_command                      # 'SET'
    }

    # Convert the value to uppercase for case-insensitive matching
    upper_value = value.upper()
    words = upper_value.split()
    command = words[0]  # Access the first word (command)
    # Get the function associated with the value, or default_case if not found
    handler = cases.get(command, default_case)
    # Call the retrieved function
    handler(value, _working_dir)


if __name__ == '__main__':

    saved_paths_data = JSONFileManager("saved_paths", "JSON_Data")
    boot_path_data = JSONFileManager("boot_path", "JSON_Boot_Data")

    working_directory = WorkingDirectory()

    quit_flag = False

    saved_working_paths = saved_paths_data.read_json_file()
    boot_path = boot_path_data.read_json_file()

    junk = "BOOT"
    go_to_command(junk, working_directory)

    while not quit_flag:

        # Prompt user get response
        user_response = prompt_user(working_directory)

        # Process response from user
        process_input(user_response, working_directory)

    # Save out the dictionary to the json file
    print(saved_working_paths)
    saved_paths_data.save_json_file(saved_working_paths)
    boot_path_data.save_json_file(boot_path)
