from .main import bp as main_bp
from .warehouse import bp as warehouse_bp
from .storage_area import bp as storage_area_bp
from .supplier import bp as supplier_bp
from .product import bp as product_bp
from .batch import bp as batch_bp
from .inbound import bp as inbound_bp
from .outbound import bp as outbound_bp
from .inventory import bp as inventory_bp
from .fee_management import bp as fee_management_bp
from .excel_import_export import bp as excel_bp

__all__ = [
    'main_bp',
    'warehouse_bp',
    'storage_area_bp',
    'supplier_bp',
    'product_bp',
    'batch_bp',
    'inbound_bp',
    'outbound_bp',
    'inventory_bp',
    'fee_management_bp',
    'excel_bp'
]
