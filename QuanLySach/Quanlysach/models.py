from sqlalchemy import Column, Integer, String, Float, Enum, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from Quanlysach import db
from datetime import datetime
from flask_login import UserMixin
from enum import Enum as UserEnum

class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)

class UserRole(UserEnum):
    ADMIN = 1
    USER = 2
    NGUOIQUANLYKHO = 3
    # NGUOIQUANLY = 4
    # NHANVIENBAN = 5


class User(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    username =Column(String(50), nullable=False, unique= True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100))
    email = Column(String(50))
    active = Column(Boolean, default=True)
    joined_date = Column(DateTime, default=datetime.now())
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    receipts = relationship('Receipt', backref='user', lazy=True)
    comments = relationship('Comment', backref='user', lazy=True)

    def __str__(self):
        return self.name


class Category(BaseModel):
    __tablename__ ='category'

    name = Column(String(20), nullable=False)
    products = relationship('Product', backref='category', lazy=False)

    def __str__(self):
        return self.name


class Product(BaseModel):
    __tablename__ = 'product'

    name = Column(String(50), nullable=False)
    description = Column(String(255))
    price = Column(Float, default=0)
    image = Column(String(100))
    active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.now())
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    receipt_details = relationship('ReceiptDetail', backref='product', lazy=True)
    comments = relationship('Comment', backref='product', lazy=True)
    book_entry = relationship('Book_Entry', backref='product', lazy=True)

    def __str__(self):
        return self.name


class Book_Entry(Product):
    quantity = Column(Integer, default=0)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False, primary_key=True)



class Comment(BaseModel):
    content = Column(String(255), nullable=False)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    created_date = Column(DateTime, default=datetime.now())

    def __str__(self):
        return self.content

class Receipt(BaseModel):
    __tablename__ = 'receipt'

    created_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    details = relationship('ReceiptDetail', backref='receipt', lazy=True)




class ReceiptDetail(db.Model):
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False, primary_key=True)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False, primary_key=True)
    quantity = Column(Integer, default=0)
    unit_price = Column(Float, default=0)



class change_rule(BaseModel):
    content = Column(String(255), nullable=False)



if __name__ == '__main__':
     db.create_all()


