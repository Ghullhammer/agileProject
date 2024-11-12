from flask import Blueprint, jsonify
from database import db
from models.user import Buyer
from models.asset import Asset
from models.transaction import Transaction

buyer_bp = Blueprint('buyer', __name__)

@buyer_bp.route('/purchase/<int:asset_id>', methods=['POST'])
def purchase_asset(asset_id):
    asset = Asset.query.get(asset_id)
    if asset and asset.available:
        transaction = Transaction(buyer_id=1, asset_id=asset.id)
        db.session.add(transaction)
        asset.available = False
        transaction.status = "Completed"
        db.session.commit()
        return jsonify({"status": f"Asset {asset.name} purchased"})
    else:
        return jsonify({"status": "Asset not available"}), 400
