import os


class RenderWindow:
    def __init__(self):
        pass

    @staticmethod
    def clear_console():
        os.system('cls' if os.name == 'nt' else 'clear')

            