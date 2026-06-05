"""Excel导入导出路由"""
from flask import Blueprint, render_template, request, jsonify, send_file
from services.excel_service import ExcelService
from datetime import datetime
import os

bp = Blueprint('excel', __name__)

@bp.route('/templates')
def templates():
    """导入模板页面"""
    template_types = list(ExcelService.TEMPLATES.keys())
    return render_template('excel/templates.html', template_types=template_types)

@bp.route('/download-template/<template_type>')
def download_template(template_type):
    """下载导入模板"""
    try:
        file = ExcelService.create_template(template_type)
        if file:
            filename = f'{template_type}_template_{datetime.now().strftime("%Y%m%d")}.xlsx'
            return send_file(
                file,
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                as_attachment=True,
                download_name=filename
            )
        return jsonify({'status': 'error', 'message': '模板不存在'}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@bp.route('/import', methods=['GET', 'POST'])
def import_data():
    """导入数据"""
    if request.method == 'POST':
        try:
            if 'file' not in request.files:
                return jsonify({'status': 'error', 'message': '未选择文件'}), 400
            
            file = request.files['file']
            data_type = request.form.get('data_type', 'warehouse')
            
            if file.filename == '':
                return jsonify({'status': 'error', 'message': '未选择文件'}), 400
            
            # 调用相应的导入服务
            if data_type == 'warehouse':
                result = ExcelService.import_warehouse(file)
            elif data_type == 'supplier':
                result = ExcelService.import_supplier(file)
            elif data_type == 'product':
                result = ExcelService.import_product(file)
            else:
                return jsonify({'status': 'error', 'message': '不支持的数据类型'}), 400
            
            return jsonify({
                'status': 'success',
                'message': f'导入完成: {result["success"]}成功, {result["error"]}失败',
                'data': result
            })
        except Exception as e:
            return jsonify({'status': 'error', 'message': str(e)}), 500
    
    data_types = {
        'warehouse': '仓库',
        'supplier': '供应商',
        'product': '产品'
    }
    
    return render_template('excel/import.html', data_types=data_types)
