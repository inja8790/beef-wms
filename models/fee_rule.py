from . import db
from datetime import datetime

class FeeRule(db.Model):
    """仓储费规则表"""
    __tablename__ = 'fee_rule'
    
    id = db.Column(db.Integer, primary_key=True)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.id'), nullable=False)
    fee_type = db.Column(db.String(50), nullable=False)  # 出入库操作费、仓储费、抄码费、下架费、拍照费、货权转移费
    unit = db.Column(db.String(50), nullable=False)  # 元/吨/次、元/吨/天、元/件、元/柜等
    rate = db.Column(db.Numeric(12, 3), nullable=False)  # 费率
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    fee_records = db.relationship('FeeRecord', backref='fee_rule', cascade='all, delete-orphan')
    
    FEE_TYPES = {
        'inbound_operation': '出入库操作费',
        'storage': '仓储费',
        'barcode': '抄码费',
        'shelving': '下架费',
        'photo': '拍照费',
        'transfer': '货权转移费'
    }
    
    UNITS = [
        '元/吨/次',
        '元/吨/天',
        '元/件',
        '元/柜'
    ]
    
    def to_dict(self):
        return {
            'id': self.id,
            'warehouse_id': self.warehouse_id,
            'warehouse_name': self.warehouse.name if self.warehouse else None,
            'fee_type': self.fee_type,
            'unit': self.unit,
            'rate': float(self.rate) if self.rate else 0,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<FeeRule {self.fee_type}>'
