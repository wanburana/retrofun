from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from sqlalchemy import ForeignKey, String, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship, WriteOnlyMapped
from db import Model


ProductCountry = Table(
    'products_countries',
    Model.metadata,
    Column('product_id', ForeignKey('products.id'), primary_key=True, nullable=False),
    Column('country_id', ForeignKey('countries.id'), primary_key=True, nullable=False),
)

class Product(Model):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), index=True, unique=True)
    manufacturer_id: Mapped[int] = mapped_column(
        ForeignKey('manufacturers.id'), index=True
    )
    year: Mapped[int] = mapped_column(index=True)
    cpu: Mapped[Optional[str]] = mapped_column(String(32))

    # A product has one manufacturer
    manufacturer: Mapped['Manufacturer'] = relationship(back_populates='products')
    countries: Mapped[list['Country']] = relationship(secondary=ProductCountry, back_populates='products')
    order_items: WriteOnlyMapped['OrderItem'] = relationship(back_populates='product')

    def __repr__(self):
        return f'Product({self.id}, "{self.name}")'

class Country(Model):
    __tablename__ = "countries"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32), index=True, unique=True)

    products: Mapped[list['Product']] = relationship(secondary=ProductCountry, back_populates='countries')

    def __repr__(self):
        return f'Country({self.id}, "{self.name}")'
    
class Manufacturer(Model):
    __tablename__ = "manufacturers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(64), index=True, unique=True)

    # A manufacturer has many products
    products: Mapped[list['Product']] = relationship(cascade='all, delete-orphan', back_populates='manufacturer')
    
    def __repr__(self):
        return f'Manufacturer({self.id}, "{self.name}")'



class Order(Model):
    __tablename__ = 'orders'

    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(default=datetime.utcnow,
                                                index=True)
    customer_id: Mapped[UUID] = mapped_column(ForeignKey('customers.id'),
                                                index=True)
    
    customer: Mapped['Customer'] = relationship(back_populates='orders')
    order_items: Mapped[list['OrderItem']] = relationship(back_populates='order')

    def __repr__(self):
        return f'Order({self.id.hex})'
class Customer(Model):
    __tablename__ = 'customers'

    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    name: Mapped[str] = mapped_column(String(64), index=True, unique=True)
    phone: Mapped[Optional[str]] = mapped_column(String(32))

    orders: WriteOnlyMapped['Order'] = relationship(back_populates='customer')

    def __repr__(self):
        return f'Customer({self.id.hex}, "{self.name}")'

class OrderItem(Model):
    __tablename__ = 'orders_items'

    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'),
                                            primary_key=True)
    order_id: Mapped[UUID] = mapped_column(ForeignKey('orders.id'),
                                            primary_key=True)
    unit_price: Mapped[float]
    quantity: Mapped[int]

    product: Mapped['Product'] = relationship(back_populates='order_items')
    order: Mapped['Order'] = relationship(back_populates='order_items')