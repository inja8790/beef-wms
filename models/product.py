from . import db
from datetime import datetime
from decimal import Decimal

class Product(db.Model):
    """产品表"""
    __tablename__ = 'product'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)  # PRO001, PRO002, ...
    name = db.Column(db.String(100), nullable=False)
    spec = db.Column(db.String(100))  # 规格
    shelf_life = db.Column(db.Integer, nullable=False)  # 保质期(天数)
    default_price = db.Column(db.Numeric(12, 3), default=0)  # 默认单价
    remarks = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    batches = db.relationship('Batch', backref='product', cascade='all, delete-orphan')
    inbounds = db.relationship('Inbound', backref='product', cascade='all, delete-orphan')
    outbounds = db.relationship('Outbound', backref='product', cascade='all, delete-orphan')
    inventories = db.relationship('Inventory', backref='product', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'spec': self.spec,
            'shelf_life': self.shelf_life,
            'default_price': float(self.default_price) if self.default_price else 0,
            'remarks': self.remarks,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Product {self.code}: {self.name}>'
