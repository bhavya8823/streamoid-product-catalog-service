import csv
from typing import List, Dict, Any, Tuple
import io

REQUIRED_FIELDS = ['sku', 'name', 'brand', 'mrp', 'price']

def validate_field_presence(row: Dict[str, str]) -> bool:
    for field in REQUIRED_FIELDS:
        if not row.get(field) or not row[field].strip():
            return False
    return True

def parse_and_validate_csv(csv_file_stream: io.StringIO) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    valid_products = []
    failed_rows = []

    csv_file_stream.seek(0)
   
    reader = csv.DictReader(csv_file_stream)
    
    for row_number, raw_row in enumerate(reader, 1):
        row = {k.strip(): v.strip() for k, v in raw_row.items() if k is not None}
        errors = []

        if not validate_field_presence(row):
            errors.append("Missing required fields (sku, name, brand, mrp, price).")
        
        cleaned_data = {
            'sku': row.get('sku'),
            'name': row.get('name'),
            'brand': row.get('brand'),
            'color': row.get('color') or None, 
            'size': row.get('size') or None
        }
        
        try:
            mrp = float(row['mrp'])
            price = float(row['price'])
            
            quantity_str = row.get('quantity')
            if quantity_str and quantity_str.strip():
                quantity = int(quantity_str)
            else:
                quantity = 0
             
            if price > mrp:
                errors.append("Price must be less than or equal to MRP.")

            if quantity < 0:
                errors.append("Quantity cannot be negative.")
                
            cleaned_data.update({'mrp': mrp, 'price': price, 'quantity': quantity})
                
        except (ValueError, KeyError) as e:
            errors.append(f"Invalid numeric value for a price/quantity field. Error: {e}")
        
        if errors:
            failed_rows.append({
                "row_number": row_number,
                "row_data": dict(raw_row),
                "errors": errors
            })
        else:
            valid_products.append(cleaned_data)

    return valid_products, failed_rows