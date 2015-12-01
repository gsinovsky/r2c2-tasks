# -*- coding: utf-8 -*-
import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, BigInteger
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship, backref

from db import Base, session
from utils import parse_datetime
class User(Base):
    """Modelo para usuario de Twitter"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    # id de este usuario
    user_id = Column(String, unique=True) # json: id

    screen_name = Column(String(200, convert_unicode=True), unique=True) # json

    # tweets que estamos tracking
    tweets = relationship('Tweet', backref='user')

    def __init__(self, *args, **kwargs):
        for k, w in kwargs.items():
            setattr(self, k, w)

    @classmethod
    def from_api(cls, user):
        payload = user.AsDict()
        payload['user_id'] = str(payload['id'])
        del payload['id']
        instance = cls(**payload)
        return instance

    @classmethod
    def get_or_create(cls, user):
        instance = User.query.filter(User.user_id==str(user.id)).first()
        if instance is not None:
            return instance
        instance = cls.from_api(user)
        session.add(instance)
        session.commit()
        return instance

    def __str__(self):
        return '@{}'.format(self.screen_name)



    __repr__ = __str__

class Tweet(Base):
    """Modelo de tweets."""
    __tablename__ = 'tweets'
    id = Column(Integer, primary_key=True, autoincrement=True)
    # fechas cuando publicaron el tweet y cuando lo jalamos
    created_at = Column(DateTime, default=datetime.datetime.now) # json
    # identificador del tweet en twitter
    tweet_id = Column(String(convert_unicode=True), unique=True) # json: id
    # contenido del tweet
    text = Column(String(150, convert_unicode=True))
    # usuario que publica
    user_id = Column(Integer, ForeignKey('users.id'))

    def __init__(self, *args, **kwargs):
        for k, w in kwargs.items():
            setattr(self, k, w)

    @classmethod
    def from_api(cls, tweet):
        payload = tweet.AsDict()
        payload['tweet_id'] = str(payload['id'])
        del payload['id']
        del payload['user']
        payload['user_id'] = User.get_or_create(tweet.user).id
        payload['created_at'] = parse_datetime(tweet)
        instance = cls(**payload)
        return instance

    @classmethod
    def create(cls, tweet):
        instance = cls.from_api(tweet)
        session.add(instance)
        session.commit()
        return instance

    def __str__(self):
        return u'{}\'s tweet #{}'.format(self.user, self.tweet_id)

    __repr__ = __str__