from flask import Flask, render_template, request, redirect
import mysql.connector
app = Flask(__name__)

# Povezivanje s bazom podataka
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="AN1246A301JA",
    database="proizvodi"
)
cursor = db_connection.cursor()


@app.route('/')
def index():
    return render_template('index.html')

def smanji_cijenu_proizvoda(proizvod_id, popust):
    try:
        cursor.callproc('smanji_cijene_proizvoda', args=(proizvod_id, popust))
        db_connection.commit()
        print("Cijena proizvoda smanjena.")
    except Exception as e:
        print(f"Greška prilikom smanjenja cijene proizvoda: {str(e)}")


@app.route('/smanji_cijenu', methods=['POST'])
def smanji_cijenu_view():
    if request.method == 'POST':
        proizvod_id = int(request.form['proizvod_id'])
        popust = float(request.form['popust'])
        smanji_cijenu_proizvoda(proizvod_id, popust)
        return redirect('/proizvodi')
    else:
        return "Neispravan zahtjev."


@app.route('/proizvodi')
def prikazi_proizvode():
    cursor.execute("SELECT * FROM proizvod")
    proizvodi = cursor.fetchall()
    return render_template('proizvodi.html', proizvodi=proizvodi)


@app.route('/dodaj_proizvod', methods=['GET', 'POST'])
def dodaj_proizvod():
    if request.method == 'POST':
        naziv = request.form['naziv']
        cijena = float(request.form['cijena'])
        dodaj_proizvod_db(naziv, cijena)
        return redirect('/proizvodi')
    return render_template('dodaj_proizvod.html')


def dodaj_proizvod_db(naziv, cijena):
    cursor.execute("INSERT INTO proizvod (naziv, cijena) VALUES (%s, %s)", (naziv, cijena))
    db_connection.commit()


@app.route('/uredi_proizvod/<int:proizvod_id>', methods=['GET', 'POST'])
def uredi_proizvod(proizvod_id):
    if request.method == 'POST':
        naziv = request.form['naziv']
        cijena = float(request.form['cijena'])
        uredi_proizvod_db(proizvod_id, naziv, cijena)
        return redirect('/proizvodi')
    cursor.execute("SELECT * FROM proizvod WHERE id=%s", (proizvod_id,))
    proizvod = cursor.fetchone()
    return render_template('uredi_proizvod.html', proizvod=proizvod)


def uredi_proizvod_db(proizvod_id, naziv, cijena):
    cursor.execute("UPDATE proizvod SET naziv=%s, cijena=%s WHERE id=%s", (naziv, cijena, proizvod_id))
    db_connection.commit()


@app.route('/obrisi_proizvod/<int:proizvod_id>')
def obrisi_proizvod(proizvod_id):
    obrisi_proizvod_db(proizvod_id)
    return redirect('/proizvodi')

def obrisi_proizvod_db(proizvod_id):
    cursor.execute("DELETE FROM proizvod WHERE id=%s", (proizvod_id,))
    db_connection.commit()


def prikazi_ukupnu_cijenu():
    cursor.execute("SELECT SUM(cijena) AS ukupna_cijena_proizvoda FROM proizvod")
    ukupna_cijena = cursor.fetchone()

    if ukupna_cijena:
        print(f"Ukupna cijena svih proizvoda: {ukupna_cijena[0]}")
    else:
        print("Nema dostupnih podataka.")

# ...

@app.route('/ukupna_cijena', methods=['GET'])
def prikazi_ukupnu_cijenu_view():
    cursor.execute("SELECT SUM(cijena) AS ukupna_cijena_proizvoda FROM proizvod")
    ukupna_cijena = cursor.fetchone()

    if ukupna_cijena:
        return render_template('ukupna_cijena.html', ukupna_cijena=ukupna_cijena[0])
    else:
        return "Nema dostupnih podataka."


# ...

def generiraj_string_proizvoda():
    cursor.execute("SELECT CONCAT('Svi uneseni proizvodi su: ', GROUP_CONCAT(CONCAT(naziv, ' sa cijenom od: ', cijena) SEPARATOR '; ')) AS rezultat FROM proizvod")
    rezultat = cursor.fetchone()

    if rezultat:
        return rezultat[0]
    else:
        return "Nema dostupnih podataka."

# Primjer poziva nove funkcije
string_proizvoda = generiraj_string_proizvoda()
print(string_proizvoda)


# ...

@app.route('/generiraj_string_proizvoda', methods=['GET'])
def generiraj_string_proizvoda_view():
    string_proizvoda = generiraj_string_proizvoda()
    return render_template('generiraj_string_proizvoda.html', string_proizvoda=string_proizvoda)

# ...


if __name__ == '__main__':
    app.run(debug=True)
