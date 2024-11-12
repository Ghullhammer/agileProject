from database import db

class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id'), nullable=False)
    status = db.Column(db.String(20), default="Pending")

    def __init__(self, buyer_id, asset_id):
        self.buyer_id = buyer_id
        self.asset_id = asset_id
        self.status = "Pending"

    def mark_completed(self):
        """
        Встановлює статус транзакції як 'Completed'.
        """
        self.status = "Completed"
