import mysql.connector

sq=input('Enter mysql password: ')
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password='tiger'
)

cursor = db.cursor()
try:
    cursor.execute('create database school')
except:
    pass
cursor.execute('use School')
try:
    cursor.execute('create table students(admn int primary key, name varchar(30),feespaid int, feesdue int, due date)')             
except:
    pass

def addrecord():
    print("Add a new Record")
    print("================")
    
    admin = input('Enter admission number: ')
    name = input('Enter name: ')
    feesdue = input('Enter fees due: ')
    feespaid = input('Enter fees paid already: ')
    due = input('Enter due date: ')
    
    sql = "INSERT INTO students (admn, name, feespaid, feesdue, due) VALUES (%s, %s, %s, %s, %s)"
    values = (admin, name, feespaid, feesdue, due)

    cursor.execute(sql, values)
    db.commit()

    print("Record Saved")
    input("Press any key to continue..")

def modifyrecord():
    print("Modify a Record")
    print("================")
    
    rollno = input('Enter admission number you want to modify: ')
    
    cursor.execute("SELECT * FROM students WHERE admn = %s", (rollno,))
    record = cursor.fetchone()

    if record:
        print("Admission no. =", record[0])
        print("Name =", record[1])
        print("Fees due =", record[2])
        choice = input("Do you want to modify this record (y/n): ")

        if choice.lower() == 'y':
            new_rollno = input('Enter New rollno: ')
            new_name = input('Enter new name: ')
            new_fees = input('Enter new fees: ')

            sql = "UPDATE students SET admn = %s, name = %s, feesdue = %s WHERE admn = %s"
            values = (new_rollno, new_name, new_fees, rollno)

            cursor.execute(sql, values)
            db.commit()

            print("Record Modified")
        else:
            print("Record not modified")
    else:
        print("Record not found")

    input("Press any key to continue..")

def deleterecord():
    print("Delete a Record")
    print("================")
    
    rollno = input('Enter admission number you want to delete: ')
    
    cursor.execute("SELECT * FROM students WHERE admn = %s", (rollno,))
    record = cursor.fetchone()

    if record:
        print("Rollno =", record[0])
        print("Name =", record[1])
        print("fees =", record[2])
        choice = input("Do you want to delete this record (y/n): ")

        if choice.lower() == 'y':
            sql = "DELETE FROM students WHERE admn = %s"
            cursor.execute(sql, (rollno,))
            db.commit()

            print("Record Deleted")
        else:
            print("Record not deleted")
    else:
        print("Record not found")

    input("Press any key to continue..")

def search():
    print("Search a Record")
    print("===================")
    
    rollno = input('Enter admission number you want to search: ')
    
    cursor.execute("SELECT * FROM students WHERE admn = %s", (rollno,))
    record = cursor.fetchone()

    if record:
        print("Rollno =", record[0])
        print("Name =", record[1])
        print("fees =", record[2])
    else:
        print("Record not found")

    input("Press any key to continue..")

def viewall():
    print("List of All Records")
    print("===================")
    
    cursor.execute("SELECT * FROM students")
    records = cursor.fetchall()

    for record in records:
        print({record[0]},'\t\t',{record[1]},'\t\t',{record[2]},{record[3]},'\t\t',{record[4]})

    input("Press any key to continue..")

def admn():
    choice = 0
    while choice != 6:
        print("\n")
        print("Main Menu")
        print("~~~~~~~~~~~~")
        print("1. Add a new Record")
        print("2. Modify Existing Record")
        print("3. Delete Existing Record")
        print("4. Search a Record")
        print("5. List all Records")
        print("6. Exit")
        choice = int(input('Enter your choice: '))

        if choice == 1:
            addrecord()
        elif choice == 2:
            modifyrecord()
        elif choice == 3:
            deleterecord()
        elif choice == 4:
            search()
        elif choice == 5:
            viewall()
        elif choice == 6:
            print("Software Terminated")

def pay_fees(username):
    # Check if the student exists in the database
    cursor.execute("SELECT * FROM students WHERE admn = %s", (username,))
    student = cursor.fetchone()
    x=student[3]
    if student is None:
        print("Student not found.")
    else:
        # Check if there are fees due
        if student[3] == 0:
            print("No fees are due for this student.")
        else:
            cursor.execute("UPDATE students SET feesdue = 0, due = NULL WHERE admn = %s", (username,))
            print(f"Payment successful. All fees are cleared.")
            cursor.execute("UPDATE students SET feespaid = %s WHERE admn = %s", (x,username))
            db.commit()       

def mainmenu(x):
    choice = 0
    print(x)
    while choice != 3:
        print("\n")
        print("Main Menu")
        print("~~~~~~~~~~~~")
        print("1. Search a Record")
        print('2. Pay due fees')
        print("3. Exit")
        choice = int(input('Enter your choice: '))
        if choice == 1:
            search()
        elif choice == 2:
            pay_fees(x)
        elif choice == 3:
            print("Software Terminated") 


    

# Sample user database stored as a dictionary

user_db = {}

def login():
    print("Welcome to the School Database Fee System")
    while True:
        print("1. Log in")
        print("2. Quit")
        choice = input("Enter your choice (1/2): ")

        if choice == '1':
            username = input("Enter your username: ")#aadittayan
            password = int(input("Enter your password: "))#2
            if username=='admin' and password=='admnpasswd':
                admn()
                continue
            cursor.execute("SELECT * FROM students WHERE admn = %s", (password,))
            admno = cursor.fetchone()
            s=int(admno[0])
            user_db[admno[1]] = s

            if user_db[username] == password:
                print("Login successful!")
                z=password
                mainmenu(z)
                # You can add your code to access the school database for fees here
            else:
                print("Invalid username or password. Please try again.")
        elif choice == '2':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")

def register():
    print("User Registration")
    while True:
        username = input("Enter a new username: ")
        if username in user_db:
            print("Username already exists. Please choose another.")
            continue
        password = input("Enter a password: ")
        user_db[username] = password
        print("Registration successful!")
        break

if __name__ == '__main__':
    login()

# Close the cursor and connection when done
cursor.close()
db.close()
