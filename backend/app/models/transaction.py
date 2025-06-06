"""
Transaction System for Pi Network Integration
Comprehensive transaction handling with escrow and security features.
"""

import uuid
import enum
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from decimal import Decimal
from sqlalchemy import event
from sqlalchemy.ext.hybrid import hybrid_property

from app.extensions import db
from app.core.exceptions import ValidationError, InsufficientFundsError


class TransactionType(enum.Enum):
    """Transaction type enumeration."""
    TRANSFER = "transfer"
    QUEST_REWARD = "quest_reward"
    MARKETPLACE_PURCHASE = "marketplace_purchase"
    MARKETPLACE_SALE = "marketplace_sale"
    ADMIN_ADJUSTMENT = "admin_adjustment"
    WITHDRAWAL = "withdrawal"
    DEPOSIT = "deposit"
    COMMISSION = "commission"
    REFUND = "refund"


class TransactionStatus(enum.Enum):
    """Transaction status enumeration."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    DISPUTED = "disputed"
    REFUNDED = "refunded"


class Transaction(db.Model):
    """
    Comprehensive transaction model with Pi Network integration.
    Handles all financial operations with proper audit trails.
    """
    
    __tablename__ = 'transactions'
    
    # Primary identification
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    reference_number = db.Column(db.String(20), unique=True, nullable=False)
    
    # Transaction participants
    sender_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    receiver_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    
    # Transaction details
    transaction_type = db.Column(db.Enum(TransactionType), nullable=False)
    amount = db.Column(db.Numeric(precision=20, scale=8), nullable=False)
    currency = db.Column(db.String(10), default='PI', nullable=False)
    description = db.Column(db.String(500), nullable=True)
    
    # Status and processing
    status = db.Column(db.Enum(TransactionStatus), default=TransactionStatus.PENDING, nullable=False)
    priority = db.Column(db.Integer, default=5, nullable=False)  # 1-10, 1 being highest
    
    # Pi Network integration
    pi_transaction_id = db.Column(db.String(100), unique=True, nullable=True)
    pi_payment_id = db.Column(db.String(100), unique=True, nullable=True)
    blockchain_hash = db.Column(db.String(128), nullable=True)
    
    # Fees and calculations
    base_fee = db.Column(db.Numeric(precision=20, scale=8), default=0, nullable=False)
    network_fee = db.Column(db.Numeric(precision=20, scale=8), default=0, nullable=False)
    total_fee = db.Column(db.Numeric(precision=20, scale=8), default=0, nullable=False)
    net_amount = db.Column(db.Numeric(precision=20, scale=8), nullable=False)
    
    # Reference data
    reference_type = db.Column(db.String(50), nullable=True)  # quest, marketplace_item, etc.
    reference_id = db.Column(db.String(36), nullable=True)
    metadata = db.Column(db.JSON, nullable=True)
    
    # Processing timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    processed_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    expires_at = db.Column(db.DateTime, nullable=True)
    
    # Error handling
    error_code = db.Column(db.String(50), nullable=True)
    error_message = db.Column(db.Text, nullable=True)
    retry_count = db.Column(db.Integer, default=0, nullable=False)
    
    # Relationships
    sender = db.relationship('User', backref='sent_transactions', foreign_keys=[sender_id])
    receiver = db.relationship('User', backref='received_transactions', foreign_keys=[receiver_id])
    
    # Constraints
    __table_args__ = (
        db.CheckConstraint('amount > 0', name='valid_amount'),
        db.CheckConstraint('priority >= 1 AND priority <= 10', name='valid_priority'),
        db.CheckConstraint('retry_count >= 0', name='valid_retry_count'),
        db.Index('idx_transaction_status_created', 'status', 'created_at'),
        db.Index('idx_transaction_type_date', 'transaction_type', 'created_at'),
        db.Index('idx_transaction_reference', 'reference_type', 'reference_id'),
        db.Index('idx_transaction_participants', 'sender_id', 'receiver_id'),
    )
    
    def __init__(self, **kwargs):
        """Initialize transaction with auto-generated reference number."""
        if 'reference_number' not in kwargs:
            kwargs['reference_number'] = self._generate_reference_number()
        
        # Calculate net amount
        amount = kwargs.get('amount', 0)
        total_fee = kwargs.get('total_fee', 0)
        kwargs['net_amount'] = amount - total_fee
        
        # Set expiration for pending transactions
        if 'expires_at' not in kwargs and kwargs.get('status') == TransactionStatus.PENDING:
            kwargs['expires_at'] = datetime.utcnow() + timedelta(hours=24)
        
        super().__init__(**kwargs)
    
    @hybrid_property
    def is_expired(self) -> bool:
        """Check if transaction has expired."""
        return (self.expires_at is not None and 
                self.expires_at <= datetime.utcnow() and
                self.status == TransactionStatus.PENDING)
    
    @hybrid_property
    def processing_time(self) -> Optional[timedelta]:
        """Calculate transaction processing time."""
        if self.completed_at:
            return self.completed_at - self.created_at
        return None
    
    @staticmethod
    def _generate_reference_number() -> str:
        """Generate unique transaction reference number."""
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        random_suffix = str(uuid.uuid4())[:6].upper()
        return f"TXN{timestamp}{random_suffix}"
    
    def calculate_fees(self) -> None:
        """Calculate transaction fees based on type and amount."""
        # Base fee calculation
        if self.transaction_type == TransactionType.TRANSFER:
            self.base_fee = max(Decimal('0.01'), self.amount * Decimal('0.01'))  # 1% or min 0.01 PI
        elif self.transaction_type in [TransactionType.MARKETPLACE_PURCHASE, TransactionType.MARKETPLACE_SALE]:
            self.base_fee = self.amount * Decimal('0.025')  # 2.5% for marketplace
        elif self.transaction_type == TransactionType.WITHDRAWAL:
            self.base_fee = max(Decimal('0.1'), self.amount * Decimal('0.02'))  # 2% or min 0.1 PI
        else:
            self.base_fee = Decimal('0')  # No fee for quest rewards, deposits, etc.
        
        # Network fee (simulated - would integrate with Pi Network)
        self.network_fee = Decimal('0.001') if self.amount > 0 else Decimal('0')
        
        # Total fee
        self.total_fee = self.base_fee + self.network_fee
        
        # Recalculate net amount
        self.net_amount = self.amount - self.total_fee
    
    def process(self) -> bool:
        """
        Process the transaction through Pi Network.
        Returns True if successful, False otherwise.
        """
        if self.status != TransactionStatus.PENDING:
            raise ValidationError("Transaction is not in pending status")
        
        if self.is_expired:
            self.status = TransactionStatus.FAILED
            self.error_message = "Transaction expired"
            return False
        
        try:
            self.status = TransactionStatus.PROCESSING
            self.processed_at = datetime.utcnow()
            
            # Validate participants and balances
            if not self._validate_transaction():
                return False
            
            # Process through Pi Network (simulated)
            success = self._process_pi_payment()
            
            if success:
                self._complete_transaction()
                return True
            else:
                self._fail_transaction("Pi Network payment failed")
                return False
                
        except Exception as e:
            self._fail_transaction(str(e))
            return False
    
    def _validate_transaction(self) -> bool:
        """Validate transaction before processing."""
        # Check sender balance for outgoing transactions
        if self.sender_id and self.transaction_type in [
            TransactionType.TRANSFER, 
            TransactionType.MARKETPLACE_PURCHASE,
            TransactionType.WITHDRAWAL
        ]:
            if self.sender.total_rewards < self.amount:
                self.error_message = "Insufficient balance"
                self.status = TransactionStatus.FAILED
                return False
        
        # Check receiver exists for incoming transactions
        if self.receiver_id and not self.receiver:
            self.error_message = "Invalid receiver"
            self.status = TransactionStatus.FAILED
            return False
        
        return True
    
    def _process_pi_payment(self) -> bool:
        """
        Process payment through Pi Network.
        In production, this would integrate with Pi Network SDK.
        """
        # Simulated Pi Network integration
        import random
        import time
        
        # Simulate network delay
        time.sleep(0.1)
        
        # Simulate success rate (95% success in simulation)
        success = random.random() > 0.05
        
        if success:
            # Generate simulated blockchain data
            self.pi_transaction_id = f"pi_txn_{uuid.uuid4().hex[:16]}"
            self.pi_payment_id = f"pi_pay_{uuid.uuid4().hex[:16]}"
            self.blockchain_hash = f"0x{uuid.uuid4().hex}{uuid.uuid4().hex}"
        
        return success
    
    def _complete_transaction(self) -> None:
        """Complete transaction and update balances."""
        self.status = TransactionStatus.COMPLETED
        self.completed_at = datetime.utcnow()
        
        # Update balances
        if self.sender_id:
            self.sender.total_rewards -= self.amount
        
        if self.receiver_id:
            self.receiver.total_rewards += self.net_amount
    
    def _fail_transaction(self, error_message: str) -> None:
        """Mark transaction as failed."""
        self.status = TransactionStatus.FAILED
        self.error_message = error_message
        self.retry_count += 1
    
    def retry(self) -> bool:
        """Retry failed transaction."""
        if self.status != TransactionStatus.FAILED:
            raise ValidationError("Can only retry failed transactions")
        
        if self.retry_count >= 3:
            raise ValidationError("Maximum retry attempts exceeded")
        
        self.status = TransactionStatus.PENDING
        self.error_message = None
        self.processed_at = None
        
        return self.process()
    
    def cancel(self, reason: str = None) -> None:
        """Cancel pending transaction."""
        if self.status not in [TransactionStatus.PENDING, TransactionStatus.PROCESSING]:
            raise ValidationError("Cannot cancel completed or failed transaction")
        
        self.status = TransactionStatus.CANCELLED
        self.error_message = reason or "Cancelled by user"
    
    def refund(self, reason: str = None) -> 'Transaction':
        """
        Create refund transaction for completed transaction.
        Returns the refund transaction.
        """
        if self.status != TransactionStatus.COMPLETED:
            raise ValidationError("Can only refund completed transactions")
        
        # Create reverse transaction
        refund_txn = Transaction(
            sender_id=self.receiver_id,
            receiver_id=self.sender_id,
            transaction_type=TransactionType.REFUND,
            amount=self.net_amount,
            description=f"Refund for {self.reference_number}: {reason or 'No reason provided'}",
            reference_type='transaction',
            reference_id=self.id,
            metadata={'original_transaction': self.id, 'refund_reason': reason}
        )
        
        # Mark original as refunded
        self.status = TransactionStatus.REFUNDED
        
        db.session.add(refund_txn)
        return refund_txn
    
    def to_dict(self, include_sensitive: bool = False) -> Dict[str, Any]:
        """Convert transaction to dictionary representation."""
        data = {
            'id': self.id,
            'reference_number': self.reference_number,
            'transaction_type': self.transaction_type.value,
            'amount': float(self.amount),
            'currency': self.currency,
            'net_amount': float(self.net_amount),
            'total_fee': float(self.total_fee),
            'status': self.status.value,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'processing_time': str(self.processing_time) if self.processing_time else None
        }
        
        # Add participant information
        if self.sender:
            data['sender'] = {
                'id': self.sender.id,
                'username': self.sender.username,
                'display_name': self.sender.display_name or self.sender.username
            }
        
        if self.receiver:
            data['receiver'] = {
                'id': self.receiver.id,
                'username': self.receiver.username,
                'display_name': self.receiver.display_name or self.receiver.username
            }
        
        if include_sensitive:
            data.update({
                'pi_transaction_id': self.pi_transaction_id,
                'blockchain_hash': self.blockchain_hash,
                'error_message': self.error_message,
                'retry_count': self.retry_count,
                'metadata': self.metadata
            })
        
        return data
    
    @classmethod
    def create_transfer(cls, sender, receiver, amount: Decimal, description: str = None) -> 'Transaction':
        """Create a transfer transaction between users."""
        if sender.id == receiver.id:
            raise ValidationError("Cannot transfer to yourself")
        
        if sender.total_rewards < amount:
            raise InsufficientFundsError("Insufficient balance for transfer")
        
        transaction = cls(
            sender_id=sender.id,
            receiver_id=receiver.id,
            transaction_type=TransactionType.TRANSFER,
            amount=amount,
            description=description or f"Transfer from {sender.username} to {receiver.username}"
        )
        
        transaction.calculate_fees()
        return transaction
    
    @classmethod
    def create_quest_reward(cls, user, amount: Decimal, quest_id: str, description: str = None) -> 'Transaction':
        """Create a quest reward transaction."""
        transaction = cls(
            receiver_id=user.id,
            transaction_type=TransactionType.QUEST_REWARD,
            amount=amount,
            description=description or f"Quest reward for {user.username}",
            reference_type='quest',
            reference_id=quest_id
        )
        
        transaction.calculate_fees()
        return transaction
    
    def __repr__(self) -> str:
        return f"<Transaction {self.reference_number} ({self.status.value})>"


# Event listeners
@event.listens_for(Transaction, 'before_insert')
def set_transaction_defaults(mapper, connection, target):
    """Set default values before insert."""
    target.calculate_fees()


@event.listens_for(Transaction.status, 'set')
def handle_status_change(target, value, old_value, initiator):
    """Handle transaction status changes."""
    if value == TransactionStatus.COMPLETED and not target.completed_at:
        target.completed_at = datetime.utcnow()
    elif value == TransactionStatus.PROCESSING and not target.processed_at:
        target.processed_at = datetime.utcnow()


# Periodic cleanup task (would be run by scheduler)
def cleanup_expired_transactions():
    """Mark expired pending transactions as failed."""
    expired_transactions = Transaction.query.filter(
        Transaction.status == TransactionStatus.PENDING,
        Transaction.expires_at <= datetime.utcnow()
    ).all()
    
    for txn in expired_transactions:
        txn.status = TransactionStatus.FAILED
        txn.error_message = "Transaction expired"
    
    db.session.commit()
    return len(expired_transactions)
