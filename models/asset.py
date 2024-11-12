from database import db

class Asset(db.Model):
    __tablename__ = 'assets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True, index=True)
    price = db.Column(db.Float, nullable=False)
    asset_type = db.Column(db.String(20), nullable=False)  # Тип: 2D чи 3D
    available = db.Column(db.Boolean, default=True)

    def __init__(self, name, price, asset_type):
        self.name = name
        self.price = price
        self.asset_type = asset_type
