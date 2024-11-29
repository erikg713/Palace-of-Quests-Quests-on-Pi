from pi_sdk import PiNetwork

def process_payment(payment_id):
    pi_client = PiNetwork(api_key='YOUR_PI_NETWORK_API_KEY')
    result = pi_client.complete_payment(payment_id)
    if result['status'] == 'completed':
        return {'message': 'Payment successful'}
    else:
        raise Exception('Payment failed')

