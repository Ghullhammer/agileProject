from models.asset import Asset
from database import db

class AssetService:
    @staticmethod
    def validate_asset_data(data):
        name = data.get("name")
        price = data.get("price")
        asset_type = data.get("asset_type")

        if not name:
            return {"status": "Missing 'name' field"}, 400
        if not price or type(price) not in [int, float] or price <= 0:
            return {"status": "Invalid price value"}, 400
        if not asset_type or asset_type not in ['2D', '3D']:
            return {"status": "Invalid asset type"}, 400

        return None


    @staticmethod
    def add_asset(data):
        # Extract Method: винесли валідацію в окремий метод
        validation_error = AssetService.validate_asset_data(data)
        if validation_error:
            return validation_error

        # Replace Temp with Query: замінили тимчасові змінні на запити
        if Asset.query.filter_by(name=data.get("name")).first():
            return {"status": "Asset already exists"}, 400

        # Додаємо новий актив
        new_asset = Asset(
            name=data.get("name"),
            price=data.get("price"),
            asset_type=data.get("asset_type")
        )
        db.session.add(new_asset)

        try:
            db.session.commit()
            return {"status": "Asset added successfully"}, 201
        except Exception as e:
            db.session.rollback()
            return {"status": f"Database error: {str(e)}"}, 500
