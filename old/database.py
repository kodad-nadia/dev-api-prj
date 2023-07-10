from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'postgres://nadia:f5yLV6vAF5BNjPe8b1Ok27R97ziKIt5m@dpg-ci8rn6dgkuvmfnsaagmg-a/shop_wise'

# equivalent à un "connect"
database_engine = create_engine(DATABASE_URL)
# equivalent à un "cursor"
SessionTemplate = sessionmaker(
    bind=database_engine, autocommit=False, autoflush=False)


def get_cursor():
    db = SessionTemplate()
    try:
        yield db
    finally:
        db.close()