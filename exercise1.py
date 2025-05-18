from sqlalchemy import between, func, or_, select
from db import Model, Session
from models import Product

session = Session()

# The first three products in alphabetical order built in the year 1983.
q = select(Product).where(Product.year == 1983).order_by(Product.name).limit(3)
print(session.execute(q).all())


# Products that use the "Z80" CPU or any of its clones. Assume that all products based on this CPU have the word "Z80" in the cpu column.
q = select(Product).where(Product.cpu.like("%Z80%"))
print(session.execute(q).all())

# Products that use either the "Z80" or the "6502" CPUs, or any of its clones, built before 1990, sorted alphabetically by name.
q = (
    select(Product)
    .where(or_(Product.cpu.like("%Z80%"), Product.cpu.like("%6502%")))
    .where(Product.year < 1990)
    .order_by(Product.name)
)
print(session.execute(q).all())

# The manufacturers that built products in the 1980s.
q = (
    select(Product.manufacturer.distinct())
    .where(Product.year.between(1980, 1989))

)
print(session.execute(q).all())

# Manufacturers whose names start with the letter "T", sorted alphabetically.
q = (
    select(Product.manufacturer.distinct())
    .where(Product.manufacturer.like("T%"))
    .order_by(Product.manufacturer)

)
print(session.execute(q).all())

# The first and last years in which products have been built in Croatia, along with the number of products built.
q = (
    select(func.min(Product.year), func.max(Product.year), func.count())
    .group_by(Product.country)
    .having(Product.country == "Croatia")
)
print(session.execute(q).all())

# The number of products that were built each year. The results should start from the year with the most products, to the year with the least. Years in which no products were built do not need to be included.
q = (
    select(Product.year, func.count()).select_from(Product)
    .group_by(Product.year)
    .order_by(func.count().desc())
)
print(session.execute(q).all())

# The number of manufacturers in the United States (note that the country field for these products is set to USA)
q = (
    select(func.count(Product.manufacturer.distinct()))
    .where(Product.country == "USA")

)
print(session.execute(q).all())
