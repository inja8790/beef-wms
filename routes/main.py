"""主路由"""
from flask import Blueprint, render_template, jsonify
from models import (
    db, Warehouse, StorageArea, Supplier, Product, Batch,
    Inbound, Outbound, Inventory, FeeRule, FeeRecord
)
from datetime import datetime, timedelta

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/dashboard')
def dashboard():
    """仪表板"""
    try:
        # 统计数据
        warehouse_count = Warehouse.query.count()
        supplier_count = Supplier.query.count()
        product_count = Product.query.count()
        batch_count = Batch.query.count()
        
        # 库存统计
        total_inventory_value = db.session.query(
            db.func.sum(Inventory.amount)
        ).scalar() or 0
        
        # 最近的入库记录
        recent_inbounds = Inbound.query.order_by(Inbound.created_at.desc()).limit(10).all()
        
        # 最近的出库记录
        recent_outbounds = Outbound.query.order_by(Outbound.created_at.desc()).limit(10).all()
        
        # 库存预警(即将过期的批次)
        today = datetime.now().date()
        expire_soon = Batch.query.filter(
            Batch.expiry_date <= today + timedelta(days=30),
            Batch.expiry_date >= today
        ).count()
        
        expired = Batch.query.filter(Batch.expiry_date < today).count()
        
        stats = {
            'warehouse_count': warehouse_count,
            'supplier_count': supplier_count,
            'product_count': product_count,
            'batch_count': batch_count,
            'total_inventory_value': float(total_inventory_value),
            'expire_soon': expire_soon,
            'expired': expired,
            'recent_inbounds': [item.to_dict() for item in recent_inbounds],
            'recent_outbounds': [item.to_dict() for item in recent_outbounds]
        }
        
        return render_template('dashboard.html', stats=stats)
    except Exception as e:
        return render_template('error.html', error=str(e))

@bp.route('/api/stats')
def get_stats():
    """获取统计数据API"""
    try:
        warehouse_count = Warehouse.query.count()
        supplier_count = Supplier.query.count()
        product_count = Product.query.count()
        batch_count = Batch.query.count()
        inbound_count = Inbound.query.count()
        outbound_count = Outbound.query.count()
        
        total_inventory_value = db.session.query(
            db.func.sum(Inventory.amount)
        ).scalar() or 0
        
        return jsonify({
            'status': 'success',
            'data': {
                'warehouse': warehouse_count,
                'supplier': supplier_count,
                'product': product_count,
                'batch': batch_count,
                'inbound': inbound_count,
                'outbound': outbound_count,
                'inventory_value': float(total_inventory_value)
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@bp.route('/health')
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })
