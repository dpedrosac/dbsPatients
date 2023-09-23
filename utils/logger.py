import logging
""" Created logger funktion to track and find issues within the code more easily (if you have trouble with debugging or
    pinpointing where the issue is happening, add logger function in targeted area """
COLORS = {
    'ERROR': '\033[1;4;31m',  # bold, underlined red
    'INFO': '\033[1;4;32m',  # bold, underlined, green
    'RESET': '\033[0m'  # Reset to default color
}


# custom formatter for colored log levels only
class ColoredFormatter(logging.Formatter):
    def format(self, record):
        log_message = super().format(record)
        log_level = record.levelname
        colored_level = COLORS.get(log_level, '')
        return f"{colored_level}[{log_level}]{COLORS['RESET']}: {log_message}"


# Creates logger for file and sets level
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)  # This can be changed for later use in error/logging handling

# Add a colored console handler with the custom formatter
console_handler = logging.StreamHandler()
console_handler.setFormatter(ColoredFormatter('%(message)s'))
if logger.hasHandlers():
    logger.handlers.clear()
logger.addHandler(console_handler)

import logging

# Configure the logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def recursive_function(n):
    if n <= 0:
        logger.debug("Base case reached.")
        return 0
    else:
        logger.debug(f"Recursive call with n = {n}")
        result = n + recursive_function(n - 1)
        return result

if __name__ == "__main__":
    result = recursive_function(5)
    print("Result:", result)
