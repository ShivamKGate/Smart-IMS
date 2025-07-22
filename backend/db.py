from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import os
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

# Database Models

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    products = relationship('Product', back_populates='category')

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    price = Column(Float, nullable=False)
    reorder_level = Column(Integer, nullable=False)
    category = relationship('Category', back_populates='products')
    inventory = relationship('Inventory', back_populates='product')

class Warehouse(Base):
    __tablename__ = 'warehouses'
    id = Column(Integer, primary_key=True)
    location = Column(String, nullable=False)
    inventory = relationship('Inventory', back_populates='warehouse')

class Inventory(Base):
    __tablename__ = 'inventory'
    product_id = Column(Integer, ForeignKey('products.id'), primary_key=True)
    warehouse_id = Column(Integer, ForeignKey('warehouses.id'), primary_key=True)
    quantity = Column(Integer, nullable=False)
    product = relationship('Product', back_populates='inventory')
    warehouse = relationship('Warehouse', back_populates='inventory')

class Supplier(Base):
    __tablename__ = 'suppliers'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    contact = Column(String, nullable=True)
