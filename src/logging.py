"""Module to define the logger for the project."""
import logging
import os


def _configure_logging():
    """Function to create a main logger (once)."""
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # Set the logging level

    # Create a file handler that logs debug and higher level messages
    log_dir = os.path.join(os.path.dirname(__file__), "../logs/")
    log_file = os.path.join(log_dir, "run.log")
    os.makedirs(log_dir, exist_ok=True)

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)

    # Create a console handler for output to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Create a formatter and set it for both handlers
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Remove existing handlers to avoid duplicates
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


_configure_logging()


def get_logger(name: str):
    """Get a logger with the specified name.

    Args:
        name (str): name of the logger.

    Returns:
        logging.Logger: Global logger for logging.
    """
    return logging.getLogger(name)
