"""
进口牛肉贸易商 WMS 仓储管理系统
"""
import os
from flask import Flask, render_template, request, jsonify
from config import config
from models import db
from datetime import datetime

def create_app(config_name=None):
    """应用工厂"""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config.get(config_name, config['development']))
    
    # 初始化数据库
    db.init_app(app)
    
    # 创建上传文件夹
    os.makedirs(app.config.get('UPLOAD_FOLDER', 'uploads'), exist_ok=True)
    
    with app.app_context():
        # 创建数据库表
        db.create_all()
    
    # 注册蓝图
    register_blueprints(app)
    
    # 注册错误处理器
    register_error_handlers(app)
    
    # 注册上下文处理器
    register_context_processors(app)
    
    return app

def register_blueprints(app):
    """注册蓝图"""
    from routes import (
        warehouse_bp, storage_area_bp, supplier_bp, product_bp,
        batch_bp, inbound_bp, outbound_bp, inventory_bp,
        fee_management_bp, excel_bp, main_bp
    )
    
    app.register_blueprint(main_bp)
    app.register_blueprint(warehouse_bp, url_prefix='/warehouse')
    app.register_blueprint(storage_area_bp, url_prefix='/storage_area')
    app.register_blueprint(supplier_bp, url_prefix='/supplier')
    app.register_blueprint(product_bp, url_prefix='/product')
    app.register_blueprint(batch_bp, url_prefix='/batch')
    app.register_blueprint(inbound_bp, url_prefix='/inbound')
    app.register_blueprint(outbound_bp, url_prefix='/outbound')
    app.register_blueprint(inventory_bp, url_prefix='/inventory')
    app.register_blueprint(fee_management_bp, url_prefix='/fee_management')
    app.register_blueprint(excel_bp, url_prefix='/excel')

def register_error_handlers(app):
    """注册错误处理器"""
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': '页面未找到', 'code': 404}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': '服务器内部错误', 'code': 500}), 500

def register_context_processors(app):
    """注册上下文处理器"""
    
    @app.context_processor
    def inject_config():
        return {
            'app_name': '进口牛肉贸易商WMS',
            'app_version': '1.0.0',
            'current_year': datetime.now().year,
            'page_options': app.config.get('PAGE_OPTIONS', [10, 20, 50, 100])
        }

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
