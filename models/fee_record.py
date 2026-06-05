from . import db
from datetime import datetime
from decimal import Decimal

class FeeRecord(db.Model):
    """仓储费记录表"""
    __tablename__ = 'fee_record'
    
    id = db.Column(db.Integer, primary_key=True)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.id'), nullable=False)
    batch_id = db.Column(db.Integer, db.ForeignKey('batch.id'), nullable=False)
    fee_rule_id = db.Column(db.Integer, db.ForeignKey('fee_rule.id'), nullable=False)
    fee_type = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Numeric(12, 3), nullable=False)  # 吨/件/柜
    amount = db.Column(db.Numeric(15, 3), nullable=False)  # 金额
    billing_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'warehouse_id': self.warehouse_id,
            'warehouse_name': self.warehouse.name if self.warehouse else None,
            'batch_id': self.batch_id,
            'batch_no': self.batch.batch_no if self.batch else None,
            'fee_rule_id': self.fee_rule_id,
            'fee_type': self.fee_type,
            'quantity': float(self.quantity) if self.quantity else 0,
            'amount': float(self.amount) if self.amount else 0,
            'billing_date': self.billing_date.strftime('%Y-%m-%d') if self.billing_date else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }
    
    def __repr__(self):
        return f'<FeeRecord Batch:{self.batch_id} Type:{self.fee_type}>'
