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

    # fechas cuando el usuario fue creado en twitter, cuando
    # registramos un tweet de el, y cuando registramos su ultimo tweet
    created_at = Column(DateTime, default=datetime.datetime.now) # json
    recorded_at = Column(DateTime, default=datetime.datetime.now)
    last_tweet_at = Column(DateTime, default=datetime.datetime.now)

    # id de este usuario
    user_id = Column(String, unique=True) # json: id

    # nombre del usuario y screenname
    name = Column(String(200, convert_unicode=True)) # json
    screen_name = Column(String(200, convert_unicode=True), unique=True) # json

    # descripcion (bio) del usuario
    # TODO: entities en el bio
    description = Column(String(convert_unicode=True)) # json

    # url personal del usuario
    url = Column(String(convert_unicode=True)) # json

    # localidad definida por el usuario
    location = Column(String(convert_unicode=True)) # json

    # idioma de este usuario
    lang = Column(String(50, convert_unicode=True)) # json

    # este usuario utiliza el profile default? (podria ayudar a saber
    # si el usuario es power user or something)
    default_profile = Column(Boolean) # json

    # cuenta protegida?
    protected = Column(Boolean) # json

    # cuenta verificada? (dolartoday!)
    verified = Column(Boolean) # json

    # cuenta con geo shit?
    geo_enabled = Column(Boolean) # json

    # algunas estadisticas para este usuario
    # numero de tweets favoriteados
    favourites_count = Column(Integer) # json
    # numero de followers
    followers_count = Column(Integer) # json
    # numero de gente que followea
    friends_count = Column(Integer) # json
    # a cuantas listas este usuario pertenece
    listed_count = Column(Integer) # json
    # numero de tweets
    statuses_count = Column(Integer) # json

    # json original del api
    json = Column(String(convert_unicode=True))

    # tweets que estamos tracking
    tweets = relationship('Tweet', backref='user')

    def __init__(self, *args, **kwargs):
        for k, w in kwargs.items():
            setattr(self, k, w)

    @classmethod
    def from_api(cls, user):
        payload = user.AsDict()
        payload['user_id'] = str(payload['id'])
        payload['created_at'] = parse_datetime(user)
        payload['json'] = user.AsJsonString()
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
    recorded_at = Column(DateTime, default=datetime.datetime.now)

    # identificador del tweet en twitter
    tweet_id = Column(String(convert_unicode=True), unique=True) # json: id

    # contenido del tweet
    text = Column(String(150, convert_unicode=True))

    # usuario que publica
    user_id = Column(Integer, ForeignKey('users.id'))

    # algunas estadisticas de este tweet
    retweet_count = Column(Integer, default=0)
    favorite_count = Column(Integer, default=0)

    # TODO: entities (hashtags, urls, mentions)

    # idioma del tweet (relevante para NLP)
    lang = Column(String(50, convert_unicode=True))

    # cliente usado
    source = Column(String(convert_unicode=True))

    # TODO: coordinates, place and geolocalization

    # json original del api
    json = Column(String(convert_unicode=True))

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
        payload['json'] = tweet.AsJsonString()
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
