from pi_sdk import PiNetwork
import logging
import os

# Set up logging for debugging
logging.basicConfig(level=logging.INFO)

def process_payment(payment_id):
    try:
        pi_client = PiNetwork(api_key=os.getenv("PI_NETWORK_API_KEY"))
        result = pi_client.complete_payment(payment_id)

        # Check if payment was successfully completed
        if result['status'] == 'completed':
            logging.info(f"Payment {payment_id} successfully completed.")
            return {'message': 'Payment successful'}

        # Handle other possible payment statuses
        elif result['status'] == 'pending':
            logging.warning(f"Payment {payment_id} is still pending.")
            return {'message': 'Payment is pending, please wait for confirmation.'}

        # Handle failed payments
        else:
            logging.error(f"Payment {payment_id} failed with status: {result['status']}")
            raise Exception(f"Payment failed with status: {result['status']}")

    except Exception as e:
        # Log and raise the error for further handling
        logging.error(f"Error processing payment {payment_id}: {str(e)}")
        raise Exception(f"An error occurred while processing the payment: {str(e)}")