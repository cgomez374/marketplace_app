from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# FOR FUTURE IMPLEMENTATION: SALES HISTORY FOR EACH MERCHANT


class Merchant(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=False, nullable=False)
    email = db.Column(db.String(100), index=True, unique=False, nullable=False)
    hashed_password = db.Column(db.String(100), index=False, unique=False)
    date_joined = db.Column(db.DateTime, index=False, unique=False)
    products = db.relationship('Product', backref='seller', lazy='dynamic', cascade="all, delete-orphan")

    # SET PASSWORD
    def set_password(self, new_password):
        self.hashed_password = generate_password_hash(new_password, method='pbkdf2:sha256', salt_length=8)

    # CHECK_PASSWORD
    def check_password(self, password_to_check):
        return check_password_hash(pwhash=self.hashed_password, password=password_to_check)


# NEED TO FIGURE OUT HOW TO UPLOAD AND SAVE IMAGES
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=False, nullable=False)
    description = db.Column(db.String(500), index=False, unique=False, nullable=False)
    price = db.Column(db.Integer, index=False, unique=False, nullable=False)
    category = db.Column(db.String(100), index=False, unique=False, nullable=False)
    img_url = db.Column(db.String(300), index=False, unique=True, nullable=False)
    merchant_id = db.Column(db.Integer, db.ForeignKey('merchant.id'))
