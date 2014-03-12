from sqlalchemy import Column, Integer, String, DateTime, create_engine, \
    ForeignKey
from sqlalchemy.orm import relationship, backref

from . import Base, JsonEncodable


class Subscriber(Base, JsonEncodable):
    __tablename__ = 'subscriber'

    id = Column(Integer, primary_key=True)
    email = Column(String)
    timestamp = Column(DateTime)

    def __repr__(self):
        return "<Subscriber(name='{}', email='{}', timestamp='{}')," + \
            " headers='{}'>".format(self.name, self.email, self.timestamp,
                                    self.headers)


class SubscriberHeader(Base, JsonEncodable):
    __tablename__ = 'subscribers_headers'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('subscriber.id'))
    key = Column(String)
    value = Column(String)

    user = relationship("Subscriber", backref=backref('headers', order_by=id))

    def __repr__(self):
        return "<SubscriberHeader(id='{}', user_id='{}', key='{}'," + \
            " value='{}'".format(self.id, self.user_id, self.key, self.value)
