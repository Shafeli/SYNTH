from colorama import init, Fore, Style
# Initialize colorama
init()


def print_colored_text(text, color):
    """
    Print colored text in the Windows console.
    param text: Text to print.
    param color: Color code (0-15).
    """
    # Set the text color
    color_code = getattr(Fore, color.upper())

    # Reset the text style
    reset_code = Style.RESET_ALL

    # Print the colored text
    print(f"{color_code}{text}{reset_code}")
