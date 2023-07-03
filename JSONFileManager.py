import os
import json
import sys
from ColorText import print_colored_text


class JSONFileManager:
    def __init__(self, json_file_name="saved_paths", json_folder="Saved_JSON_Data"):
        script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        json_dir = os.path.join(script_dir, json_folder)
        self.saved_file_path = os.path.join(json_dir, json_file_name + ".json")

    def read_json_file(self):
        file_path = self.saved_file_path

        if not os.path.exists(file_path):
            # Return a default value if the file is not found
            print_colored_text("File not found. Returning empty dictionary.", "RED")
            return {}

        # Read the JSON data from the text file
        with open(file_path, "r") as file:
            json_data = file.read()

        # Convert the JSON data back to a dictionary
        return json.loads(json_data)

    def save_json_file(self, saved_working_paths):
        try:
            # Create the directory if it doesn't exist
            os.makedirs(os.path.dirname(self.saved_file_path), exist_ok=True)

            # Save the dictionary as JSON
            json_data = json.dumps(saved_working_paths)

            # Write the JSON data to the text file
            with open(self.saved_file_path, "w") as file:
                file.write(json_data)

            print_colored_text("Saved paths have been successfully written to the JSON file.", "GREEN")
        except Exception as e:
            print_colored_text(f"An error occurred while saving the paths: {str(e)}", "RED")
