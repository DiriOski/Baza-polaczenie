import random
import cx_Oracle
from datetime import datetime, timedelta
import string

user_name = ""
password = ""

try:
    dsn = cx_Oracle.makedsn(host='', port=1521, service_name='tpdb')
    connection = cx_Oracle.connect(user=user_name, password=password, dsn=dsn)
    cursor = connection.cursor()
    print("Połączono z SQLDeveloper :)")
    cursor = connection.cursor()
except cx_Oracle.Error as error:
    print("Błąd połączenia z bazą danych:", error)


def random_date(start_date, end_date):

    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    random_date = start_date + timedelta(days=random_days)
    return random_date.strftime('%Y-%m-%d')



def get_pracownicy_ids(cursor):
    cursor.execute("SELECT id_pracownik FROM pracownicy")
    pracownicy_ids = [row[0] for row in cursor.fetchall()]
    return pracownicy_ids

def get_produkty_ids(cursor):
    cursor.execute("SELECT id_produkt FROM produkty")
    produkty_ids = [row[0] for row in cursor.fetchall()]
    return produkty_ids

def get_recepty_ids(cursor):
    cursor.execute("SELECT id_recepta FROM recepty")
    recepty_ids = [row[0] for row in cursor.fetchall()]
    return recepty_ids

def get_zamowienia_ids(cursor):
    cursor.execute("SELECT id_zamowienia FROM zamowienia")
    zamowienia_ids = [row[0] for row in cursor.fetchall()]
    return zamowienia_ids

def get_stanowisko_id(cursor):
    cursor.execute("SELECT id_stanowisko FROM stanowisko")
    stanowisko_id = [row[0] for row in cursor.fetchall()]
    return stanowisko_id

def get_magazyn_id(cursor):
    cursor.execute("SELECT id_magazyn FROM magazyn")
    magazyn_id = [row[0] for row in cursor.fetchall()]
    return magazyn_id

def get_pacjent_ids(cursor):
    cursor.execute("SELECT id_pacjent FROM pacjent")
    pacjent_ids = [row[0] for row in cursor.fetchall()]
    return pacjent_ids


def InsertLosowyPacjent(howMany, cursor, save_to_file=False):
    names = ['Adam', 'Anna', 'Jan', 'Maria', 'Piotr', 'Zofia', 'Stanisław', 'Ewa', 'Marek', 'Katarzyna']
    surnames = ['Kowalski', 'Nowak', 'Wiśniewski', 'Dąbrowska', 'Lewandowski', 'Wójcik', 'Kamińska', 'Kowalczyk', 'Zielińska', 'Szymańska']
    pesels = [''.join(random.choices(string.digits, k=11)) for _ in range(10)]

    inserts = []

    cursor.execute("SELECT id_pacjent FROM pacjent")
    rows = cursor.fetchall()
    if rows:
        var = int(rows[-1][0]) + 1
    else:
        var = 1

    for i in range(var, howMany + var):
        name = random.choice(names)
        surname = random.choice(surnames)
        pesel = random.choice(pesels)
        phone = f"+48{''.join(random.choices(string.digits, k=9))}"  # Losowy numer zaczynający się na +48

        insert = f"""
            INSERT INTO pacjent 
            (id_pacjent, imie, nazwisko, pesel, nr_tel) 
            VALUES 
            ({i}, '{name}', '{surname}', '{pesel}', '{phone}')
        """
        inserts.append(insert)

    # Wykonaj inserty
    for insert_query in inserts:
        cursor.execute(insert_query)

    # Zapisz inserty do pliku
    if save_to_file:
        with open('inserts_pacjent.txt', 'w') as file:
            file.write("Wykonane inserty dla tabeli pacjent:\n")
            for insert_query in inserts:
                file.write(insert_query + "\n")

    return inserts

def InsertRandomPracownik(howMany, cursor, save_to_file=False):
    imiona = ['Magdalena', 'Stanisław', 'Ewelina', 'Daria', 'Radosław']
    nazwiska = ['Kowalczyk', 'Zieliński', 'Kamińska', 'Włodarczyk', 'Sikorski']
    pesels = [''.join(random.choices(string.digits, k=11)) for _ in range(10)]
    liczba_godziny = [158, 176, 162, 179, 171]
    stanowisko_ids = get_stanowisko_id(cursor)  # Pobierz dostępne indeksy stanowisk

    inserts = []

    cursor.execute("SELECT id_pracownik FROM pracownicy")
    rows = cursor.fetchall()
    if rows:
        var = int(rows[-1][0]) + 1
    else:
        var = 1

    for i in range(var, howMany + var):
        imie = random.choice(imiona)
        nazwisko = random.choice(nazwiska)
        pesel = random.choice(pesels)
        liczba_godz = random.choice(liczba_godziny)
        nr_tel = f"+48{''.join(random.choices(string.digits, k=9))}"
        stanowisko_id = random.choice(stanowisko_ids)  # Wybierz losowe stanowisko z dostępnych indeksów

        insert = f"""
            INSERT INTO pracownicy 
            (id_pracownik, imie, nazwisko, pesel, liczba_godz, nr_tel, stanowisko_id_stanowisko) 
            VALUES 
            ({i}, '{imie}', '{nazwisko}', '{pesel}', {liczba_godz}, '{nr_tel}', {stanowisko_id})
        """
        inserts.append(insert)

    # Wykonaj inserty
    for insert_query in inserts:
        cursor.execute(insert_query)

    # Zapisz inserty do pliku
    if save_to_file:
        with open('insertyPracownicy.txt', 'w') as file:
            file.write("Wykonane inserty dla tabeli pracownicy:\n")
            for insert_query in inserts:
                file.write(insert_query + "\n")

    return inserts

def InsertRandomStanowisko(howMany, cursor, save_to_file=False):
    nazwy_stanowisk = ['Farmaceuta', 'Farmaceuta kierowniczy', 'Magazynier']
    godziny_rozpoczecia = ['06:00:00', '14:00:00']

    inserts = []

    cursor.execute("SELECT id_stanowisko FROM stanowisko")
    rows = cursor.fetchall()
    if rows:
        var = int(rows[-1][0]) + 1
    else:
        var = 1

    for i in range(var, howMany + var):
        nazwa_stanowiska = random.choice(nazwy_stanowisk)
        godz_rozpoczecia = random.choice(godziny_rozpoczecia)
        godz_zakonczenia = '14:00:00' if godz_rozpoczecia == '06:00:00' else '22:00:00'

        insert = f"""
            INSERT INTO stanowisko 
            (id_stanowisko, nazwa, godz_rozpoczecia_zmiany, godz_zakonczenia_zmiany) 
            VALUES 
            ({i}, '{nazwa_stanowiska}', TO_DATE('2024-03-05 {godz_rozpoczecia}', 'YYYY-MM-DD HH24:MI:SS'), TO_DATE('2024-03-05 {godz_zakonczenia}', 'YYYY-MM-DD HH24:MI:SS'))
        """
        inserts.append(insert)

    # Wykonaj inserty
    for insert_query in inserts:
        cursor.execute(insert_query)

    # Zapisz inserty do pliku
    if save_to_file:
        with open('insertyStanowisko.txt', 'w') as file:
            file.write("Wykonane inserty dla tabeli stanowisko:\n")
            for insert_query in inserts:
                file.write(insert_query + "\n")

    return inserts

def InsertRandomMagazyn(howMany, cursor, save_to_file=False):
    inserts = []

    cursor.execute("SELECT id_magazyn FROM magazyn")
    rows = cursor.fetchall()
    if rows:
        var = int(rows[-1][0]) + 1
    else:
        var = 1


    for i in range(var, howMany + var):
        ilosc = random.randint(1, 50)  # Losowa ilość towarów w magazynie (od 1 do 50)
        insert = f"""
            INSERT INTO magazyn 
            (id_magazyn, ilosc) 
            VALUES 
            ({i}, {ilosc})
        """
        inserts.append(insert)

    # Wykonaj inserty
    for insert_query in inserts:
        cursor.execute(insert_query)

    # Zapisz inserty do pliku
    if save_to_file:
        with open('insertyMagazyn.txt', 'w') as file:
            file.write("Wykonane inserty dla tabeli magazyn:\n")
            for insert_query in inserts:
                file.write(insert_query + "\n")

    return inserts


def InsertLosowyProdukt(howMany, cursor, save_to_file=False):
    names = ['Amoxicillin', 'Ventolin', 'Sertraline', 'Cipralex', 'Warfarin', 'Paracetamol', 'Ibuprofen', 'Diazepam', 'Omeprazole', 'Metformin']
    producenci = ['GlaxoSmithKline', 'Pfizer', 'Lundbeck', 'Bristol-Myers Squibb', 'Merck', 'AstraZeneca', 'Novartis', 'Johnson & Johnson', 'Sanofi', 'Roche']
    rodzaje_produktow = ['Lek', 'Suplement', 'Inne']
    magazyn_ids = get_magazyn_id(cursor)

    inserts = []

    cursor.execute("SELECT id_produkt FROM produkty")
    rows = cursor.fetchall()
    if rows:
        var = int(rows[-1][0]) + 1
    else:
        var = 1

    for i in range(var, howMany + var):
        nazwa = random.choice(names)
        producent = random.choice(producenci)
        rodzaj_produktu = random.choice(rodzaje_produktow)
        cena = round(random.uniform(10.0, 100.0), 2)  # Losowa cena od 10.0 do 100.0
        magazyn_id_magazyn = random.choice(magazyn_ids)  # Losowo wybierz id_magazyn

        insert = f"""
            INSERT INTO produkty 
            (id_produkt, nazwa, producent, rodzaj_produktu, cena, magazyn_id_magazyn) 
            VALUES 
            ({i}, '{nazwa}', '{producent}', '{rodzaj_produktu}', {cena}, {magazyn_id_magazyn})
        """
        inserts.append(insert)

    # Wykonaj inserty
    for insert_query in inserts:
        cursor.execute(insert_query)

    # Zapisz inserty do pliku
    if save_to_file:
        with open('inserts_produkty.txt', 'w') as file:
            file.write("Wykonane inserty dla tabeli produkty:\n")
            for insert_query in inserts:
                file.write(insert_query + "\n")

    return inserts

def InsertRandomRecepta(howMany, cursor, save_to_file=False):
    lekarze = ['Dr. Nowak', 'Dr. Kowalski', 'Dr. Wiśniewski', 'Dr. Lewandowska', 'Dr. Dąbrowski']
    pacjent_ids = get_pacjent_ids(cursor)  # Metoda do pobierania ID pacjentów
    pracownicy_ids = get_pracownicy_ids(cursor)  # Metoda do pobierania ID pracowników

    inserts = []

    cursor.execute("SELECT id_recepta FROM recepty")
    rows = cursor.fetchall()
    if rows:
        var = int(rows[-1][0]) + 1
    else:
        var = 1

    for i in range(var, howMany + var):
        nr_recepty = random.randint(1000, 9999)  # Losowy numer recepty
        data_wystawienia = random_date(start_date='2023-01-01', end_date='2024-12-31')  # Losowa data wystawienia recepty
        data_realizacji = None  # Losowa data realizacji recepty (może być pusta)
        lekarz = random.choice(lekarze)
        pacjent_id_pacjent = random.choice(pacjent_ids)
        pracownik_id_pracownik = random.choice(pracownicy_ids)

        # Losowa data realizacji (jeśli data_wystawienia jest starsza niż 2024-01-01)
        if data_wystawienia > '2024-01-01':
            data_realizacji = random_date(start_date=data_wystawienia, end_date='2024-12-31')

        insert = f"""
            INSERT INTO recepty 
            (id_recepta, nr_recepty, data_wystawienia, data_realizacji, lekarz, pacjent_id_pacjent, pracownicy_id_pracownik) 
            VALUES 
            ({i}, {nr_recepty}, TO_DATE('{data_wystawienia}', 'YYYY-MM-DD'), {f"TO_DATE('{data_realizacji}', 'YYYY-MM-DD HH24:MI:SS')" if data_realizacji else 'NULL'}, '{lekarz}', {pacjent_id_pacjent}, {pracownik_id_pracownik})
            """
        inserts.append(insert)

    # Wykonaj inserty
    for insert_query in inserts:
        cursor.execute(insert_query)

    # Zapisz inserty do pliku
    if save_to_file:
        with open('inserts_recepty.txt', 'w') as file:
            file.write("Wykonane inserty dla tabeli recepty:\n")
            for insert_query in inserts:
                file.write(insert_query + "\n")

    return inserts

def InsertRandomLekiNaRecepte(howMany, cursor, save_to_file=False):
    inserts = []

    recepty_ids = get_recepty_ids(cursor)
    produkty_ids = get_produkty_ids(cursor)

    for i in range(1, howMany + 1):
        obnizka = random.uniform(0, 0.9)  # Losowa wartość z zakresu od 0 do 0.5
        recepta_id = random.choice(recepty_ids)
        produkt_id = random.choice(produkty_ids)

        insert = f"""
            INSERT INTO leki_na_recepte 
            (id_leki, obnizka, recepty_id_recepta, produkty_id_produkt) 
            VALUES 
            ({i}, {obnizka}, {recepta_id}, {produkt_id})
        """
        inserts.append(insert)

    # Wykonaj inserty
    for insert_query in inserts:
        cursor.execute(insert_query)

    # Zapisz inserty do pliku
    if save_to_file:
        with open('inserts_leki_na_recepte.txt', 'w') as file:
            file.write("Wykonane inserty dla tabeli leki_na_recepte:\n")
            for insert_query in inserts:
                file.write(insert_query + "\n")

    return inserts
def generate_random_username():
    random_number = ''.join(random.choices(string.digits, k=5))
    username = f"user{random_number}"
    return username

def generate_random_email(username):
    email = f"{username}@gmail.com"
    return email

def generate_random_password():
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    return password

def InsertRandomLogowanie(howMany, cursor, save_to_file=False):

    '''
    logins = ['magdalena_kowalczyk', 'stanislaw_zielinski', 'ewelina_kaminska', 'daria_wlodarczyk', 'radoslaw_sikorski']
    emails = ['magdalena.kowalczyk@example.com', 'stanislaw.zielinski@example.com', 'ewelina.kaminska@example.com', 'daria.wlodzyk@example.com', 'radoslaw.sikorski@example.com']
    passwords = ['haslo123', 'stanislaw123', 'ewelina123', 'daria123', 'radoslaw123']
    '''

    '''
    login = random.choice(logins)
            email = random.choice(emails)
            haslo = random.choice(passwords)
            '''
    inserts = []
    pracownicy_ids = get_pracownicy_ids(cursor)
    pacjent_ids = get_pacjent_ids(cursor)

    for i in range(1, howMany + 1):


        login = generate_random_username()
        email = generate_random_email(login)
        haslo = generate_random_password()

        pracownik_id = random.choice(pracownicy_ids) if random.random() < 0.5 else 'NULL'
        
        if pracownik_id == 'NULL':
            pacjent_id = random.choice(pacjent_ids)
            pacjent_ids.remove(pacjent_id)
        else:
            pracownicy_ids.remove(pracownik_id)
            pacjent_id = 'NULL'


        insert = f"""
            INSERT INTO logowanie 
            (id_uzytkonwik, login, email, haslo, pracownicy_id_pracownik, pacjent_id_pacjent) 
            VALUES 
            ({i}, '{login}', '{email}', '{haslo}', {pracownik_id}, {pacjent_id})
        """
        inserts.append(insert)

    # Wykonaj inserty
    for insert_query in inserts:
        cursor.execute(insert_query)

    # Zapisz inserty do pliku
    if save_to_file:
        with open('inserts_logowanie.txt', 'w') as file:
            file.write("Wykonane inserty dla tabeli logowanie:\n")
            for insert_query in inserts:
                file.write(insert_query + "\n")

    return inserts

def InsertRandomZamowienie(howMany, cursor, start_date='2023-01-01', end_date='2023-12-31', save_to_file=False):
    inserts = []

    pacjent_ids = get_pacjent_ids(cursor)

    for i in range(1, howMany + 1):
        data_realizacji = random_date(start_date, end_date)
        pacjent_id = random.choice(pacjent_ids)

        insert = f"""
            INSERT INTO zamowienia 
            (id_zamowienia, data_realizacji, pacjent_id_pacjent) 
            VALUES 
            ({i}, TO_DATE('{data_realizacji}', 'YYYY-MM-DD'), {pacjent_id})
        """
        inserts.append(insert)

    # Wykonaj inserty
    for insert_query in inserts:
        cursor.execute(insert_query)

    # Zapisz inserty do pliku
    if save_to_file:
        with open('inserts_zamowienia.txt', 'w') as file:
            file.write("Wykonane inserty dla tabeli zamowienia:\n")
            for insert_query in inserts:
                file.write(insert_query + "\n")

    return inserts

def InsertRandomNumerZamowienia(howMany, cursor, save_to_file=False):
    inserts = []

    produkty_ids = get_produkty_ids(cursor)
    zamowienia_ids = get_zamowienia_ids(cursor)

    for i in range(1, howMany + 1):
        produkty_id = random.choice(produkty_ids)
        zamowienia_id = random.choice(zamowienia_ids)

        insert = f"""
            INSERT INTO numer_zamowienia 
            (id_num_zam, produkty_id_produkt, zamowienia_id_zamowienia) 
            VALUES 
            ({i}, {produkty_id}, {zamowienia_id})
        """
        inserts.append(insert)

    # Wykonaj inserty
    for insert_query in inserts:
        cursor.execute(insert_query)

    # Zapisz inserty do pliku
    if save_to_file:
        with open('inserts_numer_zamowienia.txt', 'w') as file:
            file.write("Wykonane inserty dla tabeli numer_zamowienia:\n")
            for insert_query in inserts:
                file.write(insert_query + "\n")

    return inserts

def InsertRandomPlace(howMany, cursor, save_to_file=False):
    inserts = []

    stanowiska_ids = get_stanowisko_id(cursor)

    for i in range(1, howMany + 1):
        stawka_na_godzine = round(random.uniform(15.00, 40.00), 2)
        stanowisko_id = random.choice(stanowiska_ids)
        stanowiska_ids.remove(stanowisko_id)
        insert = f"""
            INSERT INTO place 
            (id_place, stawka_na_godzine, stanowisko_id_stanowisko) 
            VALUES 
            ({i}, {stawka_na_godzine}, {stanowisko_id})
        """
        inserts.append(insert)

    # Wykonaj inserty
    for insert_query in inserts:
        cursor.execute(insert_query)

    # Zapisz inserty do pliku
    if save_to_file:
        with open('inserts_place.txt', 'w') as file:
            file.write("Wykonane inserty dla tabeli place:\n")
            for insert_query in inserts:
                file.write(insert_query + "\n")

    return inserts

howMany = int(input(" 0 - Dodaj rekordy do wszystkich tabel \n" " 1 - Dodaj rekordy do jednej tabeli \n"))

if howMany == 0:
    howMany = int(input("Podaj liczbę rekordów jaką chcesz dodać do tabel: "))

    inserts = []

    inserts.append(InsertRandomStanowisko(howMany, cursor, save_to_file=False))
    inserts.append(InsertRandomPracownik(howMany, cursor, save_to_file=False))
    inserts.append(InsertLosowyPacjent(howMany, cursor, save_to_file=False))
    inserts.append(InsertRandomMagazyn(howMany, cursor, save_to_file=False))
    inserts.append(InsertLosowyProdukt(howMany, cursor, save_to_file=False))
    inserts.append(InsertRandomRecepta(howMany, cursor, save_to_file=False))
    inserts.append(InsertRandomLekiNaRecepte(howMany, cursor, save_to_file=False))
    inserts.append(InsertRandomLogowanie(howMany, cursor, save_to_file=False))
    inserts.append(InsertRandomZamowienie(howMany, cursor, save_to_file=False))
    inserts.append(InsertRandomNumerZamowienia(howMany, cursor, save_to_file=False))
    inserts.append(InsertRandomPlace(howMany, cursor, save_to_file=False))

    with open('all_inserts.txt', 'w') as file:
        file.write("Nowe inserty dla różnych tabel:\n")
        for insert_list in inserts:
            for insert_query in insert_list:
                file.write(insert_query + "\n")

elif howMany == 1:
    howMany = int(input("Wybierz tabelę: \n"
                        "1 - Pacjent \n"
                        "2 - Pracownik \n"
                        "3 - Zamowienie \n"
                        "4 - Numer Zamowienia \n"
                        "5 - Place \n"
                        "6 - Stanowisko \n"
                        "7 - Recepta \n"
                        "8 - Logowanie \n"
                        "9 - Magazyn \n"
                        "10 - Produkty \n"
                        "11 - Leki na Recepte \n"))

    if howMany == 1:
        howMany = int(input("Podaj liczbę rekordów jaką chcesz dodać do tabeli pacjent : "))
        InsertLosowyPacjent(howMany, cursor, save_to_file=True)
    elif howMany == 2:
        howMany = int(input("Podaj liczbę rekordów jaką chcesz dodać do tabeli pracownik : "))
        InsertRandomPracownik(howMany, cursor, save_to_file=True)
    elif howMany == 3:
        howMany = int(input("Podaj liczbę rekordów jaką chcesz dodać do tabeli zamowienie : "))
        InsertRandomZamowienie(howMany, cursor, save_to_file=True)
    elif howMany == 4:
        howMany = int(input("Podaj liczbę rekordów jaką chcesz dodać do tabeli numer zamowienia : "))
        InsertRandomNumerZamowienia(howMany, cursor, save_to_file=True)
    elif howMany == 5:
        howMany = int(input("Podaj liczbę rekordów jaką chcesz dodać do tabeli place : "))
        InsertRandomPlace(howMany, cursor, save_to_file=True)
    elif howMany == 6:
        howMany = int(input("Podaj liczbę rekordów jaką chcesz dodać do tabeli stanowisko : "))
        InsertRandomStanowisko(howMany, cursor, save_to_file=True)
    elif howMany == 7:
        howMany = int(input("Podaj liczbę rekordów jaką chcesz dodać do tabeli recepta : "))
        InsertRandomRecepta(howMany, cursor, save_to_file=True)
    elif howMany == 8:
        howMany = int(input("Podaj liczbę rekordów jaką chcesz dodać do tabeli logowanie : "))
        InsertRandomLogowanie(howMany, cursor, save_to_file=True)
    elif howMany == 9:
        howMany = int(input("Podaj liczbę rekordów jaką chcesz dodać do tabeli magazyn : "))
        InsertRandomMagazyn(howMany, cursor, save_to_file=True)
    elif howMany == 10:
        howMany = int(input("Podaj liczbę rekordów jaką chcesz dodać do tabeli produkty : "))
        InsertLosowyProdukt(howMany, cursor, save_to_file=True)
    elif howMany == 11:
        howMany = int(input("Podaj liczbę rekordów jaką chcesz dodać do tabeli leki na recepte : "))
        InsertRandomLekiNaRecepte(howMany, cursor, save_to_file=True)
    else:
        print("Nie ma takiej opcji wyboru")
else:
    print("Nie ma takiej opcji wyboru")


connection.commit()
connection.close()