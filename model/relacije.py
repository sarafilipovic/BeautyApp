
from sqlalchemy.orm import relationship
from korisnici import Korisnik
from proizvodi import Proizvod
from studio import Studio

from recenzije import Recenzija
from kosarica import Kosarica
from __init__ import Base
from __init__  import engine


Korisnik.termin = relationship('Termin', back_populates='korisnik')
Korisnik.recenzija = relationship("Recenzija", back_populates="korisnik")
Korisnik.kosarica = relationship('Kosarica', back_populates='korisnik')
Proizvod.kosarica = relationship('Kosarica', back_populates='proizvod')
Korisnik.proizvod = relationship('Proizvod', back_populates='korisnik')


Base.metadata.bind = engine
Base.metadata.create_all(bind=engine)