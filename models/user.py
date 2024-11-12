from database import db
from models.asset import Asset
from models.services.asset import AssetService

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    user_type = db.Column(db.String(20), nullable=False)
    balance = db.Column(db.Float, default=200.0)

    def __init__(self, username, user_type):
        self.username = username
        self.user_type = user_type

class Admin(User):
    def __init__(self, username):
        super().__init__(username, user_type="Admin")

class Buyer(User):
    def __init__(self, username):
        super().__init__(username, user_type="Buyer")

class Seller(User):
    def __init__(self, username):
        super().__init__(username, user_type="Seller")

    def add_asset_to_catalog(self, data):
        # Використовуємо AssetService для додавання активу
        return AssetService.add_asset(data)

    def update_asset(self, data):
        # Валідація даних через AssetService
        validation_error = AssetService.validate_asset_data(data)
        if validation_error:
            return validation_error

        name = data.get("name")
        price = data.get("price")
        asset_type = data.get("asset_type")

        # Перевірка, чи існує актив
        asset = Asset.query.filter_by(name=name).first()
        if asset:
            # Оновлюємо актив
            asset.price = price
            asset.asset_type = asset_type
            db.session.commit()
            return {"status": "Asset updated successfully"}, 200
        else:
            # Додаємо новий актив через AssetService
            return AssetService.add_asset(data)
