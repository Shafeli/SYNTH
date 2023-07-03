from ColorText import print_colored_text


class SavedWorkingPaths:
    def __init__(self):
        self.saved_working_paths = {}

    def add_to_saved_paths(self, nick_name, new_path):  # add new path to the map
        self.saved_working_paths[nick_name] = new_path

    def get_path(self, nick_name):  # returns a path for a given nickname
        return self.saved_working_paths.get(nick_name)

    def delete_path(self, nick_name):   # removing an item from the map
        del self.saved_working_paths[nick_name]

    def clear_paths(self):  # clears the map of paths
        self.saved_working_paths = {}

    def print_saved_paths(self):
        for key, value in self.saved_working_paths.items():
            print_colored_text(key + " " + value, "YELLOW")

