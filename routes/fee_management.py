"""仓储费管理路由"""
from flask import Blueprint, render_template, request, jsonify
from models import db, FeeRule, FeeRecord, Warehouse, Batch
from datetime import datetime, date
from decimal import Decimal

bp = Blueprint('fee_management', __name__)

@bp.route('/rules')
def list_fee_rules():
    """费用规则列表"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        warehouse_id = request.args.get('warehouse_id', None, type=int)
        
        query = FeeRule.query
        if warehouse_id:
            query = query.filter_by(warehouse_id=warehouse_id)
        
        paginated = query.order_by(FeeRule.id.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        warehouses = Warehouse.query.all()
        
        return render_template(
            'fee_management/rules.html',
            fee_rules=paginated.items,
            pagination=paginated,
            warehouses=warehouses,
            per_page=per_page
        )
    except Exception as e:
        return render_template('error.html', error=str(e))

@bp.route('/rules/create', methods=['GET', 'POST'])
def create_fee_rule():
    """创建费用规则"""
    if request.method == 'POST':
        try:
            data = request.get_json()
            
            fee_rule = FeeRule(
                warehouse_id=data.get('warehouse_id'),
                fee_type=data.get('fee_type'),
                unit=data.get('unit'),
                rate=Decimal(str(data.get('rate', 0)))
            )
            
            db.session.add(fee_rule)
            db.session.commit()
            
            return jsonify({
                'status': 'success',
                'message': '费用规则创建成功',
                'data': fee_rule.to_dict()
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({'status': 'error', 'message': str(e)}), 400
    
    warehouses = Warehouse.query.all()
    fee_types = FeeRule.FEE_TYPES
    units = FeeRule.UNITS
    
    return render_template(
        'fee_management/create_rule.html',
        warehouses=warehouses,
        fee_types=fee_types,
        units=units
    )

@bp.route('/records')
def list_fee_records():
    """费用记录列表"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        warehouse_id = request.args.get('warehouse_id', None, type=int)
        batch_id = request.args.get('batch_id', None, type=int)
        
        query = FeeRecord.query
        if warehouse_id:
            query = query.filter_by(warehouse_id=warehouse_id)
        if batch_id:
            query = query.filter_by(batch_id=batch_id)
        
        paginated = query.order_by(FeeRecord.id.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        # 统计信息
        total_amount = db.session.query(
            db.func.sum(FeeRecord.amount)
        ).scalar() or 0
        
        warehouses = Warehouse.query.all()
        
        return render_template(
            'fee_management/records.html',
            fee_records=paginated.items,
            pagination=paginated,
            warehouses=warehouses,
            total_amount=float(total_amount),
            per_page=per_page
        )
    except Exception as e:
        return render_template('error.html', error=str(e))

@bp.route('/records/create', methods=['GET', 'POST'])
def create_fee_record():
    """创建费用记录"""
    if request.method == 'POST':
        try:
            data = request.get_json()
            
            fee_rule = FeeRule.query.get(data.get('fee_rule_id'))
            if not fee_rule:
                return jsonify({'status': 'error', 'message': '费用规则不存在'}), 400
            
            quantity = Decimal(str(data.get('quantity', 0)))
            amount = quantity * fee_rule.rate
            
            fee_record = FeeRecord(
                warehouse_id=fee_rule.warehouse_id,
                batch_id=data.get('batch_id'),
                fee_rule_id=data.get('fee_rule_id'),
                fee_type=fee_rule.fee_type,
                quantity=quantity,
                amount=amount,
                billing_date=datetime.strptime(data.get('billing_date'), '%Y-%m-%d').date()
            )
            
            db.session.add(fee_record)
            db.session.commit()
            
            return jsonify({
                'status': 'success',
                'message': '费用记录创建成功',
                'data': fee_record.to_dict()
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({'status': 'error', 'message': str(e)}), 400
    
    warehouses = Warehouse.query.all()
    fee_rules = FeeRule.query.all()
    batches = Batch.query.all()
    
    return render_template(
        'fee_management/create_record.html',
        warehouses=warehouses,
        fee_rules=fee_rules,
        batches=batches
    )
