import sqlite3
import time


class CredentialManager:
    def __init__(self):
        self.connection = sqlite3.connect('data/credentials.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS credentials (username MEDIUMTEXT NOT NULL, password MEDIUMTEXT NOT NULL, date_entered BIGINT UNSIGNED NOT NULL, department TEXT, clearance UNSIGNED TINYINT, PRIMARY KEY (username))")

    def get_clearance(self, username):
        values = (username,)
        self.cursor.execute(f"SELECT clearance FROM credentials WHERE username = ?", values)
        clearance = self.cursor.fetchone()[0]
        if clearance == 2:
            return "Admin"
        if clearance == 1:
            return "User"
        else:
            return "Guest"
    
    def get_usernames(self):
        self.cursor.execute(f"SELECT username FROM credentials")
        return (row[0] for row in self.cursor.fetchall())
    
    def _get_feb_days(self, year):
        if year % 400 == 0:
            return 29
        if year % 100 == 0:
            return 28
        if year % 4 == 0:
            return 29
        return 28

    def convert_ms_to_utc(self, time_ms):
        date_entered_yr = int((((((time_ms / 1000) / 60) / 60) / 24) / 365.2425) + 1970)
        date_entered_dy = int((((((time_ms / 1000) / 60) / 60) / 24)) % 365.2425)
        date_entered_hr = int((((time_ms / 1000) / 60) / 60) % 24)
        date_entered_mn = int(((time_ms / 1000) / 60) % 60)
        date_entered_sc = int((time_ms / 1000) % 60)

        days_in_month = [31, self._get_feb_days(date_entered_yr), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        date_entered_mo = 1
        for month in days_in_month:
            if date_entered_dy > month:
                date_entered_dy -= month
                date_entered_mo += 1

        return f"{date_entered_hr}:{date_entered_mn}:{date_entered_sc} {date_entered_mo}/{date_entered_dy}/{date_entered_yr} UTC"


    def get_date_entered(self, username):
        values = (username,)
        self.cursor.execute(f"SELECT date_entered FROM credentials WHERE username = ?", values)
        return self.convert_ms_to_utc(self.cursor.fetchone()[0])

    def verify_credentials(self, username, password):
        values = (username,)
        self.cursor.execute(f"SELECT password FROM credentials WHERE username = ?", values)
        if password in (row[0] for row in self.cursor.fetchall()):
            return True
        return False
        

    def get_department(self, username):
        values = (username,)
        self.cursor.execute(f"SELECT department FROM credentials WHERE username = ?", values)
        department = self.cursor.fetchone()[0]
        return department

    def display_all(self):
        self.cursor.execute(f"SELECT * FROM credentials")
        for row in self.cursor.fetchall():
            print(row)

    def add_user(self, username, password, department=None, clearance=0):
        date_entered = int(round(time.time() * 1000))

        values = (username, password, date_entered, department, clearance)
        self.cursor.execute(f"INSERT INTO credentials VALUES (?, ?, ?, ?, ?)", values)
        self.connection.commit()


interface = CredentialManager()
logged_in = False

if "y" == input("Would you like to log in?\n(y/n)> "):
    username = input("Username:\n> ")
    password = input("Password\n> ")
    valid = True
    if username not in interface.get_usernames():
        valid = False
    if not interface.verify_credentials(username, password):
        valid = False
    if valid:
        logged_in = True
        print("You have successfully logged in")

if logged_in and "y" == input("Would you like to enter a new user?\n(y/n)> "):
    done = False
    while not done:
        taken = True
        while taken:
            username = input("Username\n> ")
            if username not in interface.get_usernames():
                taken = False
            else:
                print("That username is already taken")
        password = input("Password\n> ")
        if username != "" and password != "" and len(username) >= 8 and len(password) >= 8:
            done = True
        else:
            print("Username and Password must be at least 8 characters long")
    done = False
    print("Department?")
    while not done:
        num_department = input("1 - Rehab\n2 - ICU\n3 - Surgery\n> ")
        if (num_department.isnumeric() and (0 <= int(num_department) <= 3)):
            done = True
        else:
            print("Invalid entry, choose one of the following:")
    assert 0 <= int(num_department) <= 3
    if num_department == '0':
        department = "Administration"
    elif num_department == '1':
        department = "Rehab"
    elif num_department == '2':
        department = "ICU"
    elif num_department == '3':
        department = "Surgery"
    else:
        assert False
    done = False
    print("Clearance:")
    while not done:
        clearance = input("1 - Guest\n2 - User\n3 - Admin\n> ")
        if (clearance.isnumeric() and (1 <= int(clearance) <= 3)):
            done = True
        else:
            print("Invalid entry, choose one of the following:")
    clearance = int(clearance) - 1
    interface.add_user(username, password, department, clearance) 

interface.display_all()
