from flask import Blueprint, request, jsonify, render_template
from models import db, Product, Category, Brand, Tag, Unit

product_bp = Blueprint('product', __name__, url_prefix='/dashboard/products')

@product_bp.route('/')
def product():
    module = "product"
    return render_template('dashboard/product/product.html', module = module)

# Create a new product
@product_bp.route('/', methods=['POST'])
def create_product():
    data = request.json
    try:
        product = Product(
            name=data['name'],
            cost=data['cost'],
            price=data['price'],
            category_id=data['category_id'],
            unit_id=data['unit_id'],
            brand_id=data['brand_id'],
            tag_id=data['tag_id']
        )
        db.session.add(product)
        db.session.commit()
        return jsonify({"message": "Product created successfully", "product": product.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Get all products
@product_bp.route('list', methods=['GET'])
def get_products():
    # Query the products and include related categories, units, brands, and tags
    products = Product.query.all()

    # Prepare the result with the related names instead of IDs
    result = [
        {
            "id": product.id,
            "name": product.name,
            "cost": str(product.cost),
            "price": str(product.price),
            "category_name": product.category.name if product.category else None,
            "unit_name": product.unit.name if product.unit else None,
            "brand_name": product.brand.name if product.brand else None,
            "tag_name": product.tag.name if product.tag else None
        }
        for product in products
    ]

    return jsonify(result), 200

# Get a product by ID
@product_bp.route('/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"message": "Product not found"}), 404
    return jsonify({
        "id": product.id,
        "name": product.name,
        "cost": str(product.cost),
        "price": str(product.price),
        "category_id": product.category_id,
        "unit_id": product.unit_id,
        "brand_id": product.brand_id,
        "tag_id": product.tag_id
    }), 200

# Update a product
@product_bp.route('/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.json
    product = Product.query.get(id)
    if not product:
        return jsonify({"message": "Product not found"}), 404

    try:
        product.name = data.get('name', product.name)
        product.cost = data.get('cost', product.cost)
        product.price = data.get('price', product.price)
        product.category_id = data.get('category_id', product.category_id)
        product.unit_id = data.get('unit_id', product.unit_id)
        product.brand_id = data.get('brand_id', product.brand_id)
        product.tag_id = data.get('tag_id', product.tag_id)

        db.session.commit()
        return jsonify({"message": "Product updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Delete a product
@product_bp.route('/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"message": "Product not found"}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully"}), 200


# Get dropdown data for categories, units, brands, and tags
@product_bp.route('/getDropdownData', methods=['GET'])
def get_dropdown_data():
    dropdown_data = {
        "categories": [{"id": category.id, "name": category.name} for category in Category.query.all()],
        "units": [{"id": unit.id, "name": unit.name} for unit in Unit.query.all()],
        "brands": [{"id": brand.id, "name": brand.name} for brand in Brand.query.all()],
        "tags": [{"id": tag.id, "name": tag.name} for tag in Tag.query.all()],
    }
    return jsonify(dropdown_data)
