"""库区管理路由"""
from flask import Blueprint, render_template, request, jsonify
from models import db, StorageArea, Warehouse
from services.auto_code_generator import CodeGenerator
from datetime import datetime

bp = Blueprint('storage_area', __name__)

@bp.route('/')
def list_storage_areas():
    """库区列表"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        warehouse_id = request.args.get('warehouse_id', None, type=int)
        search = request.args.get('search', '', type=str)
        
        query = StorageArea.query
        
        if warehouse_id:
            query = query.filter_by(warehouse_id=warehouse_id)
        if search:
            query = query.filter(
                db.or_(
                    StorageArea.code.ilike(f'%{search}%'),
                    StorageArea.name.ilike(f'%{search}%')
                )
            )
        
        paginated = query.order_by(StorageArea.id.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        warehouses = Warehouse.query.all()
        
        return render_template(
            'storage_area/list.html',
            storage_areas=paginated.items,
            pagination=paginated,
            warehouses=warehouses,
            selected_warehouse=warehouse_id,
            search=search,
            per_page=per_page
        )
    except Exception as e:
        return render_template('error.html', error=str(e))

@bp.route('/create', methods=['GET', 'POST'])
def create_storage_area():
    """创建库区"""
    if request.method == 'POST':
        try:
            data = request.get_json()
            warehouse_id = data.get('warehouse_id')
            name = data.get('name', '').strip()
            
            if not warehouse_id or not name:
                return jsonify({'status': 'error', 'message': '仓库和库区名称不能为空'}), 400
            
            # 验证仓库存在
            warehouse = Warehouse.query.get(warehouse_id)
            if not warehouse:
                return jsonify({'status': 'error', 'message': '仓库不存在'}), 400
            
            storage_area = StorageArea(
                code=CodeGenerator.generate_storage_area_code(),
                warehouse_id=warehouse_id,
                name=name
            )
            
            db.session.add(storage_area)
            db.session.commit()
            
            return jsonify({
                'status': 'success',
                'message': '库区创建成功',
                'data': storage_area.to_dict()
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({'status': 'error', 'message': str(e)}), 400
    
    warehouses = Warehouse.query.all()
    return render_template('storage_area/create.html', warehouses=warehouses)

@bp.route('/<int:storage_area_id>/edit', methods=['GET', 'POST'])
def edit_storage_area(storage_area_id):
    """编辑库区"""
    storage_area = StorageArea.query.get_or_404(storage_area_id)
    
    if request.method == 'POST':
        try:
            data = request.get_json()
            storage_area.name = data.get('name', '').strip()
            storage_area.updated_at = datetime.utcnow()
            
            db.session.commit()
            
            return jsonify({
                'status': 'success',
                'message': '库区更新成功',
                'data': storage_area.to_dict()
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({'status': 'error', 'message': str(e)}), 400
    
    warehouses = Warehouse.query.all()
    return render_template('storage_area/edit.html', storage_area=storage_area, warehouses=warehouses)

@bp.route('/<int:storage_area_id>/delete', methods=['DELETE'])
def delete_storage_area(storage_area_id):
    """删除库区"""
    try:
        storage_area = StorageArea.query.get_or_404(storage_area_id)
        db.session.delete(storage_area)
        db.session.commit()
        
        return jsonify({'status': 'success', 'message': '库区删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 400

@bp.route('/<int:storage_area_id>')
def view_storage_area(storage_area_id):
    """查看库区详情"""
    storage_area = StorageArea.query.get_or_404(storage_area_id)
    return render_template('storage_area/view.html', storage_area=storage_area)
