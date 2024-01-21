import mysql.connector
from mysql.connector import IntegrityError

# Povezivanje s bazom podataka
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="AN1246A301JA",
    database="proizvodi"
)
cursor = db_connection.cursor()

def smanji_cijenu_proizvoda(proizvod_id, popust):
    try:
        cursor.callproc('smanji_cijene_proizvoda', args=(proizvod_id, popust))
        db_connection.commit()
        print("Cijena proizvoda smanjena.")
    except Exception as e:
        print(f"Greška prilikom smanjenja cijene proizvoda: {str(e)}")


def prikazi_ukupnu_cijenu():
    cursor.execute("SELECT ukupna_cijena FROM pogled_proizvodi LIMIT 1")
    ukupna_cijena = cursor.fetchone()

    if ukupna_cijena:
        print(f"Ukupna cijena svih proizvoda: {ukupna_cijena[0]}")
    else:
        print("Nema dostupnih podataka.")

def prikazi_proizvode():
    cursor.execute("SELECT * FROM proizvod")
    proizvodi = cursor.fetchall()
    for proizvod in proizvodi:
        print(proizvod)

def dodaj_proizvod(naziv, cijena):
    # Provjera jedinstvenosti kombinacije naziva i cijene
    cursor.execute("SELECT id FROM proizvod WHERE naziv=%s AND cijena=%s", (naziv, cijena))
    existing_proizvod = cursor.fetchone()

    if existing_proizvod:
        print(f"Greška: Proizvod s nazivom '{naziv}' i cijenom '{cijena}' već postoji.")
    else:
        cursor.execute("INSERT INTO proizvod (naziv, cijena) VALUES (%s, %s)", (naziv, cijena))
        db_connection.commit()
        print("Proizvod dodan.")

def uredi_proizvod(proizvod_id, naziv, cijena):
    cursor.execute("UPDATE proizvod SET naziv=%s, cijena=%s WHERE id=%s", (naziv, cijena, proizvod_id))
    db_connection.commit()
    print("Proizvod uređen.")

def obrisi_proizvod(proizvod_id):
    cursor.execute("DELETE FROM proizvod WHERE id=%s", (proizvod_id,))
    db_connection.commit()
    print("Proizvod obrisan.")

while True:
    print("\n1. Prikazi proizvode")
    print("2. Dodaj proizvod")
    print("3. Uredi proizvod")
    print("4. Obrisi proizvod")
    print("5. Prikazi ukupnu cijenu")
    print("6. Smanji cijene proizvoda")
    print("0. Izlaz")

    izbor = input("Odaberi opciju: ")

    if izbor == "1":
        prikazi_proizvode()
    elif izbor == "2":
        naziv = input("Unesi naziv proizvoda: ")
        cijena = float(input("Unesi cijenu proizvoda: "))
        dodaj_proizvod(naziv, cijena)
    elif izbor == "3":
        proizvod_id = int(input("Unesi ID proizvoda koji želiš urediti: "))
        naziv = input("Unesi novi naziv proizvoda: ")
        cijena = float(input("Unesi novu cijenu proizvoda: "))
        uredi_proizvod(proizvod_id, naziv, cijena)
    elif izbor == "4":
        proizvod_id = int(input("Unesi ID proizvoda koji želiš obrisati: "))
        obrisi_proizvod(proizvod_id)
    elif izbor == "5":
        prikazi_ukupnu_cijenu()
    elif izbor == "6":
        proizvod_id = int(input("Unesi ID proizvoda kojem želiš smanjiti cijenu: "))
        popust = float(input("Unesi postotak za koji želiš smanjiti cijenu: "))
        smanji_cijenu_proizvoda(proizvod_id, popust)
    elif izbor == "0":
        break
    else:
        print("Neispravan unos. Pokušaj ponovno.")

# Zatvaranje veze s bazom podataka
cursor.close()
db_connection.close()
