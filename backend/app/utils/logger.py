import logging

logging.basicConfig(
    filename="payment_logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_payment_action(action, details):
    logging.info(f"{action}: {details}")