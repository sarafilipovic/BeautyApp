from __init__ import Base

from sqlalchemy import *


class Proizvod (Base):
    __tablename__ = "proizvod"
    ID_proizvoda = Column(Integer, primary_key = True)
    korisnik_id = Column(Integer,ForeignKey("korisnici.ID_korisnika", ondelete="CASCADE"))
    ime = Column(String(50))
    opis =Column(String(200))
    cijena=Column(Integer)
  