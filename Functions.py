import mysql.connector
import datetime
import pandas as pd


# Function to create the employee table with additional details
def create_employee_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                age INT,
                department VARCHAR(255),
                position VARCHAR(255),
                salary FLOAT,
                email VARCHAR(255),
                phone VARCHAR(20),
                hire_date DATE,
                address VARCHAR(255)
            )
        ''')
        # print("Employee table created successfully")
    except mysql.connector.Error as e:
        print(e)


# Function to add a new employee with additional details
def add_employee(name, age, department, position, salary, email, phone, hire_date, address,conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO employees (name, age, department, position, salary, email, phone, hire_date, address)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (name, age, department, position, salary, email, phone, hire_date, address))
        conn.commit()
        print("Employee added successfully")
    except mysql.connector.Error as e:
        print(e)


def get_employees_df(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM employees
        ''')
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]  # Get column names from cursor description
        df = pd.DataFrame(rows, columns=columns)
        return df
    except mysql.connector.Error as e:
        print(e)
        return None


# Function to delete an employee by ID
def delete_employee(conn, id):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM employees WHERE id = %s
        ''', (id,))
        conn.commit()
        print("Employee with ID {} deleted successfully.".format(id))
    except mysql.connector.Error as e:
        print(e)


# Function to empty (truncate) the entire employees table
def empty_employee_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            TRUNCATE TABLE employees
        ''')
        conn.commit()
        print("Employee table emptied successfully.")
    except mysql.connector.Error as e:
        print(e)


# Function to update an employee's details based on user input
def update_employee_details(conn, employee_id):
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM employees WHERE id = %s', (employee_id,))
        employee = cursor.fetchone()
        # print(type(employee))
        if employee:
            print("Employee details:")
            print("ID:", employee[0])
            print("Name:", employee[1])
            print("Age:", employee[2])
            print("Department:", employee[3])
            print("Position:", employee[4])
            print("Salary:", employee[5])
            print("Email:", employee[6])
            print("Phone:", employee[7])
            print("Hire Date:", employee[8])
            print("Address:", employee[9])

            field_to_update = input("Enter the field you want to update (name/age/department/position/salary/email/phone/hire_date/address): ").strip().lower()

            if field_to_update in ('name', 'age', 'department', 'position', 'salary', 'email', 'phone', 'hire_date', 'address'):
                new_value = input("Enter the new value for {}: ".format(field_to_update)).strip()
                cursor.execute('''
                    UPDATE employees
                    SET {} = %s
                    WHERE id = %s
                '''.format(field_to_update), (new_value, employee_id))
                conn.commit()
                print("Employee details updated successfully.")
            else:
                print("Invalid field.")
        else:
            print("Employee with ID {} not found.".format(employee_id))
    except mysql.connector.Error as e:
        print(e)


# Function to get employee details by ID
def get_employee_by_id(conn,id):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM employees WHERE id = %s
        ''', (id))
        row = cursor.fetchone()
        if row:
            print("Employee details:")
            print("ID:", row[0])
            print("Name:", row[1])
            print("Age:", row[2])
            print("Department:", row[3])
            print("Position:", row[4])
            print("Salary:", row[5])
            print("Email:", row[6])
            print("Phone:", row[7])
            print("Hire Date:", row[8])
            print("Address:", row[9])
        else:
            print("Employee with ID {} not found.".format(id))
    except mysql.connector.Error as e:
        print(e)

def get_employee_task(conn, emp_id):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM tasks WHERE assignee_id = %s
        ''', (emp_id,))
        tasks = cursor.fetchall()
        if not tasks:
            print("No tasks found for employee with ID {}.".format(emp_id))
            return
        print("Tasks for Employee ID {}: ".format(emp_id))
        for task in tasks:
            task_id, task_name, assignee_id, deadline, status = task
            print("Task ID: {}, Task Name: {}, Deadline: {}, Status: {}".format(task_id, task_name, deadline, status))
    except mysql.connector.Error as e:
        print("Error fetching tasks:", e)


 # leave request
class LeaveRequest:
    def __init__(self, emp_id, leave_type, start_date, end_date, status='Pending'):
        self.emp_id = emp_id
        self.leave_type = leave_type
        self.start_date = start_date
        self.end_date = end_date
        self.status = status

class LeaveManagementSystem:
    def __init__(self, conn):
        self.conn = conn

    def submit_leave_request(self, leave_request, days):
        try:
            cursor = self.conn.cursor()

            # Check CL and update leave status accordingly
            cursor.execute('''
                SELECT cl FROM employees WHERE id = %s
            ''', (leave_request.emp_id,))
            cl = cursor.fetchone()[0]

            if cl > days:
                leave_request.status = 'Approved'
                cl -= days
                cursor.execute('''
                    UPDATE employees SET cl = %s WHERE id = %s
                ''', (cl, leave_request.emp_id))
            else:
                leave_request.status = 'Rejected'

            # Insert leave request into leave_requests table
            cursor.execute('''
                INSERT INTO leave_requests (emp_id, leave_type, start_date, end_date, status)
                VALUES (%s, %s, %s, %s, %s)
            ''', (leave_request.emp_id, leave_request.leave_type, leave_request.start_date, leave_request.end_date, leave_request.status))

            self.conn.commit()
            print("Leave request submitted successfully")
        except mysql.connector.Error as e:
            print(e)

    def create_leave_request_table(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS leave_requests (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    emp_id INT,
                    leave_type VARCHAR(50),
                    start_date DATE,
                    end_date DATE,
                    status VARCHAR(20)
                )
            ''')
            self.conn.commit()
            # print("Leave requests table created successfully.")
        except mysql.connector.Error as e:
            print("Error creating leave requests table:", e)

# Main function
def leave_req(emp_id):
    # Create connection to MySQL database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="test"
    )
    if conn.is_connected():
        # print("Connected to MySQL database")

        # Initialize LeaveManagementSystem instance
        leave_system = LeaveManagementSystem(conn)

        # Create leave request table
        leave_system.create_leave_request_table()

        # Take inputs from the user
        # emp_id = int(input("Enter Employee ID: "))
        leave_type = input("Enter Leave Reason: ")
        start_date_str = input("Enter Start Date (YYYY-MM-DD): ")
        end_date_str = input("Enter End Date (YYYY-MM-DD): ")

        # Convert input strings to datetime objects
        start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()

        # Calculate the number of days
        num_days = (end_date - start_date).days

        # Create LeaveRequest object with num_days
        leave_request = LeaveRequest(emp_id, leave_type, start_date, end_date)

        # Submit leave request
        leave_system.submit_leave_request(leave_request, num_days)

        conn.close()
    else:
        print("Error! Cannot connect to MySQL database.")


class TaskManagementSystem:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="test"
        )
        self.create_task_table()

    def create_task_table(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    task_id INT AUTO_INCREMENT PRIMARY KEY,
                    task_name VARCHAR(255) NOT NULL,
                    assignee_id INT,
                    deadline DATE,
                    status VARCHAR(20)
                )
            ''')
            self.conn.commit()
            # print("Task table created successfully.")
        except mysql.connector.Error as e:
            print("Error creating task table:", e)

    def employee_exists(self, emp_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT * FROM employees WHERE id = %s
            ''', (emp_id,))
            if cursor.fetchone():
                return True
            else:
                print("Employee with ID {} does not exist.".format(emp_id))
                return False
        except mysql.connector.Error as e:
            print("Error checking employee existence:", e)
            return False

    def add_task(self, task_name, assignee_id, deadline):
        if not self.employee_exists(assignee_id):
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO tasks (task_name, assignee_id, deadline, status)
                VALUES (%s, %s, %s, %s)
            ''', (task_name, assignee_id, deadline, 'Pending'))
            self.conn.commit()
            print("Task added successfully.")
        except mysql.connector.Error as e:
            print("Error adding task:", e)

    def edit_task_status(self, task_id, new_status):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                UPDATE tasks
                SET status = %s
                WHERE task_id = %s
            ''', (new_status, task_id))
            self.conn.commit()
            print("Task status updated successfully.")
        except mysql.connector.Error as e:
            print("Error updating task status:", e)


    def get_employee_tasks(self, emp_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT * FROM tasks WHERE assignee_id = %s
            ''', (emp_id,))
            tasks = cursor.fetchall()
            if not tasks:
                print("No tasks found for employee with ID {}.".format(emp_id))
                return
            print("Tasks for Employee ID {}: ".format(emp_id))
            for task in tasks:
                task_id, task_name, assignee_id, deadline, status = task
                print("Task ID: {}, Task Name: {}, Deadline: {}, Status: {}".format(task_id, task_name, deadline, status))
        except mysql.connector.Error as e:
            print("Error fetching tasks:", e)

# Method to Manage Task
def task_Management():
    task_system = TaskManagementSystem()

    while True:
        print('Press 1 to assign task')
        print('Press 2 to update task status')
        print('Press 3 to view employee tasks')
        print('Press 4 to exit')
        choice = int(input('Enter your choice: '))

        if choice == 1:
            assignee_id = int(input("Enter assignee's employee ID: "))
            if not task_system.employee_exists(assignee_id):
                continue
            task_name = input("Enter task name: ")
            deadline = input("Enter deadline (YYYY-MM-DD): ")
            task_system.add_task(task_name, assignee_id, deadline)
        elif choice == 2:
            task_id = int(input("Enter task ID to update status: "))
            new_status = input("Enter new status: ")
            task_system.edit_task_status(task_id, new_status)
        elif choice == 3:
            emp_id = int(input("Enter employee ID to view tasks: "))
            if not task_system.employee_exists(emp_id):
                continue
            task_system.get_employee_tasks(emp_id)
        elif choice == 4:
            break
        else:
            print("Invalid choice. Please try again.")

#
# class TaskManagementSystem:
#     def __init__(self):
#         self.conn = mysql.connector.connect(
#             host="localhost",
#             user="root",
#             password="",
#             database="employees"
#         )
#
#
#     def employee_exists(self, emp_id):
#         try:
#             cursor = self.conn.cursor()
#             cursor.execute('''
#                 SELECT * FROM employees WHERE id = %s
#             ''', (emp_id,))
#             if cursor.fetchone():
#                 return True
#             else:
#                 print("Employee with ID {} does not exist.".format(emp_id))
#                 return False
#         except mysql.connector.Error as e:
#             print("Error checking employee existence:", e)
#             return False
#
#
#
#
#     def get_employee_tasks(self, emp_id):
#         try:
#             cursor = self.conn.cursor()
#             cursor.execute('''
#                 SELECT * FROM tasks WHERE assignee_id = %s
#             ''', (emp_id,))
#             tasks = cursor.fetchall()
#             if not tasks:
#                 print("No tasks found for employee with ID {}.".format(emp_id))
#                 return
#             print("Tasks for Employee ID {}: ".format(emp_id))
#             for task in tasks:
#                 task_id, task_name, assignee_id, deadline, status = task
#                 print("Task ID: {}, Task Name: {}, Deadline: {}, Status: {}".format(task_id, task_name, deadline, status))
#         except mysql.connector.Error as e:
#             print("Error fetching tasks:", e)
#
# # Main function
# def task_view(emp_id):
#     task_system = TaskManagementSystem()
#     if not task_system.employee_exists(emp_id):
#         return
#     task_system.get_employee_tasks(emp_id)


class AttendanceSystem:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="test"
        )
        self.create_attendance_table()

    def create_attendance_table(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS attendance (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    emp_id INT,
                    date DATE,
                    status VARCHAR(20)
                )
            ''')
            self.conn.commit()
            # print("Attendance table created successfully.")
        except mysql.connector.Error as e:
            print("Error creating attendance table:", e)

    def mark_attendance(self, emp_id):
        try:
            cursor = self.conn.cursor()
            today = datetime.date.today()

            # Check if attendance for the current date already exists
            cursor.execute('''
                SELECT * FROM attendance WHERE emp_id = %s AND date = %s
            ''', (emp_id, today))
            existing_attendance = cursor.fetchone()

            if existing_attendance:
                print("Attendance already marked for today.")
            else:
                cursor.execute('''
                    INSERT INTO attendance (emp_id, date, status)
                    VALUES (%s, %s, %s)
                ''', (emp_id, today, 'Present'))
                self.conn.commit()
                print("Attendance marked successfully.")
        except mysql.connector.Error as e:
            print("Error marking attendance:", e)

    def view_attendance(self, emp_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT date, status FROM attendance WHERE emp_id = %s
            ''', (emp_id,))
            attendance_records = cursor.fetchall()
            if not attendance_records:
                print("No attendance records found for employee with ID {}.".format(emp_id))
                return
            print("Attendance records for Employee ID {}: ".format(emp_id))
            for record in attendance_records:
                date, status = record
                print("Date: {}, Status: {}".format(date, status))
        except mysql.connector.Error as e:
            print("Error fetching attendance:", e)


def get_user_type():
    print("Are you an Employee or Admin?")
    while True:
        user_type = input("Enter 'Employee' or 'Admin': ").strip().lower()
        if user_type in ['employee', 'admin']:
            return user_type
        else:
            print("Invalid input. Please enter 'Employee' or 'Admin'.")

def signIn(user_id, password):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  # Replace with your MySQL password
            database="test"
        )
        cursor = conn.cursor()

        query = "SELECT position FROM login WHERE uname = %s AND password = %s"
        cursor.execute(query, (user_id, password))
        result = cursor.fetchone()

        return result  # Return user position if found, None otherwise
    except mysql.connector.Error as e:
        print(e)
        return None



