import pytest
from app import app, db
from models.user import Admin, Buyer, Seller
from models.asset import Asset
from models.transaction import Transaction

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Додаємо початкові дані для тестування
            admin = Admin(username="admin_user")
            buyer = Buyer(username="buyer_user")
            seller = Seller(username="seller_user")
            asset = Asset(name="Example Asset", price=100, asset_type="2D")
            
            db.session.add_all([admin, buyer, seller, asset])
            db.session.commit()
        yield client

def test_admin_view_complaints(client):
    response = client.get('/admin/complaints')
    assert response.status_code == 200

def test_buyer_purchase_asset(client):
    response = client.post('/buyer/purchase/1')
    assert response.status_code == 200
    assert b"Asset Example Asset purchased" in response.data

def test_seller_add_to_catalog(client):
    response = client.post('/seller/add', json={"name": "New Asset", "price": 200, "asset_type": "3D"})
    assert response.status_code == 200
    assert b"Asset added to catalog" in response.data
