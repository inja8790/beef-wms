"""自动编码生成服务"""
from models import db, Warehouse, StorageArea, Supplier, Product, Batch
from datetime import datetime

class CodeGenerator:
    """自动编码生成器"""
    
    @staticmethod
    def generate_warehouse_code():
        """生成仓库编码 WH001, WH002, ..."""
        last_warehouse = Warehouse.query.order_by(Warehouse.id.desc()).first()
        if last_warehouse and last_warehouse.code:
            try:
                num = int(last_warehouse.code.replace('WH', '')) + 1
                return f'WH{num:03d}'
            except:
                pass
        return 'WH001'
    
    @staticmethod
    def generate_storage_area_code():
        """生成库区编码 SA001, SA002, ..."""
        last_area = StorageArea.query.order_by(StorageArea.id.desc()).first()
        if last_area and last_area.code:
            try:
                num = int(last_area.code.replace('SA', '')) + 1
                return f'SA{num:03d}'
            except:
                pass
        return 'SA001'
    
    @staticmethod
    def generate_supplier_code():
        """生成供应商编码 SUP001, SUP002, ..."""
        last_supplier = Supplier.query.order_by(Supplier.id.desc()).first()
        if last_supplier and last_supplier.code:
            try:
                num = int(last_supplier.code.replace('SUP', '')) + 1
                return f'SUP{num:03d}'
            except:
                pass
        return 'SUP001'
    
    @staticmethod
    def generate_product_code():
        """生成产品编码 PRO001, PRO002, ..."""
        last_product = Product.query.order_by(Product.id.desc()).first()
        if last_product and last_product.code:
            try:
                num = int(last_product.code.replace('PRO', '')) + 1
                return f'PRO{num:03d}'
            except:
                pass
        return 'PRO001'
    
    @staticmethod
    def generate_batch_no(supplier_code, product_code):
        """
        生成批次号
        规则: 供应商缩写+日期+流水号
        例如: SUP-20240105-001
        """
        if not supplier_code or len(supplier_code) < 3:
            supplier_code = 'SUP'
        
        supplier_abbr = supplier_code[:3]
        date_str = datetime.now().strftime('%Y%m%d')
        
        # 查询今天最后一个批次的流水号
        today_batches = Batch.query.filter(
            Batch.batch_no.like(f'{supplier_abbr}-{date_str}-%')
        ).all()
        
        seq = len(today_batches) + 1
        return f'{supplier_abbr}-{date_str}-{seq:03d}'
    
    @staticmethod
    def generate_inbound_no():
        """生成入库单号 RK+日期+流水号"""
        date_str = datetime.now().strftime('%Y%m%d')
        from models import Inbound
        
        today_inbounds = Inbound.query.filter(
            Inbound.inbound_no.like(f'RK{date_str}%')
        ).all()
        
        seq = len(today_inbounds) + 1
        return f'RK{date_str}{seq:04d}'
    
    @staticmethod
    def generate_outbound_no():
        """生成出库单号 CK+日期+流水号"""
        date_str = datetime.now().strftime('%Y%m%d')
        from models import Outbound
        
        today_outbounds = Outbound.query.filter(
            Outbound.outbound_no.like(f'CK{date_str}%')
        ).all()
        
        seq = len(today_outbounds) + 1
        return f'CK{date_str}{seq:04d}'
