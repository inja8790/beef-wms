"""供应商管理路由"""
from flask import Blueprint, render_template, request, jsonify
from models import db, Supplier
from services.auto_code_generator import CodeGenerator
from datetime import datetime

bp = Blueprint('supplier', __name__)

@bp.route('/')
def list_suppliers():
    """供应商列表"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        search = request.args.get('search', '', type=str)
        
        query = Supplier.query
        if search:
            query = query.filter(
                db.or_(
                    Supplier.code.ilike(f'%{search}%'),
                    Supplier.name.ilike(f'%{search}%')
                )
            )
        
        paginated = query.order_by(Supplier.id.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return render_template(
            'supplier/list.html',
            suppliers=paginated.items,
            pagination=paginated,
            search=search,
            per_page=per_page
        )
    except Exception as e:
        return render_template('error.html', error=str(e))

@bp.route('/create', methods=['GET', 'POST'])
def create_supplier():
    """创建供应商"""
    if request.method == 'POST':
        try:
            data = request.get_json()
            
            supplier = Supplier(
                code=CodeGenerator.generate_supplier_code(),
                name=data.get('name', '').strip(),
                country=data.get('country', '').strip(),
                contact=data.get('contact', ''),
                phone=data.get('phone', '')
            )
            
            db.session.add(supplier)
            db.session.commit()
            
            return jsonify({
                'status': 'success',
                'message': '供应商创建成功',
                'data': supplier.to_dict()
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 400
    
    return render_template('supplier/create.html')

@bp.route('/<int:supplier_id>/edit', methods=['GET', 'POST'])
def edit_supplier(supplier_id):
    """编辑供应商"""
    supplier = Supplier.query.get_or_404(supplier_id)
    
    if request.method == 'POST':
        try:
            data = request.get_json()
            supplier.name = data.get('name', '').strip()
            supplier.country = data.get('country', '').strip()
            supplier.contact = data.get('contact', '')
            supplier.phone = data.get('phone', '')
            supplier.updated_at = datetime.utcnow()
            
            db.session.commit()
            
            return jsonify({
                'status': 'success',
                'message': '供应商更新成功',
                'data': supplier.to_dict()
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 400
    
    return render_template('supplier/edit.html', supplier=supplier)

@bp.route('/<int:supplier_id>/delete', methods=['DELETE'])
def delete_supplier(supplier_id):
    """删除供应商"""
    try:
        supplier = Supplier.query.get_or_404(supplier_id)
        db.session.delete(supplier)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': '供应商删除成功'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

@bp.route('/api/search')
def search_suppliers():
    """模糊搜索供应商"""
    try:
        keyword = request.args.get('keyword', '', type=str)
        suppliers = Supplier.query.filter(
            db.or_(
                Supplier.code.ilike(f'%{keyword}%'),
                Supplier.name.ilike(f'%{keyword}%')
            )
        ).limit(20).all()
        
        return jsonify({
            'status': 'success',
            'data': [s.to_dict() for s in suppliers]
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@bp.route('/api/all')
def get_all_suppliers():
    """获取所有供应商"""
    try:
        suppliers = Supplier.query.all()
        return jsonify({
            'status': 'success',
            'data': [s.to_dict() for s in suppliers]
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500
