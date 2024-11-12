from flask import Blueprint, request, jsonify
from models.services.purchase_service import purchase_asset

buyer_bp = Blueprint('buyer', __name__)

@buyer_bp.route('/purchase/<int:asset_id>', methods=['POST'])
def purchase_asset_route(asset_id):
    data = request.json
    buyer_id = data.get("buyer_id")

    if not buyer_id:
        return jsonify({"status": "Missing buyer_id"}), 400

    response, status_code = purchase_asset(buyer_id, asset_id)
    return jsonify(response), status_code
