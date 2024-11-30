from flask import Blueprint, request, jsonify, render_template
from models import db, Brand

brand_bp = Blueprint('brand', __name__, url_prefix='/dashboard/brands')

@brand_bp.route('/')
def brand():
    module = "brand"
    return render_template('dashboard/brand/brand.html', module = module)

# Create a new Brand
@brand_bp.route('/', methods=['POST'])
def create_brand():
    data = request.json
    try:
        brand = Brand(name=data['name'], description=data['description'])
        db.session.add(brand)
        db.session.commit()
        return jsonify({"message": "Brand created successfully", "id": brand.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Get all Brands
@brand_bp.route('/list', methods=['GET'])
def get_all_brands():
    brands = Brand.query.all()
    result = [{"id": brand.id, "name": brand.name, "description": brand.description} for brand in brands]
    return jsonify(result), 200

# Get a single Brand by ID
@brand_bp.route('/<int:id>', methods=['GET'])
def get_brand(id):
    brand = Brand.query.get(id)
    if not brand:
        return jsonify({"message": "Brand not found"}), 404
    return jsonify({"id": brand.id, "name": brand.name, "description": brand.description}), 200

# Update a Brand by ID
@brand_bp.route('/<int:id>', methods=['PUT'])
def update_brand(id):
    data = request.json
    brand = Brand.query.get(id)
    if not brand:
        return jsonify({"message": "Brand not found"}), 404
    try:
        brand.name = data.get('name', brand.name)
        brand.description = data.get('description', brand.description)
        db.session.commit()
        return jsonify({"message": "Brand updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Delete a Brand by ID
@brand_bp.route('/<int:id>', methods=['DELETE'])
def delete_brand(id):
    brand = Brand.query.get(id)
    if not brand:
        return jsonify({"message": "Brand not found"}), 404
    db.session.delete(brand)
    db.session.commit()
    return jsonify({"message": "Brand deleted successfully"}), 200
