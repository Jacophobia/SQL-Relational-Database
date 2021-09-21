import sqlite3

"""
CSE310 SQL Database Workshop

This simple database will store names, titles, and pay for employees.

TODO:

1) Implement display employees.  Try sorting the results.
2) Implement add new employee.  Check for invalid inputs for the pay.
3) Implement update employee pay and check if no update was made because 
   employee name was invalid
4) Implement delete employee by implementing the get_name function.  The 
   get_name funciton should list out all of the employees name with a 
   numbered list.  The user will then select the number for the name they 
   want to delete.
"""

import sqlite3

# Connect to the database
connection = sqlite3.connect('Testing/records.db')
cursor = connection.cursor()

# Create table (if it does not already exist)
cursor.execute("CREATE TABLE IF NOT EXISTS employees (name TEXT, title TEXT, pay REAL)")

def get_name(cursor):
    while True:
        cursor.execute("SELECT name FROM employees")
        names = set()
        for name in cursor.fetchall():
            print(name[0])
            names.add(name[0])
        fired_employee = input("Enter the name of the employee you want to delete\n> ")
        if fired_employee in names:
            return name[0]
        else:
            print("That is not a valid employee")


    


choice = None
while choice != "5":
    print("1) Display Employees")
    print("2) Add Employee")
    print("3) Update Employee Pay")
    print("4) Delete Employee")
    print("5) Quit")
    choice = input("> ")
    print()
    if choice == "1":
        # Display Employees
        cursor.execute("SELECT * FROM employees")
        
        print("{:>10}  {:>10}  {:>10}".format("Name", "Title", "Pay"))
        for record in cursor.fetchall():
            print("{:>10}  {:>10}  {:>10}".format(record[0], record[1], record[2]))

    elif choice == "2":
        # Add New Employee
        name = input("Name: ")
        title = input("Title: ")
        pay = float(input("Pay: "))
        values = (name, title, pay)
        cursor.execute("INSERT INTO employees VALUES (?, ?, ?)", values)
        connection.commit()

    elif choice == "3":
        try:
            # Update Employee Pay
            name = input("Name: ")
            pay = float(input("Pay: "))
            values = (pay, name)
            cursor.execute("UPDATE employees SET pay = ? WHERE ?", values)
            connection.commit()
            if cursor.rowcount() == 0:
                print("Invalid name")
        except ValueError:
            print("Invalid pay")

    elif choice == "4":
        # Delete employee
        name = get_name(cursor)
        values = (name,)
        cursor.execute("DELETE FROM employees WHERE name = ?", values)
        connection.commit()
    print()

# Close the database connection before exiting
connection.close()