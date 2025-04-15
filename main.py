def main():
    print("Database Manager booting up...")
    print("Now managing (DATABASE_NAME)")

    while True:
        print("Enter a value coresponding to the function of your choice")
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
        
        func_select = int((input("\nEnter your choice (1-11): ").strip()))

        match func_select:
            case 1:
                add_employee()
            case 2:
                view_employee()
            case 3:
                modify_employee()
            case 4:
                remove_employee()
            case 5:
                add_dependent()
            case 6:
                remove_dependent()
            case 7:
                add_department()
            case 8:
                view_department()
            case 9:
                remove_department()
            case 10:
                add_department_location()
            case 11:
                remove_department_location()
            case 0:
                print("\nTerminating Database Manger... Goodbye.")
                return

    

def add_employee():
    # create new employee entry with proper data constraints
    # check if_exsists, ensure data format is proper, and there are no referential constraints
    # add error messages
    pass

def view_employee():
    # ask for mySSN
    # print all attributes of employee table
    # show supervisor name, department name and dependents
    pass

def modify_employee():
    # ask for SSN
    # LOCK RECORD (***HOW?)
    # Display employee info (view_employee)
    # Allow user toupdate one or more of the following fields (address, sex, salary, super_ssn, Dno)
    pass

def remove_employee():
    # ask for SSN
    # LOCK EMPLOYEE RECORD
    # Display employee info (view_employee)
    # ask for confirmation to delete
    # if confirmed = y, delete
    # if error, show warning message then ask to remove dependencies first
    pass

def add_dependent():
    # ask for employee SSN
    # LOCK EMPLOYEE RECORD
    # show all dependents
    # ask for new dependent info
    # create ne wdependent record
    pass

def remove_dependent():
    # ask for employee SSN
    # LOCK EMPLOYEE RECORD
    # show all dependents
    # ask for name of dependent to remove
    # remove dependent 
    pass

def add_department():
    # ask for new department name and information
    # add new record
    # display error for constraint violations
    pass

def view_department():
    # ask for Dnumber
    # show list of departments, manager names, and all department locations
    pass

def remove_department():
    # ask for Dnumber
    # LOCK DEPARTMENT RECORD
    # show department information
    # ask for confirmation before delete
    # deete deprtment
    # print errors and ask them to remove dependencies
    pass

def add_department_location():
    # ask for Dnumber
    # LOCK DEPARTMENT RECORD
    # show all locations
    # ask for new location
    # create new location record
    pass

def remove_department_location():
    # ask for Dnumber
    # LOCK DEPARTMENT RECORD
    # show all loctions
    # ask for location to remove
    # confirm removal
    # delete location record
    pass 

if __name__ == "__main__":
    main()