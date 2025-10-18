# Streamoid Product Catalog Service

Tech Stack
Backend Framework: Python (Flask)
Database: SQLite (using Flask-SQLAlchemy for ORM)
Data Handling: Python's built-in `csv` and `io` libraries

Setup and Running Instructions

1. Prerequisites
Must have Python 3.8+ installed on system.

2. Environment Setup

1.  Clone the repository

2.  Activate Virtual Environment:
    ```bash
    # For macOS/Linux
    source .venv/bin/activate
    # For Windows
    # .venv\Scripts\activate
    ```

3.  Install Dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the Application

Start the Flask development server in activated environment:

```bash
python app.py
```

API Documentation

1. CSV Upload and Validation
API: POST /upload
Sample Request: curl -X POST -F "file=@products.csv" http://localhost:8000/upload
Sample Response: {
  "failed": [],
  "stored": 20
}

2. List All Products
API: GET /products
Sample Request: curl "http://localhost:8000/products?page=1&limit=5"
Sample Response: {
  "page": 1,
  "pages": 4,
  "per_page": 5,
  "products": [
    {
      "brand": "CarryCo",
      "color": "Beige",
      "mrp": 899.0,
      "name": "Canvas Tote Bag",
      "price": 699.0,
      "quantity": 35,
      "size": "OneSize",
      "sku": "BAG-TOTE-BEI"
    },
    {
      "brand": "CarryCo",
      "color": "Brown",
      "mrp": 1199.0,
      "name": "Leather Belt",
      "price": 899.0,
      "quantity": 40,
      "size": "38",
      "sku": "BELT-BRN-38"
    },
    {
      "brand": "BloomWear",
      "color": "Pink",
      "mrp": 2499.0,
      "name": "Floral Summer Dress",
      "price": 2199.0,
      "quantity": 10,
      "size": "S",
      "sku": "DRESS-PNK-S"
    },
    {
      "brand": "BloomWear",
      "color": "Yellow",
      "mrp": 2499.0,
      "name": "Floral Summer Dress",
      "price": 1999.0,
      "quantity": 7,
      "size": "M",
      "sku": "DRESS-YLW-M"
    },
    {
      "brand": "SnugWear",
      "color": "Charcoal",
      "mrp": 2199.0,
      "name": "Cozy Hoodie",
      "price": 1799.0,
      "quantity": 11,
      "size": "XL",
      "sku": "HOODIE-CHR-XL"
    }
  ],
  "total": 20
}

3. Search and Filter Products
API: GET /products/search
Sample Request: curl "http://localhost:8000/products/search?brand=BloomWear&maxPrice=2500"
Sample Response: [
  {
    "brand": "BloomWear",
    "color": "Pink",
    "mrp": 2499.0,
    "name": "Floral Summer Dress",
    "price": 2199.0,
    "quantity": 10,
    "size": "S",
    "sku": "DRESS-PNK-S"
  },
  {
    "brand": "BloomWear",
    "color": "Yellow",
    "mrp": 2499.0,
    "name": "Floral Summer Dress",
    "price": 1999.0,
    "quantity": 7,
    "size": "M",
    "sku": "DRESS-YLW-M"
  }
]