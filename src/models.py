from src import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Float, default=0.0)
    reserved = db.Column(db.Boolean, default=False)
    sold = db.Column(db.Boolean, default=False)
    category_id = db.Column(
        db.Integer, db.ForeignKey('category.id'), nullable=False
    )
    category = db.relationship('Category', backref='products')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'category_id': self.category_id,
            'discount': self.discount,
            'reserved': self.reserved,
            'sold': self.sold
        }
