from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()

class User(db.Model):
    user_id=db.Column(db.Integer(),primary_key=True,autoincrement=True)
    firstname=db.Column(db.String(60),nullable=False)
    lastname=db.Column(db.String(60),nullable=False)
    email=db.Column(db.String(128),unique=True,nullable=False)
    city=db.Column(db.String(300),nullable=True)
    password=db.Column(db.String(300),nullable=False)
    phone = db.Column(db.BigInteger(),unique=True,nullable=False)  #phone number should be unique
    address= db.Column(db.String(300),nullable=False)
    status=db.Column(db.String(300),nullable=True)
    username=db.Column(db.String(100),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)

class Admin(db.Model):
    admin_id= db.Column(db.Integer(),primary_key=True,autoincrement=True)
    email=db.Column(db.String(128),nullable=False)
    pwd=db.Column(db.String(300),nullable=True)

class Product(db.Model):
    product_id=db.Column(db.Integer(),primary_key=True,autoincrement=True)
    front_img=db.Column(db.String(300),nullable=False)
    back_img=db.Column(db.String(300),nullable=False)
    price=db.Column(db.Float())
    delprice=db.Column(db.Float())
    quantity=db.Column(db.Integer(),nullable=False)
    description=db.Column(db.String(300),nullable=False)
    seller_user_id=db.Column(db.Integer(),db.ForeignKey("user.user_id"),nullable=False)

class Cart(db.Model):
    cart_id=db.Column(db.Integer(),primary_key=True,autoincrement=True)
    price=db.Column(db.Float(),nullable=False)
    quantity=db.Column(db.Integer(),nullable=False)
    description=db.Column(db.String(300),nullable=False)
    img=db.Column(db.String(300),nullable=False)
    seller_id= db.Column(db.Integer(),nullable=False)
    user_id=db.Column(db.Integer(),db.ForeignKey("user.user_id"))
    goods_id=db.Column(db.Integer(),db.ForeignKey("product.product_id"))

class Category(db.Model):
    category_id=db.Column(db.Integer(), primary_key=True,autoincrement=True)
    category=db.Column(db.String(100),nullable=False)

class Job(db.Model):
    job_id=db.Column(db.Integer(), primary_key=True,autoincrement=True)
    job_title=db.Column(db.String(300),nullable=False)  
    job_state=db.Column(db.String(300),nullable=False)
    job_country=db.Column(db.String(300),nullable=False)
    salary_range=db.Column(db.String(300),nullable=False)
    employer=db.Column(db.String(300),nullable=False)
    working_hours=db.Column(db.String(300),nullable=False)
    job_link=db.Column(db.String(500),nullable=False)

class Adverts(db.Model):
    ads_id=db.Column(db.Integer(), primary_key=True,autoincrement=True)
    ads_company=db.Column(db.String(300),nullable=False)
    ads_cover = db.Column(db.String(100)) 
    ads_Link = db.Column(db.String(100))



class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    amount = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50))
    reference = db.Column(db.String(100))
    product_description = db.Column(db.String(500))  # To store comma-separated product names
    quantities = db.Column(db.String(500))  # To store comma-separated quantities
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(300), nullable=False)
    img = db.Column(db.String(300), nullable=False)
    shipment_status = db.Column(db.String(300), nullable=True)

    # Relationship to User model (if needed)
    user = db.relationship('User', backref='transactions', lazy=True)

