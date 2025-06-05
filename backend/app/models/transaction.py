"""Transaction model for Pi payments and rewards."""

from app import db
from datetime import datetime

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    recipient_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    tx_hash = db.Column(db.String(128), unique=True, nullable=True)
    status = db.Column(db.String(20), default='pending')  # pending, completed, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "sender_id": self.sender_id,
            "recipient_id": self.recipient_id,
            "amount": self.amount,
            "description": self.description,
            "tx_hash": self.tx_hash,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f"<Transaction {self.id} {self.status}>"

from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime, timedelta
from enum import Enum
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import event, Index
from app import db
import uuid
import hashlib
import json

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
    Comprehensive transaction system with audit trails and economic controls.
    Built for high-volume Pi Network transactions with proper accounting.
    """
    __tablename__ = 'transactions'
    
    # Primary identification
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    transaction_hash = db.Column(db.String(64), unique=True, nullable=False, index=True)
    
    # Transaction participants
    sender_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True, index=True)
    recipient_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True, index=True)
    
    # Transaction details
    amount = db.Column(db.Numeric(precision=18, scale=8), nullable=False)
    fee = db.Column(db.Numeric(precision=18, scale=8), default=Decimal('0.0'))
    net_amount = db.Column(db.Numeric(precision=18, scale=8), nullable=False)
    
    # Categorization
    transaction_type = db.Column(db.Enum(TransactionType), nullable=False, index=True)
    status = db.Column(db.Enum(TransactionStatus), default=TransactionStatus.PENDING, index=True)
    category = db.Column(db.String(50), index=True)  # For detailed categorization
    
    # Descriptive information
    description = db.Column(db.String(255), nullable=False)
    internal_notes = db.Column(db.Text)  # Admin notes, not visible to users
    reference_id = db.Column(db.String(100), index=True)  # Quest ID, Item ID, etc.
    reference_type = db.Column(db.String(50))  # quest, marketplace_item, etc.
    
    # Blockchain integration (for Pi Network)
    pi_transaction_id = db.Column(db.String(100), unique=True, index=True)
    blockchain_confirmations = db.Column(db.Integer, default=0)
    blockchain_status = db.Column(db.String(20))  # pending, confirmed, failed
    
    # Timing and processing
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    processed_at = db.Column(db.DateTime, index=True)
    completed_at = db.Column(db.DateTime)
    expires_at = db.Column(db.DateTime)  # For pending transactions
    
    # Risk management and fraud prevention
    risk_score = db.Column(db.Float, default=0.0)  # 0-100 risk assessment
    fraud_flags = db.Column(db.Text)  # JSON array of fraud indicators
    requires_manual_review = db.Column(db.Boolean, default=False)
    reviewed_by = db.Column(db.String(36), db.ForeignKey('users.id'))
    reviewed_at = db.Column(db.DateTime)
    
    # Accounting and reconciliation
    balance_before_sender = db.Column(db.Numeric(precision=18, scale=8))
    balance_after_sender = db.Column(db.Numeric(precision=18, scale=8))
    balance_before_recipient = db.Column(db.Numeric(precision=18, scale=8))
    balance_after_recipient = db.Column(db.Numeric(precision=18, scale=8))
    
    # Metadata and context
    metadata = db.Column(db.Text)  # JSON for additional transaction context
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(500))
    
    # Relationships
    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_transactions')
    recipient = db.relationship('User', foreign_keys=[recipient_id], backref='received_transactions')
    reviewer = db.relationship('User', foreign_keys=[reviewed_by])
    
    # Add composite indexes for performance
    __table_args__ = (
        Index('idx_transaction_user_type', 'sender_id', 'transaction_type'),
        Index('idx_transaction_status_created', 'status', 'created_at'),
        Index('idx_transaction_reference', 'reference_type', 'reference_id'),
    )
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.transaction_hash:
            self.transaction_hash = self._generate_transaction_hash()
        if not self.net_amount and self.amount:
            self.net_amount = self.amount - (self.fee or Decimal('0.0'))
    
    def __repr__(self):
        return f'<Transaction {self.id}: {self.amount} Pi ({self.status.value})>'
    
    def _generate_transaction_hash(self) -> str:
        """Generate unique transaction hash for audit purposes."""
        hash_data = f"{self.id}{self.sender_id}{self.recipient_id}{self.amount}{datetime.utcnow().isoformat()}"
        return hashlib.sha256(hash_data.encode()).hexdigest()
    
    @classmethod
    def create_quest_reward(cls, user_id: str, quest_id: int, amount: Decimal, description: str = None) -> 'Transaction':
        """Create a quest reward transaction."""
        return cls(
            recipient_id=user_id,
            amount=amount,
            net_amount=amount,
            transaction_type=TransactionType.QUEST_REWARD,
            description=description or f"Quest completion reward",
            reference_id=str(quest_id),
            reference_type='quest',
            category='game_reward'
        )
    
    @classmethod
    def create_user_transfer(cls, sender_id: str, recipient_id: str, amount: Decimal, 
                           description: str, fee: Decimal = None) -> 'Transaction':
        """Create a user-to-user transfer transaction."""
        calculated_fee = fee or cls.calculate_transfer_fee(amount)
        
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
        """Calculate transaction fee based on amount and platform rules."""
        # Progressive fee structure
        if amount <= Decimal('10.0'):
            return Decimal('0.01')  # Minimal fee for small amounts
        elif amount <= Decimal('100.0'):
            return amount * Decimal('0.01')  # 1% for medium amounts
        else:
            return amount * Decimal('0.005')  # 0.5% for large amounts
    
    def process_transaction(self) -> tuple[bool, str]:
        """
        Process the transaction with comprehensive validation and balance updates.
        Returns (success, error_message)
        """
        if self.status != TransactionStatus.PENDING:
            return False, "Transaction is not in pending status"
        
        try:
            # Set processing status
            self.status = TransactionStatus.PROCESSING
            self.processed_at = datetime.utcnow()
            
            # Validate participants exist
            if self.sender_id:
                sender = db.session.get(User, self.sender_id)
                if not sender:
                    raise ValueError("Sender not found")
                if sender.is_locked:
                    raise ValueError("Sender account is locked")
            
            if self.recipient_id:
                recipient = db.session.get(User, self.recipient_id)
                if not recipient:
                    raise ValueError("Recipient not found")
                if recipient.is_locked:
                    raise ValueError("Recipient account is locked")
            
            # Process sender deduction
            if self.sender_id and self.amount > 0:
                sender = db.session.get(User, self.sender_id)
                
                # Record pre-transaction balance
                self.balance_before_sender = sender.pi_balance
                
                # Check sufficient funds (including fee)
                total_deduction = self.amount + (self.fee or Decimal('0.0'))
                if sender.pi_balance < total_deduction:
                    raise ValueError("Insufficient funds")
                
                # Deduct amount and fee
                sender.pi_balance -= total_deduction
                sender.total_pi_spent += self.amount
                
                # Record post-transaction balance
                self.balance_after_sender = sender.pi_balance
            
            # Process recipient credit
            if self.recipient_id and self.net_amount > 0:
                recipient = db.session.get(User, self.recipient_id)
                
                # Record pre-transaction balance
                self.balance_before_recipient = recipient.pi_balance
                
                # Credit the net amount
                recipient.pi_balance += self.net_amount
                recipient.total_pi_earned += self.net_amount
                
                # Record post-transaction balance
                self.balance_after_recipient = recipient.pi_balance
            
            # Mark as completed
            self.status = TransactionStatus.COMPLETED
            self.completed_at = datetime.utcnow()
            
            # Create audit log entry
            self._create_audit_log("Transaction processed successfully")
            
            db.session.commit()
            return True, "Transaction completed successfully"
            
        except Exception as e:
            # Rollback and mark as failed
            db.session.rollback()
            self.status = TransactionStatus.FAILED
            self.internal_notes = f"Processing failed: {str(e)}"
            self._create_audit_log(f"Transaction failed: {str(e)}")
            
            db.session.commit()
            return False, str(e)
    
    def cancel_transaction(self, reason: str = None) -> bool:
        """Cancel a pending transaction."""
        if self.status not in [TransactionStatus.PENDING, TransactionStatus.PROCESSING]:
            return False
        
        self.status = TransactionStatus.CANCELLED
        if reason:
            self.internal_notes = f"Cancelled: {reason}"
        
        self._create_audit_log(f"Transaction cancelled: {reason or 'No reason provided'}")
        return True
    
    def refund_transaction(self, reason: str = None, partial_amount: Decimal = None) -> 'Transaction':
        """Create a refund transaction for this transaction."""
        if self.status != TransactionStatus.COMPLETED:
            raise ValueError("Can only refund completed transactions")
        
        refund_amount = partial_amount or self.net_amount
        if refund_amount > self.net_amount:
            raise ValueError("Refund amount cannot exceed original transaction amount")
        
        # Create reverse transaction
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
        
        # Mark original as refunded if full refund
        if refund_amount == self.net_amount:
            self.status = TransactionStatus.REFUNDED
        
        self._create_audit_log(f"Refund created: {refund_amount} Pi")
        
        return refund_transaction
    
    def assess_fraud_risk(self) -> float:
        """Assess fraud risk for this transaction."""
        risk_factors = []
        
        # High amount risk
        if self.amount > Decimal('1000.0'):
            risk_factors.append(('high_amount', 20))
        
        # New user risk
        if self.sender_id:
            sender = db.session.get(User, self.sender_id)
            if sender and (datetime.utcnow() - sender.created_at).days < 7:
                risk_factors.append(('new_sender', 15))
        
        # Frequency risk - multiple transactions in short time
        recent_transactions = Transaction.query.filter(
            Transaction.sender_id == self.sender_id,
            Transaction.created_at > datetime.utcnow() - timedelta(hours=1),
            Transaction.status == TransactionStatus.COMPLETED
        ).count()
        
        if recent_transactions > 5:
            risk_factors.append(('high_frequency', 25))
        
        # Calculate total risk score
        total_risk = sum(score for _, score in risk_factors)
        self.risk_score = min(total_risk, 100.0)  # Cap at 100
        
        # Set fraud flags
        self.fraud_flags = json.dumps([flag for flag, _ in risk_factors])
        
        # Mark for manual review if high risk
        if self.risk_score > 70:
            self.requires_manual_review = True
        
        return self.risk_score
    
    def _create_audit_log(self, action: str) -> None:
        """Create audit log entry for transaction."""
        # In a production system, this would log to a separate audit table
        # For now, we'll append to internal notes
        timestamp = datetime.utcnow().isoformat()
        audit_entry = f"[{timestamp}] {action}"
        
        if self.internal_notes:
            self.internal_notes += f"\n{audit_entry}"
        else:
            self.internal_notes = audit_entry
    
    @hybrid_property
    def is_reversible(self) -> bool:
        """Check if transaction can be reversed/refunded."""
        return (self.status == TransactionStatus.COMPLETED and 
                self.transaction_type not in [TransactionType.REFUND, TransactionType.PENALTY])
    
    def get_metadata(self) -> dict:
        """Get parsed metadata as dictionary."""
        if not self.metadata:
            return {}
        try:
            return json.loads(self.metadata)
        except (json.JSONDecodeError, TypeError):
            return {}
    
    def set_metadata(self, metadata_dict: dict) -> None:
        """Set metadata from dictionary."""
        self.metadata = json.dumps(metadata_dict)
    
    def to_dict(self, include_sensitive: bool = False) -> dict:
        """Convert transaction to dictionary for API responses."""
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
            'created_at': self.created_at.isoformat(),
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

# Import User model to avoid circular imports
from app.models.user import User

# Event listeners for automatic processing
@event.listens_for(Transaction, 'after_insert')
def auto_process_safe_transactions(mapper, connection, target):
    """Automatically process low-risk transactions."""
    if target.assess_fraud_risk() < 30 and not target.requires_manual_review:
        # Schedule for immediate processing
        # In production, this would use a task queue like Celery
        pass
