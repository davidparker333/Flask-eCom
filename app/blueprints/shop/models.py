from app import db
import datetime

class Cart(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    products = db.relationship('Product', backref='cart')

    def __init__(self, user_id):
        self.user_id = user_id

    def __repr__(self):
        return f'Cart | {self.id} object'


class Product(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'))
    sku = db.Column(db.String(15), nullable=False)
    amount = db.Column(db.Numeric(5,2), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=False)

    def __init__(self, sku, amount, name, description, image):
        self.sku = sku
        self.amount = amount
        self.name = name
        self.description = description
        self.image = image

    def __repr__(self):
        return f'Product | {self.name} object'