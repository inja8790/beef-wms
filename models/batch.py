from . import db
from datetime import datetime, timedelta
from decimal import Decimal

class Batch(db.Model):
    """批次表"""
    __tablename__ = 'batch'
    
    id = db.Column(db.Integer, primary_key=True)
    batch_no = db.Column(db.String(50), unique=True, nullable=False)  # 批次号
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)
    country = db.Column(db.String(50), nullable=False)  # 原产国(自动同步)
    production_date = db.Column(db.Date, nullable=False)
    expiry_date = db.Column(db.Date, nullable=False)  # 到期日期(自动计算)
    quantity = db.Column(db.Numeric(12, 3), nullable=False)  # 数量(3位小数)
    unit_price = db.Column(db.Numeric(12, 3), nullable=False)  # 单价
    total_price = db.Column(db.Numeric(15, 3), nullable=False)  # 总价 = 数量*单价
    inbound_time = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    inbounds = db.relationship('Inbound', backref='batch', cascade='all, delete-orphan')
    outbounds = db.relationship('Outbound', backref='batch', cascade='all, delete-orphan')
    inventories = db.relationship('Inventory', backref='batch', cascade='all, delete-orphan')
    fee_records = db.relationship('FeeRecord', backref='batch', cascade='all, delete-orphan')
    
    def calculate_total_price(self):
        """计算总价"""
        return Decimal(self.quantity or 0) * Decimal(self.unit_price or 0)
    
    def calculate_expiry_date(self, production_date, shelf_life_days):
        """计算到期日期"""
        if isinstance(production_date, str):
            production_date = datetime.strptime(production_date, '%Y-%m-%d').date()
        return production_date + timedelta(days=shelf_life_days)
    
    def to_dict(self):
        return {
            'id': self.id,
            'batch_no': self.batch_no,
            'product_id': self.product_id,
            'product_name': self.product.name if self.product else None,
            'supplier_id': self.supplier_id,
            'supplier_name': self.supplier.name if self.supplier else None,
            'country': self.country,
            'production_date': self.production_date.strftime('%Y-%m-%d') if self.production_date else None,
            'expiry_date': self.expiry_date.strftime('%Y-%m-%d') if self.expiry_date else None,
            'quantity': float(self.quantity) if self.quantity else 0,
            'unit_price': float(self.unit_price) if self.unit_price else 0,
            'total_price': float(self.total_price) if self.total_price else 0,
            'inbound_time': self.inbound_time.strftime('%Y-%m-%d %H:%M:%S') if self.inbound_time else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Batch {self.batch_no}>'
