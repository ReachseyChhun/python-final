from . import db

class Unit(db.Model):
    __tablename__ = 'unit'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))

    products = db.relationship('Product', back_populates='unit')
