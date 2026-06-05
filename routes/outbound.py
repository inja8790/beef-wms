"""出库管理路由"""
from flask import Blueprint, render_template, request, jsonify
from models import db, Outbound, Batch, Inventory
from services.auto_code_generator import CodeGenerator
from datetime import datetime
from decimal import Decimal

bp = Blueprint('outbound', __name__)

@bp.route('/')
def list_outbounds():
    """出库单列表"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        search = request.args.get('search', '', type=str)
        batch_id = request.args.get('batch_id', None, type=int)
        
        query = Outbound.query
        
        if search:
            query = query.filter(Outbound.outbound_no.ilike(f'%{search}%'))
        if batch_id:
            query = query.filter_by(batch_id=batch_id)
        
        paginated = query.order_by(Outbound.id.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return render_template(
            'outbound/list.html',
            outbounds=paginated.items,
            pagination=paginated,
            search=search,
            per_page=per_page
        )
    except Exception as e:
        return render_template('error.html', error=str(e))

@bp.route('/create', methods=['GET', 'POST'])
def create_outbound():
    """创建出库单"""
    if request.method == 'POST':
        try:
            data = request.get_json()
            
            batch_id = data.get('batch_id')
            batch = Batch.query.get(batch_id)
            
            if not batch:
                return jsonify({'status': 'error', 'message': '批次不存在'}), 400
            
            quantity = Decimal(str(data.get('quantity', 0)))
            unit_price = Decimal(str(data.get('unit_price', 0)))
            total_price = quantity * unit_price
            
            outbound = Outbound(
                outbound_no=CodeGenerator.generate_outbound_no(),
                batch_id=batch_id,
                product_id=batch.product_id,
                quantity=quantity,
                unit_price=unit_price,
                total_price=total_price,
                outbound_date=datetime.strptime(data.get('outbound_date'), '%Y-%m-%d').date(),
                customer_name=data.get('customer_name', '')
            )
            
            db.session.add(outbound)
            
            # 更新库存
            inventory = Inventory.query.filter_by(
                product_id=batch.product_id,
                batch_id=batch_id
            ).first()
            
            if inventory and inventory.current_quantity >= quantity:
                inventory.current_quantity -= quantity
                inventory.amount = inventory.current_quantity * inventory.unit_price
            else:
                return jsonify({'status': 'error', 'message': '库存不足'}), 400
            
            db.session.commit()
            
            return jsonify({
                'status': 'success',
                'message': '出库单创建成功',
                'data': outbound.to_dict()
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({'status': 'error', 'message': str(e)}), 400
    
    batches = Batch.query.all()
    return render_template('outbound/create.html', batches=batches)

@bp.route('/<int:outbound_id>')
def view_outbound(outbound_id):
    """查看出库单详情"""
    outbound = Outbound.query.get_or_404(outbound_id)
    return render_template('outbound/view.html', outbound=outbound)
