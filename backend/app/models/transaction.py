"""
Transaction model for Pi payments and rewards.

Professional, auditable, and extensible transaction record for all economic actions
in Palace of Quests. Handles user-to-user payments, marketplace, subscriptions,
rewards, refunds, and blockchain integration.
"""

import uuid
import hashlib
import json
import logging
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from enum import Enum

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import event, Index

from app import db

logger = logging.getLogger(__name__)

class TransactionType(Enum):
    QUEST_REWARD = "quest_reward"
    MARKETPLACE_PURCHASE = "marketplace_purchase"
    MARKETPLACE_SALE = "marketplace_sale"
    USER_TRANSFER = "user_transfer"
    PREMIUM_SUBSCRIPTION = "premium_subscription"
    ADMIN_ADJUSTMENT = "admin_adjustment"
    REFUND = "refund"
    PENALTY = "penalty"
    BONUS_REWARD = "bonus_reward"
    ACHIEVEMENT_REWARD = "achievement_reward"
    DAILY_LOGIN_BONUS = "daily_login_bonus"

class TransactionStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

class Transaction(db.Model):
    """
    Comprehensive transaction system with audit trails and economic controls
    for high-volume Pi Network transactions.
    """

    __tablename__ = 'transactions'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    transaction_hash = db.Column(db.String(64), unique=True, nullable=False, index=True)

    sender_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True, index=True)
    recipient_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True, index=True)

    amount = db.Column(db.Numeric(18, 8), nullable=False)
    fee = db.Column(db.Numeric(18, 8), default=Decimal('0.0'))
    net_amount = db.Column(db.Numeric(18, 8), nullable=False)

    transaction_type = db.Column(db.Enum(TransactionType), nullable=False, index=True)
    status = db.Column(db.Enum(TransactionStatus), default=TransactionStatus.PENDING, index=True)
    category = db.Column(db.String(50), index=True)

    description = db.Column(db.String(255), nullable=False)
    internal_notes = db.Column(db.Text)
    reference_id = db.Column(db.String(100), index=True)
    reference_type = db.Column(db.String(50))

    pi_transaction_id = db.Column(db.String(100), unique=True, index=True)
    blockchain_confirmations = db.Column(db.Integer, default=0)
    blockchain_status = db.Column(db.String(20))

    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    processed_at = db.Column(db.DateTime, index=True)
    completed_at = db.Column(db.DateTime)
    expires_at = db.Column(db.DateTime)

    risk_score = db.Column(db.Float, default=0.0)
    fraud_flags = db.Column(db.Text)
    requires_manual_review = db.Column(db.Boolean, default=False)
    reviewed_by = db.Column(db.String(36), db.ForeignKey('users.id'))
    reviewed_at = db.Column(db.DateTime)

    balance_before_sender = db.Column(db.Numeric(18, 8))
    balance_after_sender = db.Column(db.Numeric(18, 8))
    balance_before_recipient = db.Column(db.Numeric(18, 8))
    balance_after_recipient = db.Column(db.Numeric(18, 8))

    metadata = db.Column(db.Text)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(500))

    # Relationships
    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_transactions', lazy='joined')
    recipient = db.relationship('User', foreign_keys=[recipient_id], backref='received_transactions', lazy='joined')
    reviewer = db.relationship('User', foreign_keys=[reviewed_by], lazy='joined')

    __table_args__ = (
        Index('idx_transaction_user_type', 'sender_id', 'transaction_type'),
        Index('idx_transaction_status_created', 'status', 'created_at'),
        Index('idx_transaction_reference', 'reference_type', 'reference_id'),
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.transaction_hash:
            self.transaction_hash = self._generate_transaction_hash()
        if self.net_amount is None and self.amount is not None:
            self.net_amount = Decimal(self.amount) - (self.fee or Decimal('0.0'))
        if not self.status:
            self.status = TransactionStatus.PENDING

    def __repr__(self) -> str:
        return f'<Transaction {self.id[:8]} {self.amount} Pi ({self.status.value})>'

    def _generate_transaction_hash(self) -> str:
        """Generate a unique hash for integrity and quick lookup."""
        hash_data = f"{self.id}{self.sender_id}{self.recipient_id}{self.amount}{datetime.utcnow().isoformat()}"
        return hashlib.sha256(hash_data.encode()).hexdigest()

    @classmethod
    def create_quest_reward(
        cls,
        user_id: str,
        quest_id: int,
        amount: Decimal,
        description: str = None
    ) -> 'Transaction':
        """
        Factory for quest reward transactions.
        """
        return cls(
            recipient_id=user_id,
            amount=amount,
            net_amount=amount,
            transaction_type=TransactionType.QUEST_REWARD,
            description=description or "Quest completion reward",
            reference_id=str(quest_id),
            reference_type='quest',
            category='game_reward'
        )

    @classmethod
    def create_user_transfer(
        cls,
        sender_id: str,
        recipient_id: str,
        amount: Decimal,
        description: str,
        fee: Decimal = None
    ) -> 'Transaction':
        """
        Factory for peer-to-peer transfer transactions.
        """
        calculated_fee = fee if fee is not None else cls.calculate_transfer_fee(amount)
        return cls(
            sender_id=sender_id,
            recipient_id=recipient_id,
            amount=amount,
            fee=calculated_fee,
            net_amount=amount - calculated_fee,
            transaction_type=TransactionType.USER_TRANSFER,
            description=description,
            category='p2p_transfer'
        )

    @staticmethod
    def calculate_transfer_fee(amount: Decimal) -> Decimal:
        """
        Calculate a transfer fee based on amount tiers.
        """
        if not isinstance(amount, Decimal):
            raise TypeError("Amount must be a Decimal type")
        if amount <= Decimal('10.0'):
            return Decimal('0.01')
        elif amount <= Decimal('100.0'):
            return (amount * Decimal('0.01')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        return (amount * Decimal('0.005')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    def process_transaction(self) -> tuple[bool, str]:
        """
        Process the transaction: update balances, handle status, and commit.
        Returns (success, message).
        """
        if self.status != TransactionStatus.PENDING:
            return False, "Transaction is not in pending status"

        try:
            from app.models.user import User  # Avoid circular import

            self.status = TransactionStatus.PROCESSING
            self.processed_at = datetime.utcnow()

            if self.sender_id:
                sender = db.session.get(User, self.sender_id)
                if not sender or getattr(sender, "is_locked", False):
                    raise ValueError("Sender unavailable or locked.")
                self.balance_before_sender = getattr(sender, "pi_balance", None)
                total_deduction = Decimal(self.amount) + (self.fee or Decimal('0.0'))
                if getattr(sender, "pi_balance", Decimal('0.0')) < total_deduction:
                    raise ValueError("Insufficient funds")
                sender.pi_balance -= total_deduction
                sender.total_pi_spent = float(getattr(sender, "total_pi_spent", 0)) + float(self.amount)
                self.balance_after_sender = sender.pi_balance

            if self.recipient_id:
                recipient = db.session.get(User, self.recipient_id)
                if not recipient or getattr(recipient, "is_locked", False):
                    raise ValueError("Recipient unavailable or locked.")
                self.balance_before_recipient = getattr(recipient, "pi_balance", None)
                recipient.pi_balance += self.net_amount
                recipient.total_pi_earned = float(getattr(recipient, "total_pi_earned", 0)) + float(self.net_amount)
                self.balance_after_recipient = recipient.pi_balance

            self.status = TransactionStatus.COMPLETED
            self.completed_at = datetime.utcnow()
            self._create_audit_log("Transaction processed successfully")
            db.session.commit()
            return True, "Transaction completed successfully"
        except Exception as e:
            db.session.rollback()
            self.status = TransactionStatus.FAILED
            self.internal_notes = f"Processing failed: {repr(e)}"
            logger.error(f"Transaction {self.id} failed: {e}")
            self._create_audit_log(f"Transaction failed: {repr(e)}")
            db.session.commit()
            return False, str(e)

    def cancel_transaction(self, reason: str = None) -> bool:
        """
        Cancel a pending or processing transaction.
        """
        if self.status not in {TransactionStatus.PENDING, TransactionStatus.PROCESSING}:
            return False
        self.status = TransactionStatus.CANCELLED
        if reason:
            self.internal_notes = (self.internal_notes or "") + f"\nCancelled: {reason}"
        self._create_audit_log(f"Transaction cancelled: {reason or 'No reason provided'}")
        return True

    def refund_transaction(self, reason: str = None, partial_amount: Decimal = None) -> 'Transaction':
        """
        Create a refund transaction and update original transaction status.
        """
        if self.status != TransactionStatus.COMPLETED:
            raise ValueError("Can only refund completed transactions")
        refund_amount = partial_amount or self.net_amount
        if refund_amount > self.net_amount:
            raise ValueError("Refund amount cannot exceed original transaction amount")
        refund_transaction = Transaction(
            sender_id=self.recipient_id,
            recipient_id=self.sender_id,
            amount=refund_amount,
            net_amount=refund_amount,
            transaction_type=TransactionType.REFUND,
            description=f"Refund for transaction {self.id[:8]}",
            reference_id=self.id,
            reference_type='refund',
            category='refund'
        )
        if refund_amount == self.net_amount:
            self.status = TransactionStatus.REFUNDED
        self._create_audit_log(f"Refund created: {refund_amount} Pi")
        return refund_transaction

    def assess_fraud_risk(self) -> float:
        """
        Evaluate risk using configurable rules. Sets risk_score and flags.
        Returns a float risk score (0-100).
        """
        from app.models.user import User
        risk_factors = []
        # Pluggable risk rules for extensibility
        if self.amount > Decimal('1000.0'):
            risk_factors.append(('high_amount', 20))
        if self.sender_id:
            sender = db.session.get(User, self.sender_id)
            if sender and (datetime.utcnow() - sender.created_at).days < 7:
                risk_factors.append(('new_sender', 15))
        recent_transactions = Transaction.query.filter(
            Transaction.sender_id == self.sender_id,
            Transaction.created_at > datetime.utcnow() - timedelta(hours=1),
            Transaction.status == TransactionStatus.COMPLETED
        ).count()
        if recent_transactions > 5:
            risk_factors.append(('high_frequency', 25))
        total_risk = sum(score for _, score in risk_factors)
        self.risk_score = min(total_risk, 100.0)
        self.fraud_flags = json.dumps([flag for flag, _ in risk_factors])
        if self.risk_score > 70:
            self.requires_manual_review = True
        return self.risk_score

    def _create_audit_log(self, action: str) -> None:
        """
        Append audit log entry to internal notes with UTC timestamp.
        """
        timestamp = datetime.utcnow().isoformat()
        audit_entry = f"[{timestamp}] {action}"
        if self.internal_notes:
            self.internal_notes += f"\n{audit_entry}"
        else:
            self.internal_notes = audit_entry

    @hybrid_property
    def is_reversible(self) -> bool:
        """
        Transaction can be reversed if completed and not a penalty/refund.
        """
        return (self.status == TransactionStatus.COMPLETED and
                self.transaction_type not in {TransactionType.REFUND, TransactionType.PENALTY})

    def get_metadata(self) -> dict:
        """
        Safely decode metadata as JSON.
        """
        if not self.metadata:
            return {}
        try:
            return json.loads(self.metadata)
        except (json.JSONDecodeError, TypeError):
            return {}

    def set_metadata(self, metadata_dict: dict) -> None:
        """
        Store dict metadata as JSON.
        """
        self.metadata = json.dumps(metadata_dict)

    def to_dict(self, include_sensitive: bool = False) -> dict:
        """
        Serialize transaction for API or logging.
        Set include_sensitive=True to include sensitive fields.
        """
        transaction_data = {
            'id': self.id,
            'amount': str(self.amount),
            'net_amount': str(self.net_amount),
            'fee': str(self.fee) if self.fee else None,
            'transaction_type': self.transaction_type.value,
            'status': self.status.value,
            'description': self.description,
            'reference_id': self.reference_id,
            'reference_type': self.reference_type,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }
        if include_sensitive:
            transaction_data.update({
                'transaction_hash': self.transaction_hash,
                'sender_id': self.sender_id,
                'recipient_id': self.recipient_id,
                'risk_score': self.risk_score,
                'requires_manual_review': self.requires_manual_review,
                'internal_notes': self.internal_notes,
                'metadata': self.get_metadata()
            })
        return transaction_data

@event.listens_for(Transaction, 'after_insert')
def auto_process_safe_transactions(mapper, connection, target):
    """
    Automatically process low-risk transactions (production: enqueue to worker).
    """
    if target.assess_fraud_risk() < 30 and not target.requires_manual_review:
        # TODO: In production, enqueue a background task or process immediately.
        pass
