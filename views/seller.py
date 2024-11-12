from flask import Blueprint, request, jsonify
from models.user import Seller
from database import db
from models.asset import Asset
from models.services.asset import AssetService
#from models.services.assert import AssetService
import datetime

seller_bp = Blueprint('seller', __name__)

# Отримуємо продавця по імені
def get_seller(username):
    return Seller.query.filter_by(username=username).first()


MIN_WITHDRAWAL_AMOUNT = 10  # мінімальна сума для виводу коштів

class WithdrawFunds:
    def __init__(self, seller, amount):
        self.seller = seller
        self.amount = amount
        self.withdrawal_record = None

    def is_valid_amount(self):
        return self.amount >= MIN_WITHDRAWAL_AMOUNT

    def has_sufficient_funds(self):
        return self.seller.balance >= self.amount

    def log_operation(self):
        self.withdrawal_record = {
            "amount": self.amount,
            "timestamp": datetime.datetime.utcnow(),
            "seller_id": self.seller.id
        }

    def execute(self):
        if not self.is_valid_amount():
            return jsonify({"status": f"Minimum withdrawal amount is {MIN_WITHDRAWAL_AMOUNT}"}), 400

        if not self.has_sufficient_funds():
            return jsonify({"status": "Insufficient funds"}), 400

        self.log_operation()

        # Виконуємо зняття коштів
        self.seller.balance -= self.amount
        db.session.commit()

        return jsonify({
            "status": "Funds withdrawn",
            "remaining_balance": self.seller.balance,
            "withdrawal_amount": self.amount,
            "withdrawal_timestamp": self.withdrawal_record["timestamp"].isoformat()
        })

@seller_bp.route('/add_asset', methods=['POST'])
def add_asset_to_catalog():
    data = request.json
    seller = Seller("seller_user")

    # Використовуємо AssetService для валідації даних
    validation_error = AssetService.validate_asset_data(data)
    if validation_error:
        return jsonify(validation_error), 400

    # Додаємо актив через метод Seller
    response, status_code = seller.add_asset_to_catalog(data)
    return jsonify(response), status_code

@seller_bp.route('/update_asset', methods=['POST'])
def update_asset():
    data = request.json
    seller = Seller("seller_user")

    # Додаємо або оновлюємо актив через метод Seller
    response, status_code = seller.update_asset(data)
    return jsonify(response), status_code


@seller_bp.route('/withdraw', methods=['POST'])
def withdraw_funds():
    # отримуємо суму для виводу
    data = request.get_json()
    amount = data.get("amount")

    if amount is None or amount <= 0:
        return jsonify({"status": "Invalid amount"}), 400

    # Завантажуємо користувача з бази даних
    seller = Seller.query.filter_by(username="seller_user").first()

    # Перевірка, чи користувач існує в базі
    if not seller:
        return jsonify({"status": "Seller not found"}), 404

    withdrawal = WithdrawFunds(seller, amount)
    return withdrawal.execute()
