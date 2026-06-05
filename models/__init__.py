from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import all models
from .warehouse import Warehouse
from .storage_area import StorageArea
from .supplier import Supplier
from .product import Product
from .batch import Batch
from .inbound import Inbound
from .outbound import Outbound
from .inventory import Inventory
from .fee_rule import FeeRule
from .fee_record import FeeRecord

__all__ = [
    'db',
    'Warehouse',
    'StorageArea',
    'Supplier',
    'Product',
    'Batch',
    'Inbound',
    'Outbound',
    'Inventory',
    'FeeRule',
    'FeeRecord'
]
