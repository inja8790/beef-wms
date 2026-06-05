"""Excel 导入导出服务"""
import pandas as pd
import io
from datetime import datetime
from decimal import Decimal
from models import (
    db, Warehouse, StorageArea, Supplier, Product, Batch, 
    Inbound, Outbound, Inventory
)
from services.auto_code_generator import CodeGenerator

class ExcelService:
    """Excel 导入导出服务"""
    
    # 模板字段定义
    TEMPLATES = {
        'warehouse': {
            'columns': ['仓库名称', '备注'],
            'description': '仓库导入模板'
        },
        'storage_area': {
            'columns': ['所属仓库', '库区名称'],
            'description': '库区导入模板'
        },
        'supplier': {
            'columns': ['供应商名称', '原产国', '联系人', '电话'],
            'description': '供应商导入模板'
        },
        'product': {
            'columns': ['产品名称', '规格', '保质期(天数)', '默认单价'],
            'description': '产品导入模板'
        },
        'batch': {
            'columns': ['供应商编码', '产品编码', '生产日期', '数量', '单价'],
            'description': '批次导入模板'
        }
    }
    
    @staticmethod
    def create_template(template_type):
        """创建导入模板"""
        if template_type not in ExcelService.TEMPLATES:
            return None
        
        template = ExcelService.TEMPLATES[template_type]
        df = pd.DataFrame(columns=template['columns'])
        
        output = io.BytesIO()
        df.to_excel(output, index=False, sheet_name='数据')
        output.seek(0)
        return output
    
    @staticmethod
    def import_warehouse(file):
        """导入仓库数据"""
        try:
            df = pd.read_excel(file)
            results = {'success': 0, 'error': 0, 'errors': []}
            
            for idx, row in df.iterrows():
                try:
                    if pd.isna(row['仓库名称']):
                        results['errors'].append(f'第{idx+2}行: 仓库名称不能为空')
                        continue
                    
                    warehouse = Warehouse(
                        code=CodeGenerator.generate_warehouse_code(),
                        name=str(row['仓库名称']).strip(),
                        remarks=str(row.get('备注', '')) if pd.notna(row.get('备注')) else None
                    )
                    db.session.add(warehouse)
                    results['success'] += 1
                except Exception as e:
                    results['errors'].append(f'第{idx+2}行: {str(e)}')
                    results['error'] += 1
            
            db.session.commit()
            return results
        except Exception as e:
            return {'success': 0, 'error': 1, 'errors': [str(e)]}
    
    @staticmethod
    def import_supplier(file):
        """导入供应商数据"""
        try:
            df = pd.read_excel(file)
            results = {'success': 0, 'error': 0, 'errors': []}
            
            for idx, row in df.iterrows():
                try:
                    if pd.isna(row['供应商名称']):
                        results['errors'].append(f'第{idx+2}行: 供应商名称不能为空')
                        continue
                    if pd.isna(row['原产国']):
                        results['errors'].append(f'第{idx+2}行: 原产国不能为空')
                        continue
                    
                    supplier = Supplier(
                        code=CodeGenerator.generate_supplier_code(),
                        name=str(row['供应商名称']).strip(),
                        country=str(row['原产国']).strip(),
                        contact=str(row.get('联系人', '')) if pd.notna(row.get('联系人')) else None,
                        phone=str(row.get('电话', '')) if pd.notna(row.get('电话')) else None
                    )
                    db.session.add(supplier)
                    results['success'] += 1
                except Exception as e:
                    results['errors'].append(f'第{idx+2}行: {str(e)}')
                    results['error'] += 1
            
            db.session.commit()
            return results
        except Exception as e:
            return {'success': 0, 'error': 1, 'errors': [str(e)]}
    
    @staticmethod
    def import_product(file):
        """导入产品数据"""
        try:
            df = pd.read_excel(file)
            results = {'success': 0, 'error': 0, 'errors': []}
            
            for idx, row in df.iterrows():
                try:
                    if pd.isna(row['产品名称']):
                        results['errors'].append(f'第{idx+2}行: 产品名称不能为空')
                        continue
                    if pd.isna(row['保质期(天数)']):
                        results['errors'].append(f'第{idx+2}行: 保质期不能为空')
                        continue
                    
                    product = Product(
                        code=CodeGenerator.generate_product_code(),
                        name=str(row['产品名称']).strip(),
                        spec=str(row.get('规格', '')) if pd.notna(row.get('规格')) else None,
                        shelf_life=int(row['保质期(天数)']),
                        default_price=Decimal(str(row.get('默认单价', 0))) if pd.notna(row.get('默认单价')) else Decimal(0)
                    )
                    db.session.add(product)
                    results['success'] += 1
                except Exception as e:
                    results['errors'].append(f'第{idx+2}行: {str(e)}')
                    results['error'] += 1
            
            db.session.commit()
            return results
        except Exception as e:
            return {'success': 0, 'error': 1, 'errors': [str(e)]}
    
    @staticmethod
    def export_data(model, data_list):
        """导出数据为Excel"""
        try:
            df = pd.DataFrame([item.to_dict() if hasattr(item, 'to_dict') else item for item in data_list])
            output = io.BytesIO()
            df.to_excel(output, index=False)
            output.seek(0)
            return output
        except Exception as e:
            raise Exception(f'导出失败: {str(e)}')
    
    @staticmethod
    def validate_import_data(data, template_type):
        """验证导入数据"""
        errors = []
        required_fields = ExcelService.TEMPLATES.get(template_type, {}).get('columns', [])
        
        if not isinstance(data, pd.DataFrame):
            return ['数据格式错误']
        
        # 检查必需的列
        for field in required_fields:
            if field not in data.columns:
                errors.append(f'缺少必需列: {field}')
        
        return errors
