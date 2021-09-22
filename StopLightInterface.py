import sqlite3
import random

class StopLightInterface:
    def __init__(self):
        self.connection = sqlite3.connect('data/records.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS ServiceRequests (incident_id MEDIUMINT UNSIGNED NOT NULL, summary TEXT, description TEXT, date_entered TEXT, department TEXT, request_source TEXT, category TEXT, color TEXT, reason_red TEXT, date_completed TEXT, date_expected TEXT, date_retired TEXT, PRIMARY KEY (incident_id))")

    def get_summary(self, incident_id):
        values = (incident_id,)
        self.cursor.execute("SELECT summary FROM ServiceRequests WHERE incident_id = ?", values)
        summary = self.cursor.fetchone()[0]
        return summary

    def get_description(self, incident_id):
        values = (incident_id,)
        self.cursor.execute("SELECT description FROM ServiceRequests WHERE incident_id = ?", values)
        description = self.cursor.fetchone()[0]
        return description

    def get_date_entered(self, incident_id):
        values = (incident_id,)
        self.cursor.execute("SELECT date_entered FROM ServiceRequests WHERE incident_id = ?", values)
        date_entered = self.cursor.fetchone()[0]
        return date_entered

    def get_department(self, incident_id):
        values = (incident_id,)
        self.cursor.execute("SELECT department FROM ServiceRequests WHERE incident_id = ?", values)
        department = self.cursor.fetchone()[0]
        return department

    def get_request_source(self, incident_id):
        values = (incident_id,)
        self.cursor.execute("SELECT request_source FROM ServiceRequests WHERE incident_id = ?", values)
        request_source = self.cursor.fetchone()[0]
        return request_source

    def get_category(self, incident_id):
        values = (incident_id,)
        self.cursor.execute("SELECT category FROM ServiceRequests WHERE incident_id = ?", values)
        category = self.cursor.fetchone()[0]
        return category

    def get_color(self, incident_id):
        values = (incident_id,)
        self.cursor.execute("SELECT color FROM ServiceRequests WHERE incident_id = ?", values)
        color = self.cursor.fetchone()[0]
        return color

    def get_reason_red(self, incident_id):
        values = (incident_id,)
        self.cursor.execute("SELECT reason_red FROM ServiceRequests WHERE incident_id = ?", values)
        reason_red = self.cursor.fetchone()[0]
        return reason_red

    def get_date_completed(self, incident_id):
        values = (incident_id,)
        self.cursor.execute("SELECT date_completed FROM ServiceRequests WHERE incident_id = ?", values)
        date_completed = self.cursor.fetchone()[0]
        return date_completed

    def get_date_expected(self, incident_id):
        values = (incident_id,)
        self.cursor.execute("SELECT date_expected FROM ServiceRequests WHERE incident_id = ?", values)
        date_expected = self.cursor.fetchone()[0]
        return date_expected 

    def get_date_retired(self, incident_id):
        values = (incident_id,)
        self.cursor.execute("SELECT date_retired FROM ServiceRequests WHERE incident_id = ?", values)
        date_retired = self.cursor.fetchone()[0]
        return date_retired

    def display_all(self):
        self.cursor.execute("SELECT * FROM ServiceRequests")
        for row in self.cursor.fetchall():
            print(row)

    def add_request(self, summary=None, description=None, date_entered=None, department=None, request_source=None, category=None, color=None, reason_red=None, date_completed=None, date_expected=None, date_retired=None):
        new_value = False
        self.cursor.execute("SELECT incident_id FROM ServiceRequests")
        while not new_value:
            new_value = True
            incident_id = random.randint(1111111, 9999999)
            for row in self.cursor.fetchall():
                if row[0] == incident_id:
                    new_value = False
        values = (incident_id, summary, description, date_entered, department, request_source, category, color, reason_red, date_completed, date_expected, date_retired)
        self.cursor.execute("INSERT INTO ServiceRequests VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", values)
        self.connection.commit()

interface = StopLightInterface()
interface.add_request(summary=input("summary"), description=input("description"), date_entered=input("date_entered"), department=input("department"), request_source=input("request_source"), category=input("category"), color=input("color"), reason_red=input("reason_red"), date_completed=input("date_completed"), date_expected=input("date_expected"), date_retired=input("date_retired"))
interface.display_all()

print(interface.get_summary(9418259))
print(interface.get_description(9418259))
print(interface.get_date_entered(9418259))
print(interface.get_department(9418259))
print(interface.get_request_source(9418259))
print(interface.get_category(9418259))
print(interface.get_color(9418259))
print(interface.get_reason_red(9418259))
print(interface.get_date_completed(9418259))
print(interface.get_date_expected(9418259))
print(interface.get_date_retired(9418259))