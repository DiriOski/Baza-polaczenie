import cx_Oracle
import random

user_name = ""
password = ""

try:
    dsn = cx_Oracle.makedsn(host='', port=1521, service_name='tpdb')
    connection = cx_Oracle.connect(user=user_name, password=password, dsn=dsn)
    cursor = connection.cursor()
    print("Połączono z SQLDeveloper :)")
except cx_Oracle.Error as error:
    print("Błąd połączenia z bazą danych:", error)
cursor = connection.cursor()

cursor = connection.cursor()

def get_klient_ids(cursor):
    cursor.execute("SELECT id_klient FROM klient")
    klient_ids = [row[0] for row in cursor.fetchall()]
    return klient_ids

def InsertRandomKlient(howMany, cursor):
    names = ['Adam', 'Barbara', 'Celina', 'Dariusz', 'Ewa', 'Filip', 'Gabriela', 'Henryk', 'Izabela', 'Jan']
    surnames = ['Kowalski', 'Nowak', 'Mazur', 'Wójcik', 'Krawczyk', 'Lewandowski', 'Piotrowski', 'Szymański', 'Woźniak']
    postal_codes = ['01-100', '02-200', '03-300', '04-400', '05-500', '06-600', '07-700', '08-800', '09-900', '10-100']
    city = ['Warszawa', 'Kraków', 'Gdańsk', 'Poznań', 'Wrocław', 'Katowice', 'Szczecin', 'Lublin', 'Białystok',
                'Olsztyn']
    street = ['Kwiatowa', 'Słoneczna', 'Brzozowa', 'Akacjowa', 'Dębowa', 'Topolowa', 'Świerkowa', 'Lipowa', 'Jesionowa',
                  'Wiśniowa']

    cursor.execute("SELECT id_klient FROM klient ")
    rows = cursor.fetchall()
    if rows:
        var = int(rows[-1][0]) + 1
    else:
        var = 1

    for i in range(var, howMany + var):
        Imie = random.choice(names)
        Nazwisko = random.choice(surnames)
        Miejscowosc = random.choice(city)
        Kod_pocztowy = random.choice(postal_codes)
        Ulica = random.choice(street)
        Numer_domu = random.randint(1, 200)
        Numer_mieszkania = random.randint(1, 50)
        Numer_telefonu = f"{random.randint(100000000, 999999999):09}"

        cursor.execute(
            """
            INSERT INTO Klient 
            (id_klient, imie, nazwisko, miejscowosc, kod_pocztowy, ulica, nr_domu, nr_lokalu, nr_telefonu) 
            VALUES 
            (:1, :2, :3, :4, :5, :6, :7, :8, :9)
            """,
            (i, Imie, Nazwisko, Miejscowosc, Kod_pocztowy, Ulica, Numer_domu, Numer_mieszkania, Numer_telefonu))

howMany = int(input(" 0 - Dodaj rekordy do wszystkich tabel \n" " 1 - Dodaj rekordy do jednej tabeli \n"))

klient_ids = get_klient_ids(cursor)

if howMany == 0:
    howMany = int(input("Podaj liczbę rekordów jaką chcesz dodać: "))
    InsertRandomKlient(howMany, cursor)
elif howMany == 1:
    howMany = int(input("Wybierz tabelę: \n"
                        "1 - Klient \n"))
    if howMany == 1:
        howMany = int(input("Podaj liczbę rekordów jaką chcesz dodać : "))
        InsertRandomKlient(howMany, cursor)
    else:
        print("Nie ma takiej opcji wyboru")
else:
    print("Nie ma takiej opcji wyboru")

connection.commit()
connection.close()