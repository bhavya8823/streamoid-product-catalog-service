from flask_sqlalchemy import SQLAlchemy # pyright: ignore[reportMissingImports]
from typing import Dict, Any

db = SQLAlchemy()

class Product(db.Model):
    sku = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    brand = db.Column(db.String(100), nullable=False)
    mrp = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    color = db.Column(db.String(50))
    size = db.Column(db.String(50))
    
    quantity = db.Column(db.Integer, nullable=True) 

    def to_dict(self) -> Dict[str, Any]:
        return {
            'sku': self.sku,
            'name': self.name,
            'brand': self.brand,
            'color': self.color,
            'size': self.size,
            'mrp': self.mrp,
            'price': self.price,
            'quantity': self.quantity
        }