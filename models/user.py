from database import db
from models.asset import Asset



class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    user_type = db.Column(db.String(20), nullable=False)

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

    def add_asset_to_catalog(self, name, price, asset_type):
        # Перевірка, чи існує вже актив з таким ім'ям
        if Asset.query.filter_by(name=name).first():
            return {"status": "Asset already exists"}, 400

        new_asset = Asset(name=name, price=price, asset_type=asset_type)
        db.session.add(new_asset)
        db.session.commit()
        return {"status": "Asset added successfully"}, 201