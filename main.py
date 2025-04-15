import mysql.connector

DATABASE_NAME = "Company"
USER_NAME = "root"
HOST_NAME = "localhost"
PASSWORD = ""


def connect_to_db():
    try:
        mydb = mysql.connector.connect(
        host=HOST_NAME,
        user=USER_NAME,
        password=PASSWORD,
        database=DATABASE_NAME
        )
    except Exception as e:
        print(e)
        return

    print(f"Now managing: {mydb.database}")
    return mydb


def main():
    print("Database Manager booting up...")
    connection = connect_to_db()
    menu(connection)
    print("\nTerminating Database Manger... Goodbye.")


def menu(connection):
    while True:
        print("\nEnter a value coresponding to the function of your choice")
        print("1. Add Employee")
        print("2. View Employee")
        print("3. Modify Employee")
        print("4. Remove Employee")
        print("5. Add Dependent")
        print("6. Remove Dependent")
        print("7. Add Department")
        print("8. View Department")
        print("9. Remove Department")
        print("10. Add Department Location")
        print("11. Remove Department Location")
        
        while True:
            try:
                func_select = int(input("\nEnter your choice (0-11): ").strip())
                if 0 <= func_select <= 11:
                    break
                else:
                    print("Invalid input: enter a number between 0 and 11.")
            except ValueError:
                print("Invalid input: enter a number between 0 and 11.")
                
        match func_select:
            case 1:
                add_employee(connection)
            case 2:
                view_employee(connection)
            case 3:
                modify_employee(connection)
            case 4:
                remove_employee(connection)
            case 5:
                add_dependent(connection)
            case 6:
                remove_dependent(connection)
            case 7:
                add_department(connection)
            case 8:
                view_department(connection)
            case 9:
                remove_department(connection)
            case 10:
                add_department_location(connection)
            case 11:
                remove_department_location(connection)
            case 0:
                return

    
def add_employee(connection):
    # create new employee entry with proper data constraints
    # check if_exsists, ensure data format is proper, and there are no referential constraints
    # add error messages
    pass

def view_employee(connection):
    # ask for mySSN
    # print all attributes of employee table
    # show supervisor name, department name and dependents
    pass

def modify_employee(connection):
    # ask for SSN
    # LOCK RECORD (***HOW?)
    # Display employee info (view_employee)
    # Allow user toupdate one or more of the following fields (address, sex, salary, super_ssn, Dno)
    pass

def remove_employee(connection):
    # ask for SSN
    # LOCK EMPLOYEE RECORD
    # Display employee info (view_employee)
    # ask for confirmation to delete
    # if confirmed = y, delete
    # if error, show warning message then ask to remove dependencies first
    pass

def add_dependent(connection):
    # ask for employee SSN
    # LOCK EMPLOYEE RECORD
    # show all dependents
    # ask for new dependent info
    # create ne wdependent record
    pass

def remove_dependent(connection):
    # ask for employee SSN
    # LOCK EMPLOYEE RECORD
    # show all dependents
    # ask for name of dependent to remove
    # remove dependent 
    pass

def add_department(connection):
    # ask for new department name and information
    # add new record
    # display error for constraint violations
    pass

def view_department(connection):
    # ask for Dnumber
    # show list of departments, manager names, and all department locations
    pass

def remove_department(connection):
    # ask for Dnumber
    # LOCK DEPARTMENT RECORD
    # show department information
    # ask for confirmation before delete
    # deete deprtment
    # print errors and ask them to remove dependencies
    pass

def add_department_location(connection):
    # ask for Dnumber
    # LOCK DEPARTMENT RECORD
    # show all locations
    # ask for new location
    # create new location record
    pass

def remove_department_location(connection):
    # ask for Dnumber
    # LOCK DEPARTMENT RECORD
    # show all loctions
    # ask for location to remove
    # confirm removal
    # delete location record
    pass 

if __name__ == "__main__":
    main()
