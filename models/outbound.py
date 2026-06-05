from . import db
from datetime import datetime
from decimal import Decimal

class Outbound(db.Model):
    """出库单表"""
    __tablename__ = 'outbound'
    
    id = db.Column(db.Integer, primary_key=True)
    outbound_no = db.Column(db.String(50), unique=True, nullable=False)
    batch_id = db.Column(db.Integer, db.ForeignKey('batch.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Numeric(12, 3), nullable=False)
    unit_price = db.Column(db.Numeric(12, 3), nullable=False)  # 销售单价
    total_price = db.Column(db.Numeric(15, 3), nullable=False)
    outbound_date = db.Column(db.Date, nullable=False)
    customer_name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def calculate_total_price(self):
        """��算总价"""
        return Decimal(self.quantity or 0) * Decimal(self.unit_price or 0)
    
    def to_dict(self):
        return {
            'id': self.id,
            'outbound_no': self.outbound_no,
            'batch_id': self.batch_id,
            'batch_no': self.batch.batch_no if self.batch else None,
            'product_id': self.product_id,
            'product_name': self.product.name if self.product else None,
            'quantity': float(self.quantity) if self.quantity else 0,
            'unit_price': float(self.unit_price) if self.unit_price else 0,
            'total_price': float(self.total_price) if self.total_price else 0,
            'outbound_date': self.outbound_date.strftime('%Y-%m-%d') if self.outbound_date else None,
            'customer_name': self.customer_name,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Outbound {self.outbound_no}>'
