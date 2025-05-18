import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from db import Model
from models import Product
from sqlalchemy.orm import sessionmaker

engine = create_engine(os.environ['DATABASE_URL'])


Session = sessionmaker(engine)

c64 = Product(name='Commodore 64', manufacturer='Commodore', )
with Session() as session:
    with session.begin():
        session.add(c64)

    print(c64)