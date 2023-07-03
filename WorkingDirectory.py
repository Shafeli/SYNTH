import os
from ColorText import print_colored_text
from RenderWindow import RenderWindow
import zipfile
import shutil
# TODO: Add sorting of working folder either by last updated date and / or by file extension
# TODO: Add making an back up current working dir and compress it
# TODO: Add sending files or folders to a saved path by key name


class WorkingDirectory:
    def __init__(self):
        self.m_working_dir = "not set"
        self.m_files = []

    def open_in_explorer(self):     # Open working path in file exploring
        if self.m_working_dir != "not set":
            os.startfile(self.m_working_dir)

    def set_working_dir(self, path):
        self.m_working_dir = path
        if path:
            self.m_files = os.listdir(path)
        else:
            self.m_files = []

    def reset_working_dir(self):
        self.m_working_dir = "not set"

    def to_string(self):
        return self.m_working_dir

    def create_folder(self, folder_name):
        # Create the full path to the folder by joining the location and name
        folder_path = os.path.join(self.m_working_dir, folder_name)

        try:
            os.mkdir(folder_path)
            print_colored_text("Folder created successfully.", "GREEN")
        except FileNotFoundError:
            print_colored_text("The specified directory does not exist.", "RED")
        except FileExistsError:
            print_colored_text("The folder already exists.", "RED")

    def rename_file_by_name(self, name):
        if self.m_working_dir == "not set":
            print_colored_text("Working Directory is null", "RED")
            return

        for file in self.m_files:
            print(file)
            file_name, file_extension = os.path.splitext(file)
            if name.lower() == file.lower():
                user_name = input("New name for " + file + ": ")
                os.rename(os.path.join(self.m_working_dir, file),
                          os.path.join(self.m_working_dir, user_name + file_extension))
                self.set_working_dir(self.m_working_dir)
                return

    def rename_files(self):
        if self.m_working_dir == "not set":
            print_colored_text("Working Directory is null", "RED")
            return

        path = self.m_working_dir
        files = os.listdir(path)

        for file in files:
            file_name, file_extension = os.path.splitext(file)

            print_colored_text("Enter n = No y = Yes: Would you like to rename: " + file, "YELLOW")
            input_response = input()

            if input_response == "y":
                user_name = input("New name for " + file + ": ")
                os.rename(os.path.join(path, file), os.path.join(path, user_name + file_extension))
                self.set_working_dir(path)

    def make_folder_of_folders(self, folder_group_name, group_amount):

        if self.m_working_dir == "not set":
            print_colored_text("Working Directory is null", "RED")
            return

        # Prompt the user for the folder name and location
        folder_name = folder_group_name
        folder_location = self.m_working_dir

        # Create the full path to the folder by joining the location and name
        folder_path = os.path.join(folder_location, folder_name)

        # Create the "Folder" directory
        os.mkdir(folder_path)

        # Create the sub folders
        for i in range(1, group_amount + 1):
            # Create the name of the sub folder
            module_name = folder_group_name + "_" + str(i)

            # Create the full path to the sub folder
            module_path = os.path.join(folder_path, module_name)

            # Create the sub folder
            os.mkdir(module_path)

            print_colored_text("Created: " + module_path, "BLUE")

    def unzip_file_by_name(self, name):

        if self.m_working_dir == "not set":
            print_colored_text("Working Directory is null", "RED")
            return

        path = self.m_working_dir

        folder_dir = os.listdir(path)
        for file in folder_dir:

            print(file + " " + name)
            if name == file:
                zip_file_path = os.path.join(path, file)
                extract_path = os.path.join(path, os.path.splitext(file)[0])  # Construct the extraction path
                # Create the folder before extracting files
                os.makedirs(extract_path, exist_ok=True)
                self.unzip_file(zip_file_path, extract_path)
                return

        print_colored_text(name + " Not found in " + self.m_working_dir, "RED")

    def zip_file_by_name(self, name):
        if self.m_working_dir == "not set":
            print_colored_text("Working Directory is null", "RED")
            return

        # Skip folders that are already zipped
        if name.endswith(".zip"):
            return

        folder_dir = os.listdir(self.m_working_dir)
        for file in folder_dir:
            folder_path = os.path.join(self.m_working_dir, file)

            if name == file:
                folder_path_zipped = folder_path + ".zip"
                self.zip_folder(folder_path, folder_path_zipped)
                return
        print_colored_text(name + " Not found in " + self.m_working_dir, "RED")

    def zip_all_folders_in_dir(self):
        if self.m_working_dir == "not set":
            print_colored_text("Working Directory is null", "RED")
            return

        RenderWindow.clear_console()
        path = self.m_working_dir

        folder_dir = os.listdir(path)
        for file in folder_dir:
            folder_path = os.path.join(path, file)

            # Skip folders that are already zipped
            if file.endswith(".zip"):
                continue

            folder_path_zipped = folder_path + ".zip"
            self.zip_folder(folder_path, folder_path_zipped)

        print("Press enter key to continue...")
        input()  # Program will pause here until the user enters any input
        print("Continuing...")

    def unzip_all_folders_in_dir(self):

        if self.m_working_dir == "not set":
            print_colored_text("Working Directory is null", "RED")
            return

        RenderWindow.clear_console()
        path = self.m_working_dir

        folder_dir = os.listdir(path)
        for file in folder_dir:
            zip_file_path = os.path.join(path, file)

            # Skip folders that are not zipped
            if not file.endswith(".zip"):
                continue

            extract_path = os.path.join(path, os.path.splitext(file)[0])  # Construct the extraction path
            # Create the folder before extracting files

            os.makedirs(extract_path, exist_ok=True)

            self.unzip_file(zip_file_path, extract_path)

        print("Press enter key to continue...")
        input()  # Program will pause here until the user enters any input
        print("Continuing...")

    def delete_by_name(self, target_name):
        path = self.m_working_dir
        file_path_to_delete = os.path.join(path, target_name)

        if os.path.exists(file_path_to_delete):
            print_colored_text("Are you sure you would like to delete " + target_name + "? Enter n = No, y = Yes: ",
                               "YELLOW")
            input_response = input().strip().lower()    # Convert the input to lowercase and remove leading/trailing

            if input_response == "y":
                # Delete the original file or folder
                if os.path.isfile(file_path_to_delete):
                    os.remove(file_path_to_delete)
                    print_colored_text("Deleting file: " + target_name, "GREEN")
                elif os.path.isdir(file_path_to_delete):
                    shutil.rmtree(file_path_to_delete)
                    print_colored_text("Deleting folder: " + target_name, "GREEN")
            else:
                print_colored_text("Action not confirmed. Aborting deleting: " + target_name, "RED")
        else:
            print_colored_text("Could not find " + target_name, "RED")

    @staticmethod
    def print_folder(path):
        files = os.listdir(path)
        for file in files:
            print_colored_text(file, "WHITE")

    @staticmethod
    def zip_folder(source_folder, zip_file):
        # Create a zip file in write mode
        with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Iterate over all files and subdirectories in the source folder
            for root, dirs, files in os.walk(source_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Add each file to the zip file with its relative path
                    zipf.write(file_path, os.path.relpath(file_path, source_folder))

                    print_string = "Compressing Folder at path: " + source_folder
                    print_colored_text(print_string, "BLUE")

        # Delete the original folder
        shutil.rmtree(source_folder)
        print_colored_text("Cleaning uncompressed data : " + source_folder, "CYAN")

    @staticmethod
    def unzip_file(zip_file_path, extract_path):
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
            print_string = "Decompressing Folder at path: " + zip_file_path
            print_colored_text(print_string, "BLUE")

        # Delete the original zip file
        os.remove(zip_file_path)
        print_colored_text("Cleaning compressed data : " + zip_file_path, "CYAN")
