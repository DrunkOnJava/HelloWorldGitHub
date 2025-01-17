import logging

# Configure basic logging to console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_input(user_input):
    logging.info(f"User Input: {user_input}")

def log_output(output):
    logging.info(f"Terminal Output: {output}")
