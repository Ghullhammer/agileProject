# services/purchase_service.py
from models.user import Buyer
from models.asset import Asset
from models.transaction import Transaction
from database import db

def purchase_asset(buyer_id, asset_id):
    buyer = Buyer.query.get(buyer_id)
    asset = Asset.query.get(asset_id)

    if not buyer:
        return {"status": "Buyer not found"}, 404
    if not asset or not asset.available:
        return {"status": "Asset not available"}, 400
    if buyer.balance < asset.price:
        return {"status": "Insufficient funds"}, 400

    transaction = Transaction(buyer_id=buyer.id, asset_id=asset.id)
    db.session.add(transaction)

    try:
        buyer.balance -= asset.price
        asset.available = False
        transaction.mark_completed()
        db.session.commit()
        return {"status": f"Asset '{asset.name}' purchased successfully"}, 201
    except Exception as e:
        db.session.rollback()
        return {"status": f"Database error: {str(e)}"}, 500
