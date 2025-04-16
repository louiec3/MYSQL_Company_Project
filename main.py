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
        print("Connection failed...")
        print(e)
        return



    print(f"Now managing: {mydb.database}")
    return mydb


def main():
    print("Database Manager booting up...")
    connection = connect_to_db()
    menu(connection)
    print("\nTerminating Database Manager.")


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

    try:
        print("\nEnter new employee information:")
        fname = input("First Name: ").strip()
        minit = input("Middle Initial: ").strip()
        lname = input("Last Name: ").strip()
        ssn = input("SSN: ").strip()
        bdate = input("Birthdate (YYYY-MM-DD): ").strip()
        address = input("Address: ").strip()
        sex = input("Sex (M/F): ").strip().upper()
        salary = float(input("Salary: ").strip())
        super_ssn = input("Supervisor SSN (or leave blank): ").strip() or None
        dno = input("Department Number: ").strip()

        with connection.cursor() as cursor:
            # check if ssn  exists
            cursor.execute("SELECT * FROM employees WHERE Ssn = %s", (ssn,))
            if cursor.fetchone():
                print("Error: an employee with this SSN already exists.")
                return

            # check if supervisor ssn exists
            if super_ssn:
                cursor.execute("SELECT * FROM employees WHERE Ssn = %s", (super_ssn,))
                if not cursor.fetchone():
                    print("Error: supervisor SSN does not exist.")
                    return

            # check if department number exists
            cursor.execute("SELECT * FROM department WHERE Dnumber = %s", (dno,))
            dept = cursor.fetchone()
            if not dept:
                print("Error: department number does not exist.")
                return

            cursor.execute("""
                INSERT INTO employees (Fname, Minit, Lname, Ssn, Bdate, Address, Sex, Salary, Super_ssn, Dno)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (fname, minit, lname, ssn, bdate, address, sex, salary, super_ssn, dno))

            connection.commit()

            print("\nEmployee added successfully.")

            print("\nEmployee Information:")
            print(f"First Name     : {fname}")
            print(f"Middle Initial : {minit}")
            print(f"Last Name      : {lname}")
            print(f"SSN            : {ssn}")
            print(f"Birthdate      : {bdate}")
            print(f"Address        : {address}")
            print(f"Sex            : {sex}")
            print(f"Salary         : ${salary:,.2f}")
            print(f"Supervisor SSN : {super_ssn if super_ssn else 'None'}")
            print(f"Department No. : {dno}")
            print(f"Department     : {dept[0]}")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    except ValueError:
        print("Invalid input. Salary must be a number.")


def view_employee(connection):
    # ask for mySSN
    # print all attributes of employee table
    # show supervisor name, department name and dependents

    ssn = input("Enter the employee's SSN: ").strip()
    try:
        with connection.cursor() as cursor:
            # get employee attributes, department supervisor info
            cursor.execute("""
                SELECT 
                    e.Fname, e.Minit, e.Lname, e.Ssn, e.Bdate, e.Address, e.Sex, e.Salary,
                    e.Super_ssn, e.Dno,
                    d.Dname AS Department,
                    s.Fname AS SupervisorFname, s.Lname AS SupervisorLname
                FROM employees e
                LEFT JOIN department d ON e.Dno = d.Dnumber
                LEFT JOIN employees s ON e.Super_ssn = s.Ssn
                WHERE e.Ssn = %s
            """, (ssn,))
            row = cursor.fetchone()

            if not row:
                print("Employee not found.")
                return

            print("\nEmployee Information:")
            print(f"First Name     : {row[0]}")
            print(f"Middle Initial : {row[1]}")
            print(f"Last Name      : {row[2]}")
            print(f"SSN            : {row[3]}")
            print(f"Birthdate      : {row[4]}")
            print(f"Address        : {row[5]}")
            print(f"Sex            : {row[6]}")
            print(f"Salary         : ${row[7]:,.2f}")
            print(f"Supervisor SSN : {row[8]}")
            print(f"Department No. : {row[9]}")
            print(f"Department     : {row[10]}")
            print(f"Supervisor     : {row[11]} {row[12]}")

            # get dependents
            cursor.execute("SELECT Dependent_name FROM dependent WHERE Essn = %s", (ssn,))
            dependents = cursor.fetchall()
            print("Dependents:")
            if not dependents:
                print("None")
            else:
                dep_names = [dep[0] for dep in dependents]
                print(", ".join(dep_names))


    except mysql.connector.Error as err:
        print(f"Error: {err}")
    

def modify_employee(connection):
    # ask for SSN
    try:
        ssn = input("Enter SSN of employee to modify: ").strip()

        with connection.cursor() as cursor:
            # LOCK RECORD
            cursor.execute("SELECT * FROM employees WHERE Ssn = %s FOR UPDATE", (ssn,))
            row = cursor.fetchone()
            if not row:
                print("Employee not found.")
                return

            # Display employee info (view_employee)
            print("\nCurrent Employee Information:")
            print(f"First Name     : {row[0]}")
            print(f"Middle Initial : {row[1]}")
            print(f"Last Name      : {row[2]}")
            print(f"SSN            : {row[3]}")
            print(f"Birthdate      : {row[4]}")
            print(f"Address        : {row[5]}")
            print(f"Sex            : {row[6]}")
            print(f"Salary         : ${row[7]:,.2f}")
            print(f"Supervisor SSN : {row[8]}")
            print(f"Department No. : {row[9]}")

            # Allow user to update one or more of the following fields (address, sex, salary, super_ssn, Dno)
            new_address = input("New Address (leave blank to keep current): ").strip() or row[5]
            new_sex = input("New Sex (M/F) (leave blank to keep current): ").strip().upper() or row[6]
            try:
                new_salary_input = input("New Salary (leave blank to keep current): ").strip()
                new_salary = float(new_salary_input) if new_salary_input else row[7]
            except ValueError:
                print("Invalid salary input.")
                return

            new_super_ssn = input("New Supervisor SSN (leave blank to keep current): ").strip() or row[8]
            new_dno = input("New Department Number (leave blank to keep current): ").strip() or row[9]

            # check if supervisor exists
            if new_super_ssn:
                cursor.execute("SELECT * FROM employees WHERE Ssn = %s", (new_super_ssn,))
                if not cursor.fetchone():
                    print("Error: Supervisor SSN does not exist.")
                    return

            # check if department exists
            cursor.execute("SELECT * FROM department WHERE Dnumber = %s", (new_dno,))
            if not cursor.fetchone():
                print("Error: Department number does not exist.")
                return

            # excute use update
            cursor.execute("""
                UPDATE employees
                SET Address = %s,
                    Sex = %s,
                    Salary = %s,
                    Super_ssn = %s,
                    Dno = %s
                WHERE Ssn = %s
            """, (new_address, new_sex, new_salary, new_super_ssn, new_dno, ssn))

            connection.commit()
            print("\nEmployee record updated successfully")

    except mysql.connector.Error as err:
        print(f"Error: {err}")




def remove_employee(connection):
    # ask for SSN
    # LOCK EMPLOYEE RECORD
    # Display employee info (view_employee)
    # ask for confirmation to delete
    # if confirmed = y, delete
    # if error, show warning message then ask to remove dependencies first

    ssn = input("Enter SSN of employee to remove: ").strip()

    try:
        connection.start_transaction()
        with connection.cursor() as cursor:
            # LOCK EMPLOYEE RECORD
            cursor.execute("SELECT * FROM employees WHERE Ssn = %s FOR UPDATE", (ssn,))
            row = cursor.fetchone()

            if not row:
                print("Error: Employee not found.")
                connection.rollback() # unlock
                return

            # Display employee info (view_employee)
            print("\nEmployee Information:")
            print(f"First Name     : {row[0]}")
            print(f"Middle Initial : {row[1]}")
            print(f"Last Name      : {row[2]}")
            print(f"SSN            : {row[3]}")
            print(f"Birthdate      : {row[4]}")
            print(f"Address        : {row[5]}")
            print(f"Sex            : {row[6]}")
            print(f"Salary         : ${row[7]:,.2f}")
            print(f"Supervisor SSN : {row[8]}")
            print(f"Department No. : {row[9]}")

            confirm = input("\nAre you sure you want to delete this employee? (y/n): ").strip().lower()
            if confirm != 'y':
                print("Cancelled.")
                connection.rollback() # unlock
                return

            # deete employee record
            try:
                cursor.execute("DELETE FROM employees WHERE Ssn = %s", (ssn,))
                connection.commit()
                print("Employee successfully removed.")
            except mysql.connector.Error as err:
                print("Error occurred during deletion.")
                print(f"Reason: {err}")
                print("You may need to remove dependent records (e.g., dependents, works_on) first.")
                connection.rollback() # unlock

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        connection.rollback() # unlock

def add_dependent(connection):
    # ask for employee SSN
    # LOCK EMPLOYEE RECORD
    # show all dependents
    # ask for new dependent info
    # create ne wdependent record

    # ask for employee SSN
    ssn = input("Enter the SSN of the employee to add a dependent for: ").strip()

    try:
        connection.start_transaction()
        with connection.cursor() as cursor:
            # LOCK EMPLOYEE RECORD
            cursor.execute("SELECT * FROM employees WHERE Ssn = %s FOR UPDATE", (ssn,))
            employee = cursor.fetchone()
            if not employee:
                print("Employee not found.")
                connection.rollback() # unlock
                return

            # show all dependents
            cursor.execute("SELECT Dependent_name FROM dependent WHERE Essn = %s", (ssn,))
            dependents = cursor.fetchall()
            print("\nCurrent Dependents:")
            if not dependents:
                print("None")
            else:
                dep_names = [dep[0] for dep in dependents]
                print(", ".join(dep_names))

            # ask for new dependent info
            name = input("\nEnter new dependent's name: ").strip()
            sex = input("Sex (M/F): ").strip().upper()
            bdate = input("Birthdate (YYYY-MM-DD): ").strip()
            relationship = input("Relationship: ").strip()

            # check if dependent already exists
            cursor.execute("SELECT * FROM dependent WHERE Essn = %s AND Dependent_name = %s", (ssn, name))
            if cursor.fetchone():
                print("A dependent with this name already exists for this employee.")
                connection.rollback() # unlock
                return

            # create new dependent record
            cursor.execute("""
                INSERT INTO dependent (Essn, Dependent_name, Sex, Bdate, Relationship)
                VALUES (%s, %s, %s, %s, %s)
            """, (ssn, name, sex, bdate, relationship))
            connection.commit()
            print("Dependent added successfully.")

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        connection.rollback() # unlock


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
