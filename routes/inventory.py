"""库存管理路由"""
from flask import Blueprint, render_template, request, jsonify
from models import db, Inventory, Product, Batch
from datetime import datetime

bp = Blueprint('inventory', __name__)

@bp.route('/')
def list_inventories():
    """库存列表"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        product_id = request.args.get('product_id', None, type=int)
        search = request.args.get('search', '', type=str)
        
        query = Inventory.query.filter(Inventory.current_quantity > 0)
        
        if product_id:
            query = query.filter_by(product_id=product_id)
        if search:
            query = query.join(Product).filter(
                db.or_(
                    Product.code.ilike(f'%{search}%'),
                    Product.name.ilike(f'%{search}%')
                )
            )
        
        paginated = query.order_by(Inventory.id.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        # 统计信息
        total_quantity = db.session.query(
            db.func.sum(Inventory.current_quantity)
        ).filter(Inventory.current_quantity > 0).scalar() or 0
        
        total_value = db.session.query(
            db.func.sum(Inventory.amount)
        ).filter(Inventory.current_quantity > 0).scalar() or 0
        
        products = Product.query.all()
        
        return render_template(
            'inventory/list.html',
            inventories=paginated.items,
            pagination=paginated,
            products=products,
            total_quantity=float(total_quantity),
            total_value=float(total_value),
            search=search,
            per_page=per_page
        )
    except Exception as e:
        return render_template('error.html', error=str(e))

@bp.route('/<int:inventory_id>')
def view_inventory(inventory_id):
    """查看库存详情"""
    inventory = Inventory.query.get_or_404(inventory_id)
    return render_template('inventory/view.html', inventory=inventory)

@bp.route('/api/stats')
def get_inventory_stats():
    """获取库存统计信息"""
    try:
        total_quantity = db.session.query(
            db.func.sum(Inventory.current_quantity)
        ).filter(Inventory.current_quantity > 0).scalar() or 0
        
        total_value = db.session.query(
            db.func.sum(Inventory.amount)
        ).filter(Inventory.current_quantity > 0).scalar() or 0
        
        item_count = Inventory.query.filter(Inventory.current_quantity > 0).count()
        
        return jsonify({
            'status': 'success',
            'data': {
                'total_quantity': float(total_quantity),
                'total_value': float(total_value),
                'item_count': item_count
            }
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
