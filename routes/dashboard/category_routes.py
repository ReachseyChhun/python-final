from flask import Blueprint, request, jsonify, render_template
from models import db, Category

category_bp = Blueprint('category', __name__, url_prefix='/dashboard/categories')

@category_bp.route('/')
def category():
    module = "category"
    return render_template('dashboard/category/category.html', module = module)

@category_bp.route('/', methods=['POST'])
def create_category():
    data = request.json
    try:
        category = Category(name=data['name'], description=data['description'])
        db.session.add(category)
        db.session.commit()
        return jsonify({"message": "Category created successfully", "id": category.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@category_bp.route('/list', methods=['GET'])
def get_all_categories():
    categories = Category.query.all()
    result = [{"id": cat.id, "name": cat.name, "description": cat.description} for cat in categories]
    return jsonify(result), 200

@category_bp.route('/<int:id>', methods=['GET'])
def get_category(id):
    category = Category.query.get(id)
    if not category:
        return jsonify({"message": "Category not found"}), 404
    return jsonify({"id": category.id, "name": category.name, "description": category.description}), 200

@category_bp.route('/<int:id>', methods=['PUT'])
def update_category(id):
    data = request.json
    category = Category.query.get(id)
    if not category:
        return jsonify({"message": "Category not found"}), 404
    try:
        category.name = data.get('name', category.name)
        category.description = data.get('description', category.description)
        db.session.commit()
        return jsonify({"message": "Category updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@category_bp.route('/<int:id>', methods=['DELETE'])
def delete_category(id):
    category = Category.query.get(id)
    if not category:
        return jsonify({"message": "Category not found"}), 404
    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": "Category deleted successfully"}), 200
