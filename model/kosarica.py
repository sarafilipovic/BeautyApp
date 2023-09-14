from __init__ import Base

from sqlalchemy import *


class Kosarica (Base):
    __tablename__ = "kosarica"
    ID_kosarice = Column(Integer, primary_key = True)
    korisnik_id = Column(Integer,ForeignKey("korisnici.ID_korisnika", ondelete="CASCADE"))
    proizvod_id = Column(Integer, ForeignKey("proizvod.ID_proizvoda",ondelete="CASCADE"))
   