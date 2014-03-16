from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Superclass for all model objects
Base = declarative_base()


# Superclass for all model objects
class JsonEncodable():
    """
    Superclass for making model classes json-encodable, ignoring sqlalchemy's
    extra attributes.
    """
    def to_json(self):
        d = self.__dict__.copy()
        del d["_sa_instance_state"]
        return d


def init_schema(db_string):
    engine = create_engine(db_string, echo=False)
    Session.configure(bind=engine)
    Base.metadata.create_all(engine)

Session = sessionmaker()

# Import all model classes and build the schema
from subscribers import Subscriber, SubscriberHeader

# Other exposed classes
from encoder import ModelEncoder
