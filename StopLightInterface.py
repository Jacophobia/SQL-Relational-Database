import sqlite3
import random
import time


class StopLightInterface:
    def __init__(self, department):
        assert department != None and department != "None"
        self.department = department
        self.connection = sqlite3.connect('data/records.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.department} (incident_id MEDIUMINT UNSIGNED NOT NULL, summary TEXT, description TEXT NOT NULL, date_entered BIGINT UNSIGNED NOT NULL, department TEXT, request_source TEXT, category TEXT, color TEXT, reason_red TEXT, date_completed TEXT, date_expected TEXT, date_retired TEXT, PRIMARY KEY (incident_id))")

    def get_summary(self, incident_id):
        values = (incident_id,)
        self.cursor.execute(f"SELECT summary FROM {self.department} WHERE incident_id = ?", values)
        summary = self.cursor.fetchone()[0]
        return summary

    def get_description(self, incident_id):
        values = (incident_id,)
        self.cursor.execute(f"SELECT description FROM {self.department} WHERE incident_id = ?", values)
        description = self.cursor.fetchone()[0]
        return description
    
    def _get_feb_days(self, year):
        if year % 400 == 0:
            return 29
        if year % 100 == 0:
            return 28
        if year % 4 == 0:
            return 29
        return 28

    def get_date_entered(self, incident_id):
        values = (incident_id,)
        self.cursor.execute(f"SELECT date_entered FROM {self.department} WHERE incident_id = ?", values)
        date_entered_ms = self.cursor.fetchone()[0]
        date_entered_yr = int((((((date_entered_ms / 1000) / 60) / 60) / 24) / 365.2425) + 1970)
        date_entered_dy = int((((((date_entered_ms / 1000) / 60) / 60) / 24)) % 365.2425)
        date_entered_hr = int((((date_entered_ms / 1000) / 60) / 60) % 24)
        date_entered_mn = int(((date_entered_ms / 1000) / 60) % 60)
        date_entered_sc = int((date_entered_ms / 1000) % 60)

        days_in_month = [31, self._get_feb_days(date_entered_yr), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        date_entered_mo = 1
        for month in days_in_month:
            if date_entered_dy > month:
                date_entered_dy -= month
                date_entered_mo += 1


        return f"{date_entered_hr}:{date_entered_mn}:{date_entered_sc} {date_entered_mo}/{date_entered_dy}/{date_entered_yr} UTC"

    def get_department(self, incident_id):
        values = (incident_id,)
        self.cursor.execute(f"SELECT department FROM {self.department} WHERE incident_id = ?", values)
        department = self.cursor.fetchone()[0]
        return department

    def get_request_source(self, incident_id):
        values = (incident_id,)
        self.cursor.execute(f"SELECT request_source FROM {self.department} WHERE incident_id = ?", values)
        request_source = self.cursor.fetchone()[0]
        return request_source

    def get_category(self, incident_id):
        values = (incident_id,)
        self.cursor.execute(f"SELECT category FROM {self.department} WHERE incident_id = ?", values)
        category = self.cursor.fetchone()[0]
        return category

    def get_color(self, incident_id):
        values = (incident_id,)
        self.cursor.execute(f"SELECT color FROM {self.department} WHERE incident_id = ?", values)
        color = self.cursor.fetchone()[0]
        return color

    def get_reason_red(self, incident_id):
        values = (incident_id,)
        self.cursor.execute(f"SELECT reason_red FROM {self.department} WHERE incident_id = ?", values)
        reason_red = self.cursor.fetchone()[0]
        return reason_red

    def get_date_completed(self, incident_id):
        values = (incident_id,)
        self.cursor.execute(f"SELECT date_completed FROM {self.department} WHERE incident_id = ?", values)
        date_completed = self.cursor.fetchone()[0]
        return date_completed

    def get_date_expected(self, incident_id):
        values = (incident_id,)
        self.cursor.execute(f"SELECT date_expected FROM {self.department} WHERE incident_id = ?", values)
        date_expected = self.cursor.fetchone()[0]
        return date_expected 

    def get_date_retired(self, incident_id):
        values = (incident_id,)
        self.cursor.execute(f"SELECT date_retired FROM {self.department} WHERE incident_id = ?", values)
        date_retired = self.cursor.fetchone()[0]
        return date_retired

    def display_all(self):
        self.cursor.execute(f"SELECT * FROM {self.department}")
        for row in self.cursor.fetchall():
            print(row)

    def add_request(self, summary=None, description=None, department=None, request_source=None, category=None, color=None, reason_red=None, date_completed=None, date_expected=None, date_retired=None):
        new_value = False
        self.cursor.execute(f"SELECT incident_id FROM {self.department}")
        while not new_value:
            new_value = True
            incident_id = random.randint(1111111, 9999999)
            for row in self.cursor.fetchall():
                if row[0] == incident_id:
                    new_value = False

        date_entered = int(round(time.time() * 1000))

        values = (incident_id, summary, description, date_entered, department, request_source, category, color, reason_red, date_completed, date_expected, date_retired)
        self.cursor.execute(f"INSERT INTO {self.department} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", values)
        self.connection.commit()


interface = StopLightInterface()

if "y" == input("Would you like to enter a new item?\n(y/n)> "):
    interface.add_request(
        summary       = input("summary\n>"), 
        description   = input("description\n>"), 
        department    = input("department\n>"), 
        request_source= input("request_source\n>"), 
        category      = input("category\n>"), 
        color         = input("color\n>"), 
        reason_red    = input("reason_red\n>"),
        date_completed= input("date_completed\n>"), 
        date_expected = input("date_expected\n>"), 
        date_retired  = input("date_retired\n>")
    ) 

interface.display_all()

Incident_Number = 1655114

print(interface.get_summary(Incident_Number))
print(interface.get_description(Incident_Number))
print(interface.get_date_entered(Incident_Number))
print(interface.get_department(Incident_Number))
print(interface.get_request_source(Incident_Number))
print(interface.get_category(Incident_Number))
print(interface.get_color(Incident_Number))
print(interface.get_reason_red(Incident_Number))
print(interface.get_date_completed(Incident_Number))
print(interface.get_date_expected(Incident_Number))
print(interface.get_date_retired(Incident_Number))