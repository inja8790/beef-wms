"""仓库管理路由"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from models import db, Warehouse
from services.auto_code_generator import CodeGenerator
from datetime import datetime

bp = Blueprint('warehouse', __name__)

@bp.route('/')
def list_warehouses():
    """仓库列表"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        search = request.args.get('search', '', type=str)
        
        query = Warehouse.query
        if search:
            query = query.filter(
                db.or_(
                    Warehouse.code.ilike(f'%{search}%'),
                    Warehouse.name.ilike(f'%{search}%')
                )
            )
        
        paginated = query.order_by(Warehouse.id.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return render_template(
            'warehouse/list.html',
            warehouses=paginated.items,
            pagination=paginated,
            search=search,
            per_page=per_page
        )
    except Exception as e:
        return render_template('error.html', error=str(e))

@bp.route('/create', methods=['GET', 'POST'])
def create_warehouse():
    """创建仓库"""
    if request.method == 'POST':
        try:
            data = request.get_json()
            
            warehouse = Warehouse(
                code=CodeGenerator.generate_warehouse_code(),
                name=data.get('name', '').strip(),
                remarks=data.get('remarks', '')
            )
            
            db.session.add(warehouse)
            db.session.commit()
            
            return jsonify({
                'status': 'success',
                'message': '仓库创建成功',
                'data': warehouse.to_dict()
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 400
    
    return render_template('warehouse/create.html')

@bp.route('/<int:warehouse_id>/edit', methods=['GET', 'POST'])
def edit_warehouse(warehouse_id):
    """编辑仓库"""
    warehouse = Warehouse.query.get_or_404(warehouse_id)
    
    if request.method == 'POST':
        try:
            data = request.get_json()
            warehouse.name = data.get('name', '').strip()
            warehouse.remarks = data.get('remarks', '')
            warehouse.updated_at = datetime.utcnow()
            
            db.session.commit()
            
            return jsonify({
                'status': 'success',
                'message': '仓库更新成功',
                'data': warehouse.to_dict()
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 400
    
    return render_template('warehouse/edit.html', warehouse=warehouse)

@bp.route('/<int:warehouse_id>/delete', methods=['DELETE'])
def delete_warehouse(warehouse_id):
    """删除仓库"""
    try:
        warehouse = Warehouse.query.get_or_404(warehouse_id)
        db.session.delete(warehouse)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': '仓库删除成功'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

@bp.route('/<int:warehouse_id>')
def view_warehouse(warehouse_id):
    """查看仓库详情"""
    warehouse = Warehouse.query.get_or_404(warehouse_id)
    return render_template('warehouse/view.html', warehouse=warehouse)

@bp.route('/api/all')
def get_all_warehouses():
    """获取所有仓库(用于其他模块选择)"""
    try:
        warehouses = Warehouse.query.all()
        return jsonify({
            'status': 'success',
            'data': [w.to_dict() for w in warehouses]
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
