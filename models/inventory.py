from . import db
from datetime import datetime
from decimal import Decimal

class Inventory(db.Model):
    """库存表"""
    __tablename__ = 'inventory'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    batch_id = db.Column(db.Integer, db.ForeignKey('batch.id'), nullable=False)
    current_quantity = db.Column(db.Numeric(12, 3), nullable=False)  # 当前库存(3位小数)
    unit_price = db.Column(db.Numeric(12, 3), nullable=False)
    amount = db.Column(db.Numeric(15, 3), nullable=False)  # 金额 = 库存数量*单价
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def calculate_amount(self):
        """计算金额"""
        return Decimal(self.current_quantity or 0) * Decimal(self.unit_price or 0)
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'product_name': self.product.name if self.product else None,
            'batch_id': self.batch_id,
            'batch_no': self.batch.batch_no if self.batch else None,
            'current_quantity': float(self.current_quantity) if self.current_quantity else 0,
            'unit_price': float(self.unit_price) if self.unit_price else 0,
            'amount': float(self.amount) if self.amount else 0,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Inventory Product:{self.product_id} Batch:{self.batch_id}>'
