from . import db
from datetime import datetime
from decimal import Decimal

class Inbound(db.Model):
    """入库单表"""
    __tablename__ = 'inbound'
    
    id = db.Column(db.Integer, primary_key=True)
    inbound_no = db.Column(db.String(50), unique=True, nullable=False)
    batch_id = db.Column(db.Integer, db.ForeignKey('batch.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Numeric(12, 3), nullable=False)
    unit_price = db.Column(db.Numeric(12, 3), nullable=False)
    total_price = db.Column(db.Numeric(15, 3), nullable=False)
    inbound_date = db.Column(db.Date, nullable=False)
    operator = db.Column(db.String(50))  # 操作人
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def calculate_total_price(self):
        """计算总价"""
        return Decimal(self.quantity or 0) * Decimal(self.unit_price or 0)
    
    def to_dict(self):
        return {
            'id': self.id,
            'inbound_no': self.inbound_no,
            'batch_id': self.batch_id,
            'batch_no': self.batch.batch_no if self.batch else None,
            'product_id': self.product_id,
            'product_name': self.product.name if self.product else None,
            'quantity': float(self.quantity) if self.quantity else 0,
            'unit_price': float(self.unit_price) if self.unit_price else 0,
            'total_price': float(self.total_price) if self.total_price else 0,
            'inbound_date': self.inbound_date.strftime('%Y-%m-%d') if self.inbound_date else None,
            'operator': self.operator,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Inbound {self.inbound_no}>'
