from flask import Blueprint, request, jsonify, render_template
from models import db, Unit

unit_bp = Blueprint('unit', __name__, url_prefix='/dashboard/units')

@unit_bp.route('/')
def unit():
    module = "unit"
    return render_template('dashboard/unit/unit.html', module = module)

@unit_bp.route('/', methods=['POST'])
def create_unit():
    data = request.json
    try:
        unit = Unit(name=data['name'], description=data['description'])
        db.session.add(unit)
        db.session.commit()
        return jsonify({"message": "Unit created successfully", "id": unit.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@unit_bp.route('/list', methods=['GET'])
def get_all_units():
    units = Unit.query.all()
    result = [{"id": u.id, "name": u.name, "description": u.description} for u in units]
    return jsonify(result), 200

@unit_bp.route('/<int:id>', methods=['GET'])
def get_unit(id):
    unit = Unit.query.get(id)
    if not unit:
        return jsonify({"message": "Unit not found"}), 404
    return jsonify({"id": unit.id, "name": unit.name, "description": unit.description}), 200

@unit_bp.route('/<int:id>', methods=['PUT'])
def update_unit(id):
    data = request.json
    unit = Unit.query.get(id)
    if not unit:
        return jsonify({"message": "Unit not found"}), 404
    try:
        unit.name = data.get('name', unit.name)
        unit.description = data.get('description', unit.description)
        db.session.commit()
        return jsonify({"message": "Unit updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@unit_bp.route('/<int:id>', methods=['DELETE'])
def delete_unit(id):
    unit = Unit.query.get(id)
    if not unit:
        return jsonify({"message": "Unit not found"}), 404
    db.session.delete(unit)
    db.session.commit()
    return jsonify({"message": "Unit deleted successfully"}), 200
