"""产品管理路由"""
from flask import Blueprint, render_template, request, jsonify
from models import db, Product
from services.auto_code_generator import CodeGenerator
from datetime import datetime

bp = Blueprint('product', __name__)

@bp.route('/')
def list_products():
    """产品列表"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        search = request.args.get('search', '', type=str)
        
        query = Product.query
        if search:
            query = query.filter(
                db.or_(
                    Product.code.ilike(f'%{search}%'),
                    Product.name.ilike(f'%{search}%')
                )
            )
        
        paginated = query.order_by(Product.id.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return render_template(
            'product/list.html',
            products=paginated.items,
            pagination=paginated,
            search=search,
            per_page=per_page
        )
    except Exception as e:
        return render_template('error.html', error=str(e))

@bp.route('/create', methods=['GET', 'POST'])
def create_product():
    """创建产品"""
    if request.method == 'POST':
        try:
            data = request.get_json()
            
            product = Product(
                code=CodeGenerator.generate_product_code(),
                name=data.get('name', '').strip(),
                spec=data.get('spec', ''),
                shelf_life=int(data.get('shelf_life', 0)),
                default_price=data.get('default_price', 0),
                remarks=data.get('remarks', '')
            )
            
            db.session.add(product)
            db.session.commit()
            
            return jsonify({
                'status': 'success',
                'message': '产品创建成功',
                'data': product.to_dict()
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({'status': 'error', 'message': str(e)}), 400
    
    return render_template('product/create.html')

@bp.route('/<int:product_id>/edit', methods=['GET', 'POST'])
def edit_product(product_id):
    """编辑产品"""
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'POST':
        try:
            data = request.get_json()
            product.name = data.get('name', '').strip()
            product.spec = data.get('spec', '')
            product.shelf_life = int(data.get('shelf_life', 0))
            product.default_price = data.get('default_price', 0)
            product.remarks = data.get('remarks', '')
            product.updated_at = datetime.utcnow()
            
            db.session.commit()
            
            return jsonify({
                'status': 'success',
                'message': '产品更新成功',
                'data': product.to_dict()
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({'status': 'error', 'message': str(e)}), 400
    
    return render_template('product/edit.html', product=product)

@bp.route('/<int:product_id>/delete', methods=['DELETE'])
def delete_product(product_id):
    """删除产品"""
    try:
        product = Product.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        
        return jsonify({'status': 'success', 'message': '产品删除成功'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 400

@bp.route('/<int:product_id>')
def view_product(product_id):
    """查看产品详情"""
    product = Product.query.get_or_404(product_id)
    return render_template('product/view.html', product=product)

@bp.route('/api/all')
def get_all_products():
    """获取所有产品"""
    try:
        products = Product.query.all()
        return jsonify({
            'status': 'success',
            'data': [p.to_dict() for p in products]
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
