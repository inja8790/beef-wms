from . import db
from datetime import datetime

class Supplier(db.Model):
    """供应商表"""
    __tablename__ = 'supplier'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)  # SUP001, SUP002, ...
    name = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(50), nullable=False)  # 原产国
    contact = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    batches = db.relationship('Batch', backref='supplier', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'country': self.country,
            'contact': self.contact,
            'phone': self.phone,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Supplier {self.code}: {self.name}>'
