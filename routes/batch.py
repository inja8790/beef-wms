"""批次管理路由"""
from flask import Blueprint, render_template, request, jsonify
from models import db, Batch, Product, Supplier, Inventory
from services.auto_code_generator import CodeGenerator
from datetime import datetime, timedelta
from decimal import Decimal

bp = Blueprint('batch', __name__)

@bp.route('/')
def list_batches():
    """批次列表"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        search = request.args.get('search', '', type=str)
        product_id = request.args.get('product_id', None, type=int)
        supplier_id = request.args.get('supplier_id', None, type=int)
        
        query = Batch.query
        
        if search:
            query = query.filter(Batch.batch_no.ilike(f'%{search}%'))
        if product_id:
            query = query.filter_by(product_id=product_id)
        if supplier_id:
            query = query.filter_by(supplier_id=supplier_id)
        
        paginated = query.order_by(Batch.id.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        products = Product.query.all()
        suppliers = Supplier.query.all()
        
        return render_template(
            'batch/list.html',
            batches=paginated.items,
            pagination=paginated,
            products=products,
            suppliers=suppliers,
            search=search,
            per_page=per_page
        )
    except Exception as e:
        return render_template('error.html', error=str(e))

@bp.route('/create', methods=['GET', 'POST'])
def create_batch():
    """创建批次"""
    if request.method == 'POST':
        try:
            data = request.get_json()
            
            product_id = data.get('product_id')
            supplier_id = data.get('supplier_id')
            product = Product.query.get(product_id)
            supplier = Supplier.query.get(supplier_id)
            
            if not product or not supplier:
                return jsonify({'status': 'error', 'message': '产品或供应商不存在'}), 400
            
            production_date = datetime.strptime(data.get('production_date'), '%Y-%m-%d').date()
            expiry_date = production_date + timedelta(days=product.shelf_life)
            
            quantity = Decimal(str(data.get('quantity', 0)))
            unit_price = Decimal(str(data.get('unit_price', 0)))
            total_price = quantity * unit_price
            
            batch = Batch(
                batch_no=CodeGenerator.generate_batch_no(supplier.code, product.code),
                product_id=product_id,
                supplier_id=supplier_id,
                country=supplier.country,
                production_date=production_date,
                expiry_date=expiry_date,
                quantity=quantity,
                unit_price=unit_price,
                total_price=total_price
            )
            
            db.session.add(batch)
            db.session.commit()
            
            # 创建库存记录
            inventory = Inventory(
                product_id=product_id,
                batch_id=batch.id,
                current_quantity=quantity,
                unit_price=unit_price,
                amount=total_price
            )
            db.session.add(inventory)
            db.session.commit()
            
            return jsonify({
                'status': 'success',
                'message': '批次创建成功',
                'data': batch.to_dict()
            })
        except Exception as e:
            db.session.rollback()
            return jsonify({'status': 'error', 'message': str(e)}), 400
    
    products = Product.query.all()
    suppliers = Supplier.query.all()
    return render_template('batch/create.html', products=products, suppliers=suppliers)

@bp.route('/<int:batch_id>')
def view_batch(batch_id):
    """查看批次详情"""
    batch = Batch.query.get_or_404(batch_id)
    return render_template('batch/view.html', batch=batch)
