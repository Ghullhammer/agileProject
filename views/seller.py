from flask import Blueprint, request, jsonify
from models.user import Seller
from database import db

seller_bp = Blueprint('seller', __name__)
seller = Seller("seller_user")

@seller_bp.route('/add_asset', methods=['POST'])
def add_asset_to_catalog():
    data = request.json
    name = data.get("name")
    price = data.get("price")
    asset_type = data.get("asset_type")

    if not all([name, price, asset_type]):
        return jsonify({"status": "Invalid input"}), 400

    response, status_code = seller.add_asset_to_catalog(name, price, asset_type)
    return jsonify(response), status_code
