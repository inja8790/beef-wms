from . import db
from datetime import datetime

class Warehouse(db.Model):
    """仓库表"""
    __tablename__ = 'warehouse'
    
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, nullable=False)  # WH001, WH002, ...
    name = db.Column(db.String(100), nullable=False)
    remarks = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    storage_areas = db.relationship('StorageArea', backref='warehouse', cascade='all, delete-orphan')
    fee_rules = db.relationship('FeeRule', backref='warehouse', cascade='all, delete-orphan')
    fee_records = db.relationship('FeeRecord', backref='warehouse', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'remarks': self.remarks,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Warehouse {self.code}: {self.name}>'
