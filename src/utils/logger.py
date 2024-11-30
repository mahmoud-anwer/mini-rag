import logging


# Create a logger to log events and errors
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)  # Set the minimum log level to DEBUG for detailed logs

# Create a file handler to write logs to a file
file_handler = logging.FileHandler('uvicorn.log')
file_handler.setLevel(logging.DEBUG)  # Set file log level to DEBUG

# Create a log format to structure the logs with timestamp, logger name, log level, and message
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the file handler to the logger to enable logging to file
logger.addHandler(file_handler)
