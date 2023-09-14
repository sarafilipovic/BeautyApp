from __init__ import Base

from sqlalchemy import *


class Recenzija (Base):
    __tablename__ = "recenzije"
    ID_recenzije = Column(Integer, primary_key = True)
    korisnik_id = Column(Integer,ForeignKey("korisnici.ID_korisnika"))
    komentar = Column(String(100))
    ocjena = Column(Integer)
    