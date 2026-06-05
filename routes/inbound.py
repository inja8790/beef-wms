"""入库管理路由"""
from flask import Blueprint, render_template, request, jsonify
from models import db, Inbound, Batch, Inventory
from services.auto_code_generator import CodeGenerator
from datetime import datetime
from decimal import Decimal

bp = Blueprint('inbound', __name__)

@bp.route('/')
def list_inbounds():
    """入库单列表"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        search = request.args.get('search', '', type=str)
        batch_id = request.args.get('batch_id', None, type=int)
        
        query = Inbound.query
        
        if search:
            query = query.filter(Inbound.inbound_no.ilike(f'%{search}%'))
        if batch_id:
            query = query.filter_by(batch_id=batch_id)
        
        paginated = query.order_by(Inbound.id.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return render_template(
            'inbound/list.html',
            inbounds=paginated.items,
            pagination=paginated,
            search=search,
            per_page=per_page
        )
    except Exception as e:
        return render_template('error.html', error=str(e))

@bp.route('/create', methods=['GET', 'POST'])
def create_inbound():
    """创建入库单"""
    if request.method == 'POST':
        try:
            data = request.get_json()
            
            batch_id = data.get('batch_id')
            batch = Batch.query.get(batch_id)
            
            if not batch:
                return jsonify({'status': 'error', 'message': '批次不存在'}), 400
            
            quantity = Decimal(str(data.get('quantity', 0)))
            unit_price = Decimal(str(data.get('unit_price', 0))) or batch.unit_price
            total_price = quantity * unit_price
            
            inbound = Inbound(
                inbound_no=CodeGenerator.generate_inbound_no(),
                batch_id=batch_id,
                product_id=batch.product_id,
                quantity=quantity,
                unit_price=unit_price,
                total_price=total_price,
                inbound_date=datetime.strptime(data.get('inbound_date'), '%Y-%m-%d').date(),
                operator=data.get('operator', '')
            )
            
            db.session.add(inbound)
            
            # 更新库存
            inventory = Inventory.query.filter_by(
                product_id=batch.product_id,
                batch_id=batch_id
            ).first()
            
            if inventory:
                inventory.current_quantity += quantity
                inventory.amount = inventory.current_quantity * inventory.unit_price
            else:
                inventory = Inventory(
                    product_id=batch.product_id,
                    batch_id=batch_id,
                    current_quantity=quantity,
                    unit_price=unit_price,
                    amount=total_price
                )
                db.session.add(inventory)
            
            db.session.commit()
            
            return jsonify({
                'status': 'success',
                'message': '入库单创建成功',
                'data': inbound.to_dict()
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({'status': 'error', 'message': str(e)}), 400
    
    batches = Batch.query.all()
    return render_template('inbound/create.html', batches=batches)

@bp.route('/<int:inbound_id>')
def view_inbound(inbound_id):
    """查看入库单详情"""
    inbound = Inbound.query.get_or_404(inbound_id)
    return render_template('inbound/view.html', inbound=inbound)
