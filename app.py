from flask import Flask, request, jsonify, make_response # pyright: ignore[reportMissingImports]
from database import db, Product
from validation import parse_and_validate_csv
from sqlalchemy.exc import IntegrityError # pyright: ignore[reportMissingImports]
import io

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///streamoid_products.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/upload', methods=['POST'])
def upload_csv():
    if 'file' not in request.files or not request.files['file'].filename.endswith('.csv'):
        return jsonify({"error": "No CSV file provided or invalid file type."}), 400

    csv_file = request.files['file']
    try:
        stream = io.StringIO(csv_file.stream.read().decode("utf-8"), newline=None)
    except UnicodeDecodeError:
        return jsonify({"error": "Failed to decode file. Ensure it is a valid UTF-8 CSV."}), 400

    valid_products_data, failed_rows = parse_and_validate_csv(stream)
    stored_count = 0
    
    try:
        for data in valid_products_data:
            product = Product(**data)
            db.session.merge(product)
            stored_count += 1
            
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback() 
        return jsonify({"error": "Database Integrity Error (e.g., duplicate SKU or missing required value)", "details": str(e)}), 500
    except Exception as e:
        db.session.rollback() 
        return jsonify({"error": "An unexpected database error occurred.", "details": str(e)}), 500

    return jsonify({
        "stored": stored_count,
        "failed": failed_rows
    })

@app.route('/products', methods=['GET'])
def list_products():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    
    if page < 1 or limit < 1:
        return jsonify({"error": "Page and limit must be positive integers."}), 400
    
    pagination = db.paginate(
        db.select(Product).order_by(Product.sku), 
        page=page, 
        per_page=limit,
        error_out=False
    )
    
    products_list = [product.to_dict() for product in pagination.items]
    
    return jsonify({
        "products": products_list,
        "page": pagination.page,
        "per_page": pagination.per_page,
        "total": pagination.total,
        "pages": pagination.pages
    })


@app.route('/products/search', methods=['GET'])
def search_products():
    brand_filter = request.args.get('brand')
    color_filter = request.args.get('color')
    min_price = request.args.get('minPrice', type=float)
    max_price = request.args.get('maxPrice', type=float)
    
    query = db.select(Product).order_by(Product.sku)
    
    if brand_filter:
        query = query.filter(Product.brand.ilike(f'%{brand_filter}%'))

    if color_filter:
        query = query.filter(Product.color.ilike(f'%{color_filter}%'))

    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
        
    products = db.session.execute(query).scalars().all()
    
    products_list = [product.to_dict() for product in products]
    
    return jsonify(products_list)

if __name__ == '__main__':
    print("Starting Streamoid Product Catalog Service on http://localhost:8000")
    app.run(debug=True, port=8000)