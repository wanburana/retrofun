from sqlalchemy import not_, select, func
from db import Session
from models import Country, Product, Manufacturer

session = Session()

# Products that were made in UK or USA.
# Easy way to remember: Join with its object, Product, Country.products
q = select(Product, Country.name).join(Country.products).where(Country.name.in_(['UK', 'USA'])).distinct()
print(q)
results = session.execute(q).all()
print(len(results), len(set(results)))
for item in results:
    print(item)

# Products not made in UK or USA. Products that were made in UK and/or USA jointly with other countries should be included in the query results.
# So basically products that are not exclusively made in UK or USA?
# Strategy: 
q = (
    select(Product)
    .join(Country.products)
    .where(not_(Country.name.in_(['UK', 'USA'])))
    .distinct()
)
print(q)
results = session.execute(q).all()
print(len(results))
print(len(results), len(set(results)))
for item in results:
    print(item)

# Countries with products based on the Z80 CPU or any of its clones.
q = (
    select(Country)
    .join(Product.countries)
    .where(Product.cpu.like("%Z80%"))
    .distinct()

)
print(q)
results = session.execute(q).all()
print(len(results))
print(len(results), len(set(results)))
for item in results:
    print(item)

# Countries that had products made in the 1970s in alphabetical order.
q = (
    select(Country)
    .join(Country.products)
    .where(Product.year.between(1970, 1979))
    .distinct()
    .order_by(Country.name)
)
print(q)
results = session.execute(q).all()
print(len(results), len(set(results)))
for item in results:
    print(item)

# The 5 countries with the most products. If there is a tie, the query should pick the countries in alphabetical order.
n_products = func.count(Product.id).label(None)
q = (
    select(Country, n_products)
    .join(Product.countries)
    .group_by(Country)
    .order_by(n_products.desc(), Country.name)
    .limit(5)
)
print(q)
results = session.execute(q).all()
print(len(results), len(set(results)))
for item in results:
    print(item)

# Manufacturers that have more than 3 products in UK or USA.
n_products = func.count(Product.id.distinct()).label(None)
q = (
    select(Manufacturer, n_products)
    .join(Manufacturer.products)
    .join(Product.countries)
    .where(Country.name.in_(['UK', 'USA']))
    .group_by(Manufacturer)
    .having(n_products > 3)
)
print(q)
results = session.execute(q).all()
print(len(results), len(set(results)))
for item in results:
    print(item)

# Manufacturers that have products in more than one country.
n_countries = func.count(Country.id.distinct()).label(None)
q = (
    select(Manufacturer, n_countries)
    .join(Manufacturer.products)
    .join(Product.countries)
    .group_by(Manufacturer)
    .having(n_countries >= 2)
)
print(q)
results = session.execute(q).all()
print(len(results), len(set(results)))
for item in results:
    print(item)

# Products made jointly in UK and USA.
q = (
    select(Product)
    .join(Country.products)
    .where(Country.name.in_(['UK', "USA"]))
    .group_by(Product)
    .having(func.count(Country.id.distinct()) == 2)
)
print(q)
results = session.execute(q).all()
print(len(results), len(set(results)))
for item in results:
    print(item)