from __init__ import Base
from sqlalchemy import *


class Studio (Base):
    __tablename__ = "studio"
    ID_studio = Column(Integer, primary_key = True)
    ime = Column(String(50))
    adresa =Column(String(50))
    kontakt = Column(Integer)