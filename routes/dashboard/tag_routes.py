from flask import Blueprint, request, jsonify, render_template
from models import db, Tag

tag_bp = Blueprint('tag', __name__, url_prefix='/dashboard/tags')


@tag_bp.route('/')
def tag():
    module = "tag"
    return render_template('dashboard/tag/tag.html', module = module)

# Create a new Tag
@tag_bp.route('/', methods=['POST'])
def create_tag():
    data = request.json
    try:
        tag = Tag(name=data['name'], description=data['description'])
        db.session.add(tag)
        db.session.commit()
        return jsonify({"message": "Tag created successfully", "id": tag.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Get all Tags
@tag_bp.route('/list', methods=['GET'])
def get_all_tags():
    tags = Tag.query.all()
    result = [{"id": tag.id, "name": tag.name, "description": tag.description} for tag in tags]
    return jsonify(result), 200

# Get a single Tag by ID
@tag_bp.route('/<int:id>', methods=['GET'])
def get_tag(id):
    tag = Tag.query.get(id)
    if not tag:
        return jsonify({"message": "Tag not found"}), 404
    return jsonify({"id": tag.id, "name": tag.name, "description": tag.description}), 200

# Update a Tag by ID
@tag_bp.route('/<int:id>', methods=['PUT'])
def update_tag(id):
    data = request.json
    tag = Tag.query.get(id)
    if not tag:
        return jsonify({"message": "Tag not found"}), 404
    try:
        tag.name = data.get('name', tag.name)
        tag.description = data.get('description', tag.description)
        db.session.commit()
        return jsonify({"message": "Tag updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Delete a Tag by ID
@tag_bp.route('/<int:id>', methods=['DELETE'])
def delete_tag(id):
    tag = Tag.query.get(id)
    if not tag:
        return jsonify({"message": "Tag not found"}), 404
    db.session.delete(tag)
    db.session.commit()
    return jsonify({"message": "Tag deleted successfully"}), 200