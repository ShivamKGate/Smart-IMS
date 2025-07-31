from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import os
from dotenv import load_dotenv
import urllib.parse

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

# sqlalchemy engine and session setup
DB_HOST = os.getenv('DB_HOST', '').strip('"\'')
DB_PORT = os.getenv('DB_PORT', '').strip('"\'')
DB_NAME = os.getenv('DB_NAME', '').strip('"\'')
DB_USER = os.getenv('DB_USER', '').strip('"\'')
DB_PASSWORD = urllib.parse.quote(os.getenv('DB_PASSWORD', '').strip('"\''))

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# printing url for debugging
print("DATABASE_URL:", DATABASE_URL)

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# creating the tables in the database
def create_tables():
    Base.metadata.create_all(bind=engine)
