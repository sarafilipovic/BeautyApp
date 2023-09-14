from __init__ import Session

from proizvodi import Proizvod
from korisnici import Korisnik
from kosarica import Kosarica
from __init__ import Base
from datetime import datetime
from sqlalchemy.exc import IntegrityError





import os 
from flask import Flask,render_template, request,redirect, url_for,flash,session



app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), '../templates'))
app.secret_key = 'ovo-je-moj-tajni-kljuc'
app.config['SESSION_TYPE'] = 'filesystem'


@app.route("/")
def index ():
    return render_template('register.html') 


@app.route('/register', methods=['POST'])
def register_user():
    
    ime = request.form['ime']
    prezime = request.form['prezime']
    email = request.form['email']
    password = request.form['lozinka']
    
    korisnik = Korisnik(ime=ime, prezime=prezime, email=email, password=password)
    Session.add(korisnik)
    Session.commit()

    flash('Uspjesna registracija ', 'success')
    return redirect(url_for('login'))


@app.route("/login")
def login ():
    return render_template('login.html')

@app.route('/loguser', methods=['GET', 'POST'])
def log_user():
   
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = Session.query(Korisnik).filter_by(email=email, password=password).first()
       
        if user:
            session['user_name'] = user.ime
            session['user_id'] = user.ID_korisnika
           
            return redirect(url_for('proizvod'))
        else:
            flash('Pogrešan e-mail ili lozinka. Molimo pokušajte ponovno.', 'danger')
            return redirect(url_for('login'))



@app.route('/logout')
def logout():
    
    session.pop('user_name', None)
   
    return redirect(url_for('login'))


@app.route("/proizvodi")
def proizvod ():
    proizvod = Session.query(Proizvod).all()
    korisnik_id = session['user_id']   
    proizvodi_u_kosarici = Session.query(Kosarica).filter_by(korisnik_id=korisnik_id).all()
    broj_proizvoda_u_kosarici = len(proizvodi_u_kosarici)
    return render_template('proizvod.html', proizvodi=proizvod, broj = broj_proizvoda_u_kosarici)

@app.route('/dodaj-proizvod', methods=['POST'])
def dodaj_proizvod():
    
    korisnik_id = session['user_id']

    ime = request.form['ime']
    korisnik_id = korisnik_id;
    opis = request.form['opis']
    cijena = request.form['cijena']
    
    
    proizvod= Proizvod(ime=ime, korisnik_id=korisnik_id, opis=opis, cijena=cijena,)
    Session.add(proizvod)
    Session.commit()
    return redirect(url_for('proizvod'))


@app.route('/izbrisi_proizvod/<int:ID_proizvoda>', methods=['POST'])
def izbrisi_proizvod(ID_proizvoda):
    proizvod = Session.query(Proizvod).get(ID_proizvoda)
    
    Session.delete(proizvod)
    Session.commit()  
        
    return redirect(url_for('proizvod'))
    
        
    
@app.route('/uredi_proizvod/<int:ID_proizvoda>')
def uredi_proizvod(ID_proizvoda):
    proizvod = Session.query(Proizvod).get(ID_proizvoda)
    
    return render_template('uredi_proizvod.html', proizvod=proizvod) 

@app.route('/update_proizvod/<int:ID_proizvoda>', methods=['POST'])
def update_proizvod(ID_proizvoda):
    proizvod = Session.query(Proizvod).get(ID_proizvoda)
    if proizvod:
        
        proizvod.ime = request.form.get('ime')
        proizvod.opis = request.form.get('opis')
        proizvod.cijena = request.form.get('cijena')
      
        Session.commit()
  
    return redirect(url_for('proizvod'))


@app.route('/dodaj_kosarica/<int:ID_proizvoda>', methods=['POST'])
def dodaj_kosarica(ID_proizvoda):
    
    korisnik_id = session['user_id']
    postoji = Session.query(Kosarica).filter_by(proizvod_id=ID_proizvoda, korisnik_id=korisnik_id).first()
    if postoji:
        
        return redirect(url_for('proizvod'))
    else:
        korisnik_id = session['user_id']
        kosarica = Kosarica(proizvod_id=ID_proizvoda, korisnik_id=korisnik_id)
        Session.add(kosarica)
        Session.commit()
    
    
    return redirect(url_for('proizvod'))
    
@app.route("/kosarica")
def kosarica ():
    proizvod = Session.query(Proizvod).all()
    korisnik = Session.query(Korisnik).all()
    korisnik_id = session['user_id']   
    proizvodi_u_kosarici = Session.query(Kosarica).filter_by(korisnik_id=korisnik_id).all()
    broj_proizvoda_u_kosarici = len(proizvodi_u_kosarici)
    return render_template('kosarica.html', kosarica=proizvodi_u_kosarici, broj = broj_proizvoda_u_kosarici,proizvodi=proizvod, korisnici=korisnik)


@app.route('/izbrisi_kosaricu/<int:ID_kosarice>', methods=['POST'])
def izbrisi_kosaricu(ID_kosarice):
    kosarica = Session.query(Kosarica).get(ID_kosarice)
    
    Session.delete(kosarica)
    Session.commit()  
        
    return redirect(url_for('kosarica'))


@app.route("/pretraga-proizvoda", methods=["GET"])
def pretrazi_proizvode():
   
    korisnik_id = session['user_id']   
    ime_proizvoda = request.args.get("ime_proizvoda")
    proizvodi_u_kosarici = Session.query(Kosarica).filter_by(korisnik_id=korisnik_id).all()
    broj_proizvoda_u_kosarici = len(proizvodi_u_kosarici)
  
    proizvodi = Session.query(Proizvod).filter(Proizvod.ime.ilike(f"%{ime_proizvoda}%")).all()

   
    return render_template("rezultati_pretrage.html", proizvodi=proizvodi, broj=broj_proizvoda_u_kosarici)

app.debug = True

if __name__ == '__main__':
     app.run(host="0.0.0.0", port=5000)