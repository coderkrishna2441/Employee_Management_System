import Functions as f
import mysql.connector

def main():
    conn = None
    try:
        conn = mysql.connector.connect(host="localhost", user="root", password="", database="test")
        if conn.is_connected():
            print("Connected to MySQL database")
            print("----------------------------------------------------------")
            # Ask for user position and password
            while True:
                user_id = input("Enter your ID or For exit type exit: ").strip()
                print("----------------------------------------------------------")
                if user_id=='exit':
                    print("exiting...")
                    break
                password = input("Enter password: ")
                print("----------------------------------------------------------")

                # Attempt to sign in using the provided credentials
                login_result = f.signIn(user_id, password)
                # Check the result of login attempt
                if login_result is not None:
                        print("Welcome,", login_result[0])  # Print user position
                        print("---------------------------------------------------")
                        while True:
                            if login_result[0] == "Admin":
                                print("1. Add a Employee\n2. show all Employee details\n3. Delete an employee\n4. Delete all employee data\n5.Update details of a employee\n6.show employee details\n7. Manage Tasks\n8. Mark Attendence\n9. View Attendence \n10. Exit")
                                print("----------------------------------------------------------")
                                choice = int(input("Enter the choice of action: "))
                                print("----------------------------------------------------------")
                                if choice == 1:
                                    name = input("Enter the name of the employee: ")
                                    print("----------------------------------------------------------")
                                    age = int(input("Enter the age of the employee: "))
                                    print("----------------------------------------------------------")
                                    department = input("Enter the department of the employee: ")
                                    print("----------------------------------------------------------")
                                    position = "Employee"
                                    salary = float(input("Enter the salary of the employee: "))
                                    print("----------------------------------------------------------")
                                    email = input("Enter the email of the employee: ")
                                    print("----------------------------------------------------------")
                                    phone = input("Enter the mobile number of the employee: ")
                                    print("----------------------------------------------------------")
                                    hire_date = input("Enter the hire date of the employee in YYYY/DD/MM: ")
                                    print("----------------------------------------------------------")
                                    address = input("Enter the address of the employee: ")
                                    print("----------------------------------------------------------")
                                    f.add_employee(name, age, department, position, salary, email, phone, hire_date, address, conn)
                                    # print("Employee added successfully!")
                                    print("----------------------------------------------------------")
                                elif choice == 2:
                                    employees_df = f.get_employees_df(conn)
                                    print(employees_df)
                                elif choice == 3:
                                    id = input("Enter the ID of the employee you want to delete: ")
                                    f.delete_employee(conn, int(id))
                                elif choice == 4:
                                    f.empty_employee_table(conn)
                                elif choice == 5:
                                    id = input("Enter the ID of the employee to update details: ")
                                    f.update_employee_details(conn, int(id))
                                elif choice == 6:
                                    id = input("Enter the ID of the employee: ")
                                    f.get_employee_by_id(conn, [id])
                                elif choice == 7:
                                    f.task_Management()
                                elif choice == 8:
                                    attendance_system = f.AttendanceSystem()
                                    x = int(input('Enter employees id to mark present'))
                                    attendance_system.mark_attendance(x)
                                elif choice == 9:
                                    attendance_system = f.AttendanceSystem()
                                    x = int(input('Enter employees id to view attandance'))
                                    attendance_system.view_attendance(x)
                                elif choice == 10:
                                    break
                                else:
                                    print("Enter a valid choice from the menu")
                            else:
                                print(
                                    "1. view your tasks\n2. set a leave request\n3. view attandance\n4. Exit")
                                print("----------------------------------------------------------")
                                choice = int(input("Enter the choice of action: "))
                                print("----------------------------------------------------------")
                                if choice == 1:
                                    f.get_employee_task(conn,user_id)
                                elif choice == 2:
                                    f.leave_req(user_id)
                                elif choice == 3:
                                    attendance_system = f.AttendanceSystem()
                                    attendance_system.view_attendance(user_id)
                                elif choice == 4:
                                    break
                
                
                
                else:
                    # Failed login, print error message
                    print("Login failed. Incorrect password or user position.")
    except mysql.connector.Error as e:
        print("Error:", e)
    finally:
        if conn is not None and conn.is_connected():
            conn.close()

if __name__ == "__main__":
    main()
