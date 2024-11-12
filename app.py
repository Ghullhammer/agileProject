# app.py

from flask import Flask
from database import db  # Імпортуємо db із database.py

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///marketplace.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Ініціалізація SQLAlchemy з Flask застосунком
db.init_app(app)

# Імпорт моделей ПІСЛЯ ініціалізації застосунку
with app.app_context():
    from models.user import Admin, Buyer, Seller
    from models.asset import Asset
    from models.transaction import Transaction
    
    db.create_all()

    # Додаємо початкові дані для тестування
    if not Admin.query.filter_by(username="admin_user").first():
        admin = Admin(username="admin_user")
        db.session.add(admin)
        
    if not Buyer.query.filter_by(username="buyer_user").first():
        buyer = Buyer(username="buyer_user")
        db.session.add(buyer)
        
    if not Seller.query.filter_by(username="seller_user").first():
        seller = Seller(username="seller_user")
        db.session.add(seller)
        
    if not Asset.query.filter_by(name="Example Asset").first():
        asset = Asset(name="Example Asset", price=100, asset_type="2D")
        db.session.add(asset)
        
    db.session.commit()

# Імпорт та реєстрація Blueprint-ів після ініціалізації моделей
from views.admin import admin_bp
from views.buyer import buyer_bp
from views.seller import seller_bp

app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(buyer_bp, url_prefix='/buyer')
app.register_blueprint(seller_bp, url_prefix='/seller')


if __name__ == '__main__':
    app.run(debug=True)
