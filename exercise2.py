from sqlalchemy import select, func
from db import Session
from models import Product, Manufacturer


session = Session()

# The list of products made by IBM and Texas Instruments.
q = select(Product).join(Product.manufacturer).where(Manufacturer.name.in_(["IBM", "Texas Instruments"]))

print(session.scalars(q).all())

# Manufacturers that operate in Brazil.
q = select(Manufacturer).join(Product.manufacturer).where(Product.country == "Brazil")
print(session.scalars(q).all())

# Products that have a manufacturer that has the word "Research" in their name.
q = select(Product, Manufacturer.name).join(Product.manufacturer).where(Manufacturer.name.like("%Research%"))
print(session.execute(q).all())

# Manufacturers that made products based on the Z80 CPU or any of its clones.
q = select(Manufacturer.name, Product.cpu).join(Product.manufacturer).where(Product.cpu.like("%Z80%"))
print(session.execute(q).all())

# Manufacturers that made products that are not based on the 6502 CPU or any of its clones.
q = select(Manufacturer.name, Product.cpu).join(Product.manufacturer).where(Product.cpu.not_like("%6502%"))
print(session.execute(q).all())

# Manufacturers and the year they went to market with their first product, sorted by the year
q = select(Manufacturer, func.min(Product.year)).join(Product).group_by(Manufacturer).order_by(func.min(Product.year))
print(session.execute(q).all())

# Manufacturers that have 3 to 5 products in the catalog.
q = select(Manufacturer, func.count(Product.id)).join(Product.manufacturer).group_by(Manufacturer).having(func.count(Product.id).between(3,5))
print(session.execute(q).all())

# Manufacturers that operated for more than 5 years.
operated_years = (func.max(Product.year) - func.min(Product.year)).label(None)
q = select(Manufacturer, operated_years).join(Product).group_by(Manufacturer).having(operated_years >= 5)
print(session.execute(q).all())