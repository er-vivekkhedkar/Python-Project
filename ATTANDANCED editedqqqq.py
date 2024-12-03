from tkinter import ttk
from tkinter import *
import tkinter as tk
import tkinter.messagebox as tkMessageBox
import sqlite3
from datetime import datetime, timedelta
from pytz import timezone
from calendar import monthrange
from tkcalendar import Calendar

root = Tk()
root.title("Python: Online Attendance System")

width = 1000
height = 700
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width / 2) - (width / 2)
y = (screen_height / 2) - (height / 2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)

USERNAME = StringVar()
PASSWORD = StringVar()
FIRSTNAME = StringVar()
LASTNAME = StringVar()

STUDENTNAME = StringVar()
REGNO = StringVar()
var = IntVar()

selected_date = StringVar()

attendance_data = []  # List to store attendance data

def Database():
    global conn, cursor
    conn = sqlite3.connect("db_member3.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS 'MEMBER'(mem_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "
                   "username TEXT, password TEXT, firstname TEXT , lastname TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS students (stud_no INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "
                   "Studentname TEXT , rollno TEXT, var TEXT, date TEXT)")

    # Insert default user for testing purposes
    cursor.execute("INSERT INTO 'MEMBER' (username, password, firstname, lastname) VALUES (?, ?, ?, ?)",
                   ("admin", "admin123", "Admin", "User"))
    conn.commit()


def Exit():
    result = tkMessageBox.askquestion('System', 'Are You Sure You Want Exit', icon="warning")
    if result == 'yes':
        root.destroy()
        exit()
def LoginForm():
    global LoginFrame, lbl_result1
    LoginFrame = Frame(root)
    LoginFrame.pack(side=TOP, pady=80)

    title = Label(LoginFrame, text="Teacher Login", fg="#333333", font=('arial', 30,'bold'))
    title.grid(row=0, columnspan=2,pady=5)

    lbl_username = Label(LoginFrame, text="Username:", font=('Arial', 20), fg="#333333")
    lbl_username.grid(row=1, sticky="e", padx=5)

    lbl_password = Label(LoginFrame, text="Password:", font=('Arial', 20), fg="#333333")
    lbl_password.grid(row=2, sticky="e", padx=11,pady=5)

    lbl_result1 = Label(LoginFrame, text="", font=('arial', 10))
    lbl_result1.grid(row=3, columnspan=2)

    username = Entry(LoginFrame, font=('arial', 20), textvariable=USERNAME, width=15)
    username.grid(row=1, column=1)

    password = Entry(LoginFrame, font=('arial', 20), textvariable=PASSWORD, width=15, show="*")
    password.grid(row=2, column=1)

    btn_login = Button(LoginFrame, text="Login", font=('Arial', 16, 'bold'), width=15, command=Login, bg='#007bff', fg='white', bd=3, relief=RAISED)

    btn_login.grid(row=4, columnspan=2, pady=20)

    lbl_register = Label(LoginFrame, text="CREATE ACCOUNT", fg="Blue", font=('arial', 10))
    lbl_register.grid(row=5, columnspan=2)
    lbl_register.bind('<Button-1>', ToggleToRegister)


def RegisterForm():
    global RegisterFrame, lbl_result2
    RegisterFrame = Frame(root)
    RegisterFrame.pack(side=TOP, pady=40)

    title1 = Label(RegisterFrame, text="REGISTRATION FORM", fg="#333334", font=('arial', 20,'bold'))
    title1.grid(row=0, columnspan=2)

    lbl_username = Label(RegisterFrame,text="Username:", font=('Arial', 20), fg="#333333")
    lbl_username.grid(row=1, sticky="e", padx=10,pady=5)

    lbl_password = Label(RegisterFrame, text="Password:", font=('Arial', 20), fg="#333333")
    lbl_password.grid(row=2, sticky="e", padx=10,pady=5)

    lbl_firstname = Label(RegisterFrame, text="Firstname", font=('Arial', 20), fg="#333333")
    lbl_firstname.grid(row=3, sticky="e", padx=10,pady=5)

    lbl_lastname = Label(RegisterFrame, text="Lastname", font=('Arial', 20), fg="#333333")
    lbl_lastname.grid(row=4, sticky="e", padx=10,pady=5)

    username = Entry(RegisterFrame, font=('arial', 20), textvariable=USERNAME, width=15)
    username.grid(row=1, column=1)

    password = Entry(RegisterFrame, font=('arial', 20), textvariable=PASSWORD, width=15, show="*")
    password.grid(row=2, column=1)

    firstname = Entry(RegisterFrame, font=('arial', 20), textvariable=FIRSTNAME, width=15)
    firstname.grid(row=3, column=1)

    lastname = Entry(RegisterFrame, font=('arial', 20), textvariable=LASTNAME, width=15)
    lastname.grid(row=4, column=1)

    btn_login = Button(RegisterFrame, text="Register", font=('arial', 16,'bold'), width=15, command=Register,bg='#007bff',fg='white', bd=3, relief=RAISED)
    btn_login.grid(row=6, columnspan=2, pady=20)

    lbl_result2 = Label(RegisterFrame, text="", font=('arial', 10))
    lbl_result2.grid(row=7, columnspan=2)
    lbl_login = Label(RegisterFrame, text="Go To Login Form", fg="Blue", font=('arial', 15))
    lbl_login.grid(row=8, columnspan=2)
    lbl_login.bind('<Button-1>', ToggleToLogin)


def attendanceForm():
    global attendanceFrame, lbl_result3, cal
    attendanceFrame = Frame(root)
    attendanceFrame.pack(side=TOP, pady=20)
    title2 = Label(attendanceFrame, text="Online Attendance", fg="red", font=('arial', 25), bd=18)
    title2.grid(row=0, columnspan=2)

    cal = Calendar(attendanceFrame,selectmode="day", year=datetime.now(timezone('Asia/Kolkata')).year,
                   month=datetime.now(timezone('Asia/Kolkata')).month,
                   day=datetime.now(timezone('Asia/Kolkata')).day)
    cal.grid(row=1, columnspan=2, pady=10)

    lbl_studentname = Label(attendanceFrame, text="Student Name :", font=('Arial', 20), fg="#333333")
    lbl_studentname.grid(row=2, sticky="e", padx=10,pady=5)
    lbl_rollno = Label(attendanceFrame, text="Enrollment Number :", font=('Arial', 20), fg="#333333")
    lbl_rollno.grid(row=3, sticky="e", padx=10,pady=5)

    label_3 = Label(attendanceFrame, text="Status", width=20, font=('arial', 20))
    label_3.grid(row=5, column=0)

    lbl_result3 = Label(attendanceFrame, text="", font=('arial', 18))
    lbl_result3.grid(row=6, columnspan=2)
    studentname = Entry(attendanceFrame, font=('arial', 20), textvariable=STUDENTNAME, width=15)
    studentname.grid(row=2, column=1)
    rollno = Entry(attendanceFrame, font=('arial', 20), textvariable=REGNO, width=15)
    rollno.grid(row=3, column=1)

    present = Radiobutton(attendanceFrame, text="Present", padx=5, variable=var, value=1)
    present.grid(row=5, column=1)
    absent = Radiobutton(attendanceFrame, text="Absent", padx=20, variable=var, value=0)
    absent.grid(row=5, column=2)
    absent.grid(row=5, column=2)

    btn_submit = Button(attendanceFrame, text="SUBMIT", font=('Arial', 16, 'bold'), width=15,bg='#007bff', fg='white', bd=3, command=Submit)
    btn_submit.grid(row=7, columnspan=2, pady=20)
    btn_submit.config(command=Submit)

    btn_view_data = Button(attendanceFrame, text="View Data", font=('arial', 16,'bold'), width=15,bg='#007bff', fg='white', bd=3, command=view_data_window)
    btn_view_data.grid(row=8, columnspan=2, pady=20)

    exit_btn = Button(root, text="Exit", font=('Arial', 16, 'bold'), width=15,bg='#007bff', fg='white', bd=3, command=Exit)
    exit_btn.place(x=10, y=10)

def view_data_window():
    global view_data_win, tree_view_data
    view_data_win = Toplevel(root)
    view_data_win.title("View Data")
    view_data_win.geometry("800x500")

    btn_back = Button(view_data_win, text="Back", font=('arial', 18),bg='#007bff', fg='white', bd=3, command=view_data_win.destroy)
    btn_back.pack(pady=10)

    tree_view_data = ttk.Treeview(view_data_win, column=("column1", "column2", "column3", "column4"),
                                  show='headings')
    tree_view_data.heading("#1", text="Student Name")
    tree_view_data.heading("#2", text="Enrollment Number")
    tree_view_data.heading("#3", text="Status")
    tree_view_data.heading("#4", text="Date")

    # Fetch and insert attendance data into the treeview
    conn = sqlite3.connect("db_member3.db")
    cur = conn.cursor()
    cur.execute("SELECT Studentname, rollno, var, date FROM students")
    rows = cur.fetchall()
    for row in rows:
        status = "Present" if row[2] == "1" else "Absent"  # Check the value stored in the database
        tree_view_data.insert("", tk.END, values=(row[0], row[1], status, row[3]))

    tree_view_data.pack()

    # Close the database connection
    conn.close()


def ToggleToLogin(event=None):
    RegisterFrame.destroy()
    LoginForm()


def ToggleToRegister(event=None):
    LoginFrame.destroy()
    RegisterForm()


def ToggleToSubmit(event=None):
    LoginFrame.destroy()
    attendanceForm()


def Register():
    Database()
    if USERNAME.get() == "" or PASSWORD.get() == "" or LASTNAME.get() == "":
        lbl_result2.config(text="Please Complete The Required Field", fg="orange")
    else:
        cursor.execute("SELECT * FROM 'MEMBER' WHERE username=?", (USERNAME.get(),))
        if cursor.fetchone() is not None:
            lbl_result2.config(text="Username is already taken", fg="red")
        else:
            cursor.execute("INSERT INTO 'MEMBER' (username,password,firstname,lastname)VALUES(?,?,?,?)",
                           (str(USERNAME.get()), str(PASSWORD.get()), str(FIRSTNAME.get()), str(LASTNAME.get())))
            conn.commit()
            USERNAME.set("")
            PASSWORD.set("")
            FIRSTNAME.set("")
            LASTNAME.set("")
            lbl_result2.config(text="Successfully Created !", fg="#333333", font=('arial', 30,'bold'))


def Login():
    Database()
    if USERNAME.get() == "" or PASSWORD.get() == "":
        lbl_result1.config(text="Please Complete the Required Field !", fg="orange")
    else:
        cursor.execute("SELECT * FROM 'MEMBER' WHERE username=? AND password=?", (USERNAME.get(), PASSWORD.get()))
        if cursor.fetchone() is not None:
            lbl_result1.config(text="Login successful!", fg="green")
            ToggleToSubmit()  # Switch to the attendance form upon successful login
        else:
            lbl_result1.config(text="Invalid username or password", fg="red")


def Submit():
    """Function to submit attendance."""
    Database()
    if STUDENTNAME.get() == "" or REGNO.get() == "" or var.get() == "":
        lbl_result3.config(text="Please Complete the required field !", fg="orange")
    else:
        selected_date = cal.get_date()
        if not selected_date:
            selected_date = datetime.now(timezone('Asia/Kolkata')).strftime("%Y-%m-%d")
        response = tkMessageBox.showinfo("Submitted", "Attendance Submitted Successfully!")
        if response == 'ok':
            cursor.execute("INSERT INTO 'students' (Studentname, rollno, var, date) VALUES (?, ?, ?, ?)",
                           (STUDENTNAME.get(), REGNO.get(), var.get(), selected_date))
            conn.commit()
            STUDENTNAME.set("")
            REGNO.set("")
            var.set("")
            # Append submitted data to attendance_data list
            attendance_data.append((STUDENTNAME.get(), REGNO.get(), "Present" if var.get() == 1 else "Absent", selected_date))


if __name__ == '__main__':
    Database()
    LoginForm()
    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Exit", command=Exit)
    menubar.add_cascade(label="File", menu=filemenu)
    root.config(menu=menubar)
    root.mainloop()
#EndOf Code