from .ext import db, UserMixin
from datetime import datetime

class Customers(db.Model, UserMixin):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String(100), nullable=False, unique=True, index=True)
    email = db.Column(db.String(200), nullable=False, unique=True, index=True)
    phone = db.Column(db.String(200), nullable=False, unique=False, index=True)
    profile_image = db.Column(db.String(500), nullable=True)
    date = db.Column(db.DateTime, default=datetime.now())
    password = db.Column(db.String(255),index=True)
    cart_list = db.relationship("CartList", backref="customers", lazy=True)
    payment_record = db.relationship("PaymentRecord", backref="customers", lazy=True)
    
    def __repr__(self):
        return "<Role %r>" % self.username

class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(100), nullable=False, unique=False, index=True)
    link = db.Column(db.String(255), nullable=False, unique=False, index=True)
    date = db.Column(db.DateTime, default=datetime.now())
    categoryproduct = db.relationship("CategoryProduct", backref="category", lazy=True)
    
class CategoryProduct(db.Model):
    __tablename__ = "categoryproduct"
    id = db.Column(db.Integer, primary_key=True, index=True)
    heading = db.Column(db.String(100), nullable=False, unique=False, index=True)
    description = db.Column(db.String(255), nullable=False, unique=False, index=True)
    img_url = db.Column(db.String(200), nullable=False, unique=False, index=True)
    info_url = db.Column(db.String(500), nullable=False, unique=False, index=True)
    price = db.Column(db.String(100))
    previous_price = db.Column(db.String(100))
    discount = db.Column(db.String(100))
    product = db.relationship("Product", backref="categoryproduct", lazy=True)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now())
    

class Product(db.Model):
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(100), nullable=False, unique=False, index=True)
    img_url = db.Column(db.String(200), nullable=False, unique=False, index=True)
    price = db.Column(db.String(100))
    previous_price = db.Column(db.String(100))
    discount = db.Column(db.String(100))
    product_status = db.Column(db.String(100))
    product_description = db.Column(db.String(10000))
    categoryProduct_id = db.Column(db.Integer, db.ForeignKey("categoryproduct.id"), nullable=True)
    
    
class Searched_Product(db.Model):
    __tablename__ = "searched_product"
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(500), nullable=False, unique=False, index=True)
    img_url = db.Column(db.String(200), nullable=False, unique=False, index=True)
    price = db.Column(db.String(100))
    previous_price = db.Column(db.String(100))
    discount = db.Column(db.String(100))
    product_status = db.Column(db.String(100))
    searched_title = db.Column(db.String(100))
    product_description = db.Column(db.String(10000))
    

class CartList(db.Model):
    __tablename__ = 'cartlist'
    id = db.Column(db.Integer, primary_key=True, index=True)
    product_name = db.Column(db.String(500), nullable=False, unique=False, index=True)
    price = db.Column(db.String(100), nullable=False, unique=False, index=True)
    image = db.Column(db.String(200), nullable=False, unique=False, index=True)
    customers_id = db.Column(
        db.Integer, db.ForeignKey("customers.id"), nullable=True
    )
    date = db.Column(db.DateTime, default=datetime.utcnow())
    
    
class PaymentRecord(db.Model):
    __tablename__ = "paymentrecord"
    id = db.Column(db.Integer, primary_key=True, index=True)
    product_name = db.Column(db.String(500), nullable=False, unique=False, index=True)
    price = db.Column(db.String(100), nullable=False, unique=False, index=True)
    payment_method = db.Column(db.String(100), nullable=False, unique=False, index=True)
    address =  db.Column(db.String(250), nullable=False, unique=False, index=True)
    date = db.Column(db.DateTime, default=datetime.utcnow())
    customer_id = db.Column(
        db.Integer, db.ForeignKey("customers.id")
    )
    