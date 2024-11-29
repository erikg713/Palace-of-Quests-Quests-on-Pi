from app import db
from datetime import datetime
from app.models import Payment

def update_payment_status(payment_id, status, txid=None):
    payment = Payment.query.filter_by(payment_id=payment_id).first()
    if payment:
        payment.status = status
        payment.txid = txid
        payment.updated_at = datetime.utcnow()
        db.session.commit()
