from models.asset import Asset
from models.transaction import Transaction
from database import db
class AssetService:
    @staticmethod
    def validate_asset_data(data):
        """
        Перевірка вхідних даних для активу.
        """
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
        """
        Додавання нового активу до бази даних.
        """
        # Викликаємо метод валідації
        validation_error = AssetService.validate_asset_data(data)
        if validation_error:
            return validation_error

        name = data.get("name")
        price = data.get("price")
        asset_type = data.get("asset_type")

        # Перевірка, чи існує актив з таким ім'ям
        if Asset.query.filter_by(name=name).first():
            return {"status": "Asset already exists"}, 400

        # Створюємо новий актив
        new_asset = Asset(
            name=name,
            price=price,
            asset_type=asset_type
        )
        db.session.add(new_asset)

        # Зберігаємо зміни в базу даних
        try:
            db.session.commit()
            return {"status": "Asset added successfully"}, 201
        except Exception as e:
            db.session.rollback()
            return {"status": f"Database error: {str(e)}"}, 500

    @staticmethod
    def update_asset(asset, data):
        """
        Оновлення існуючого активу.
        """
        validation_error = AssetService.validate_asset_data(data)
        if validation_error:
            return validation_error

        # Оновлюємо поля активу
        asset.price = data.get("price")
        asset.asset_type = data.get("asset_type")

        # Зберігаємо зміни
        try:
            db.session.commit()
            return {"status": "Asset updated successfully"}, 200
        except Exception as e:
            db.session.rollback()
            return {"status": f"Database error: {str(e)}"}, 500