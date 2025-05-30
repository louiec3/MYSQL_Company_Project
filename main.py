# Louis Cundari III
# Project 2: Database

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
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                (fname, minit, lname, ssn, bdate, address, sex, salary, super_ssn, dno))

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
                WHERE e.Ssn = %s""", (ssn,))
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

            confirm = input("\nConfirm employee delete? (y/n): ").strip().lower()
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
                print("You may to remove related records first (employees, department, dependents, works_on, etc...).")
                connection.rollback() # unlock

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        connection.rollback() # unlock

def add_dependent(connection):
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
    ssn = input("Enter the SSN of the employee: ").strip()
                                                    
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
            if not dependents:
                print("This employee has no dependents.")
                connection.rollback() # unlock
                return

            dep_names = [dep[0] for dep in dependents]
            print("\nCurrent Dependents:")
            print(", ".join(dep_names))

            # ask for name of dependent to remove
            name = input("Enter the name of the dependent to remove: ").strip()

            if name not in dep_names:
                print("No such dependent found for this employee.")
                connection.rollback() # unlock
                return

            # remove dependent
            cursor.execute("DELETE FROM dependent WHERE Essn = %s AND Dependent_name = %s", (ssn, name))
            connection.commit()
            print("Dependent removed successfully.")

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        connection.rollback() # unlock
    pass

def add_department(connection):
    # ask for new department name and information
    # add new record
    # display error for constraint violations
    
    dept_name = input("Enter new department name: ").strip()
    dept_number = input("Enter new department number: ").strip()
    manager_ssn = input("Enter manager SSN: ").strip()
    manager_start_date = input("Enter manager start date (YYYY-MM-DD): ").strip()

    try:
        with connection.cursor() as cursor:
            # check if department number already exists
            cursor.execute("SELECT * FROM department WHERE Dnumber = %s", (dept_number,))
            if cursor.fetchone():
                print("A department with this number already exists.")
                return

            # check if manager SSN exists
            cursor.execute("SELECT * FROM employees WHERE Ssn = %s", (manager_ssn,))
            if not cursor.fetchone():
                print("Manager SSN does not exist in the employees table.")
                return

            # add new record
            cursor.execute("""
                INSERT INTO department (Dname, Dnumber, Mgr_ssn, Mgr_start_date)
                VALUES (%s, %s, %s, %s)
            """, (dept_name, dept_number, manager_ssn, manager_start_date))

            connection.commit()
            print("Department added successfully.")

    except mysql.connector.Error as err:
        print("MySQL Error:", err)


def view_department(connection):
    # ask for department number
    dept_number = input("Enter department number: ").strip()

    try:
        with connection.cursor() as cursor:
            # Retrieve department and manager info
            cursor.execute("""
                SELECT 
                    d.Dname,
                    d.Dnumber,
                    e.Fname,
                    e.Minit,
                    e.Lname
                FROM department d
                LEFT JOIN employees e ON d.Mgr_ssn = e.Ssn
                WHERE d.Dnumber = %s
            """, (dept_number,))
            dept = cursor.fetchone()

            if not dept:
                print("Department not found.")
                return

            print("\nDepartment Information:")
            print(f"Department Name : {dept[0]}")
            print(f"Department No.  : {dept[1]}")
            print(f"Manager         : {dept[2]} {dept[3]} {dept[4]}")

            # Retrieve department locations
            cursor.execute("SELECT Dlocation FROM dept_locations WHERE Dnumber = %s", (dept_number,))
            locations = cursor.fetchall()
            print("Locations       : ", end="")

            if not locations:
                print("None")
            else:
                loc_names = [loc[0] for loc in locations]
                print(", ".join(loc_names))

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")


def remove_department(connection):
    # ask for Dnumber
    dnumber = input("Enter the department number to remove: ").strip()
    
    try:
        connection.start_transaction()
        with connection.cursor() as cursor:
            # LOCK DEPARTMENT RECORD
            cursor.execute("SELECT * FROM department WHERE Dnumber = %s FOR UPDATE", (dnumber,))
            dept = cursor.fetchone()

            if not dept:
                print("Department not found.")
                connection.rollback()
                return

            # show department information
            cursor.execute("""
                SELECT 
                    d.Dname,
                    d.Dnumber,
                    e.Fname,
                    e.Minit,
                    e.Lname
                FROM department d
                LEFT JOIN employees e ON d.Mgr_ssn = e.Ssn
                WHERE d.Dnumber = %s
            """, (dnumber,))
            row = cursor.fetchone()

            print("\nDepartment Information:")
            print(f"Department Name : {row[0]}")
            print(f"Department No.  : {row[1]}")
            print(f"Manager         : {row[2]} {row[3]} {row[4]}")

            # ask for confirmation before delete
            confirm = input("\nConfirm department delete? (y/n): ").strip().lower()
            if confirm != 'y':
                print("Cancelled.")
                connection.rollback() # unlock
                return

            # delete department
            try:
                cursor.execute("DELETE FROM department WHERE Dnumber = %s", (dnumber,))
                connection.commit()
                print("Department successfully removed.")

            except mysql.connector.Error as err:
                print(f"Error: {err}")
                print("You need to remove employees, projects, or location records first.")
                connection.rollback() # unlock

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        connection.rollback() # unlock


def add_department_location(connection):
    # ask for Dnumber
    dnumber = input("Enter the department number: ").strip()

    try:
        connection.start_transaction()
        with connection.cursor() as cursor:
            # LOCK DEPARTMENT RECORD
            cursor.execute("SELECT * FROM department WHERE Dnumber = %s FOR UPDATE", (dnumber,))
            dept = cursor.fetchone()
            if not dept:
                print("Department not found.")
                connection.rollback() # unlock
                return

            # show all locations
            cursor.execute("SELECT Dlocation FROM dept_locations WHERE Dnumber = %s", (dnumber,))
            locations = cursor.fetchall()
            print("\nCurrent Locations:")
            if not locations:
                print("None")
            else:
                location_names = [loc[0] for loc in locations]
                print(", ".join(location_names))

            # ask for new location
            new_location = input("Enter new location to add: ").strip()

            # check if location already exists
            if new_location in location_names:
                print("This location already exists for the department.")
                connection.rollback() # unlcok
                return

            # create new location record
            cursor.execute("""
                INSERT INTO dept_locations (Dnumber, Dlocation)
                VALUES (%s, %s)
            """, (dnumber, new_location))
            connection.commit()
            print("Location added successfully.")

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        connection.rollback()


def remove_department_location(connection):
    # or Dnumber
    dnumber = input("Enter the department number: ").strip()

    try:
        connection.start_transaction()
        with connection.cursor() as cursor:
            # LOCK DEPARTMENT RECORD
            cursor.execute("SELECT * FROM department WHERE Dnumber = %s FOR UPDATE", (dnumber,))
            dept = cursor.fetchone()
            if not dept:
                print("Department not found.")
                connection.rollback()
                return

            # show all locations
            cursor.execute("SELECT Dlocation FROM dept_locations WHERE Dnumber = %s", (dnumber,))
            locations = cursor.fetchall()
            location_names = [loc[0] for loc in locations]

            print("\nCurrent Locations:")
            if not location_names:
                print("None")
                connection.rollback()
                return
            else:
                print(", ".join(location_names))

            # ask for location to remove
            location_to_remove = input("Enter the location to remove: ").strip()

            if location_to_remove not in location_names:
                print("Location not found for this department.")
                connection.rollback()
                return

            # confirm removal
            confirm = input(f"Are you sure you want to remove '{location_to_remove}'? (y/n): ").strip().lower()
            if confirm != 'y':
                print("Cancelled.")
                connection.rollback()
                return

            # delete location record
            cursor.execute("""
                DELETE FROM dept_locations
                WHERE Dnumber = %s AND Dlocation = %s
            """, (dnumber, location_to_remove))
            connection.commit()
            print("Location removed successfully.")

    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
        connection.rollback()

if __name__ == "__main__":
    main()