import time

from zk import ZK, const
import tkinter as tk
import mysql.connector
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from pprint import pprint
# from mysql.connector import (connection)
# import mysql.connector
from datetime import date

db_con = ''

window = tk.Tk()
window.geometry("500x500")
window.title('Biometrics Configurations')

my_notebook = ttk.Notebook(window)
my_notebook.pack(pady=15)


def hide():
    my_notebook.hide(1)


bioconf_frame = Frame(my_notebook, width=500, height=500)
sqlconf_frame = Frame(my_notebook, width=500, height=500)

bioconf_frame.pack(fill="both", expand=1)
sqlconf_frame.pack(fill="both", expand=1)

my_notebook.add(bioconf_frame, text="Biometrics Configuration")
my_notebook.add(sqlconf_frame, text="Database Configuration")

# Fields for Database / Mysql
tk.Label(sqlconf_frame, text="Host: ").place(x=40, y=60)
tk.Label(sqlconf_frame, text="Database: ").place(x=40, y=100)
tk.Label(sqlconf_frame, text="Username: ").place(x=40, y=140)
tk.Label(sqlconf_frame, text="Password: ").place(x=40, y=180)

db_host = tk.StringVar()
dbname = tk.StringVar()
db_username = tk.StringVar()
db_pass = tk.StringVar()

db_host = tk.Entry(sqlconf_frame, width=30)
db_host.place(x=130, y=55)
dbname = tk.Entry(sqlconf_frame, width=30)
dbname.place(x=130, y=95)
db_username = tk.Entry(sqlconf_frame, width=30)
db_username.place(x=130, y=135)
db_pass = tk.Entry(sqlconf_frame, width=30)
db_pass.config(show="*")
db_pass.place(x=130, y=175)

saveConfigBTN = tk.Button(sqlconf_frame, text="  SAVE CONFIGURATION", justify='center',
                          command=lambda: __database_configuration__(dbname, db_username, db_pass, db_host))
saveConfigBTN.place(x=40, y=215)
saveConfigBTN.config(width=41, height=2)

# Fields for Biometrics Configuration
options = [
    "True",
    "False"
]

clicked = tk.StringVar(window)

clicked.set("False")
label = tk.Label(window, text="Configure Connection")

# label for IP ADDRESS
tk.Label(bioconf_frame, text="Ip Address: ").place(x=40, y=60)
tk.Label(bioconf_frame, text="Port: ").place(x=40, y=100)
tk.Label(bioconf_frame, text="Timeout: ").place(x=40, y=140)

ipfield = tk.StringVar()
port_field = tk.StringVar()
timeout_field = tk.StringVar()

ipfield = tk.Entry(bioconf_frame, width=30)
ipfield.place(x=130, y=55)
port_field = tk.Entry(bioconf_frame, width=30) or 0
port_field.place(x=130, y=95)
timeout_field = tk.Entry(bioconf_frame, width=30) or 0
timeout_field.place(x=130, y=135)

label.pack()

saveConfigBTN = tk.Button(bioconf_frame, text="  SAVE CONFIGURATION", justify='center',
                          command=lambda: check_validation(ipfield, port_field, timeout_field, db_host, dbname,
                                                           db_username, db_pass))
saveConfigBTN.place(x=40, y=195)
saveConfigBTN.config(width=41, height=2)


def __database_configuration__(db_name, db_user, db_password, db_hosts):
    db_hosts = db_hosts.get()
    db_name = db_name.get()
    db_user = db_user.get()
    db_password = db_password.get();

    if db_hosts == "":
        messagebox.showerror("Error", "Invalid database host")
    elif db_name == "":
        messagebox.showerror("Error", "Invalid database name")
    elif db_user == "":
        messagebox.showerror("Error", "Invalid database username")
    else:
        # db_con = mysql.connector.connect(
        #     host=str(db_hosts),
        #     user=db_user,
        #     password=db_password,
        #     database=db_name
        # )

        messagebox.showinfo("Success", "Configuration Success")


def __connection__(db_cons):
    msg = ""
    if db_cons:
        msg = messagebox.showinfo("Success", "Configuration Success")
    else:
        msg = messagebox.showerror("Error", "Configuration Error")
    return db_cons


def check_validation(ip, port, timeout, hosts, db_name, db_user, db_password):
    ip = str(ip.get())
    ports = port.get()
    timeouts = timeout.get()

    hosts = hosts.get()
    name = db_name.get()
    user = db_user.get()
    password = db_password.get();

    if ip == "":
        messagebox.showerror("Error", "Invalid Ip Address")
    elif ports == 0:
        messagebox.showerror("Error", "Invalid port")
    elif timeouts == 0:
        messagebox.showerror("Error", "Invalid timeouts")
    if hosts == "":
        messagebox.showerror("Error", "Insert database configuration")
    elif name == "":
        messagebox.showerror("Error", "Insert database configuration")
    elif user == "":
        messagebox.showerror("Error", "Insert database configuration")
    else:
        l = tk.Label(bioconf_frame, text="Connected..... ")
        l.place(x=180, y=270)
        bioconf_frame.update()
        __getattr__()


def __getattr__():
    ip_address = ipfield.get()
    ports = port_field.get()
    timeouts = timeout_field.get()

    hosts = db_host.get()
    name = dbname.get()
    user = db_username.get()
    password = db_pass.get();

    if ip_address == "":
        messagebox.showerror("Error", "Invalid Ip Address")
    elif ports == 0:
        messagebox.showerror("Error", "Invalid port")
    elif timeouts == 0:
        messagebox.showerror("Error", "Invalid timeouts")
    if hosts == "":
        messagebox.showerror("Error", "Insert database configuration")
    elif name == "":
        messagebox.showerror("Error", "Insert database configuration")
    elif user == "":
        messagebox.showerror("Error", "Insert database configuration")
    else:

        conn = None
        # create ZK instance
        zk = ZK(ip_address, port=int(ports), timeout=int(timeouts), password=0, force_udp=False, ommit_ping=False)

        # mysql connection
        myconnection = mysql.connector.connect(
            host=str(hosts),
            user=user,
            password=password,
            database=name
        )
        savedata = myconnection.cursor();

        # cnx = mysql.connector.connect(user='root', database='hwd_hris')
        # cursor = cnx.cursor()

        try:
            # connect to device
            conn = zk.connect()

            # disable device, this method ensures no activity on the device while the process is run
            conn.disable_device()

            attendances = conn.get_attendance()
            # pprint(attendances)
            for attendance in conn.live_capture():
                if attendance is None:
                    window.after(50)
                else:

                    attUid = attendance.user_id
                    attDate = attendance.timestamp

                    # print(attDate.year)
                    # print("")
                    # print("ID", attUid)
                    # print("name: ", attendance)
                    # print("year =", attDate.year)
                    # print("date =", attDate)
                    # print("month =", attDate.month)
                    # print("hour =", attDate.hour)
                    # print("minute =", attDate.minute)

                    sql_query_add = "INSERT INTO biometric_datas (biometric_id, date_time) VALUES (%s, %s)"

                    val = (attUid, attDate)
                    savedata.execute(sql_query_add, val)

                    myconnection.commit()
                    lab2 = tk.Label(bioconf_frame, text="User ID: ")
                    lab2.place(x=110, y=300)
                    lab2.update()

                    lab = tk.Label(bioconf_frame, text=attUid)
                    lab.place(x=200, y=300)
                    lab.update()

                    lab3 = tk.Label(bioconf_frame, text="Timestamp: ")
                    lab3.place(x=110, y=330)
                    lab3.update()

                    lab1 = tk.Label(bioconf_frame, text=attDate)
                    lab1.place(x=200, y=330)
                    lab1.update()

                    # messagebox.showinfo("Success", "Data Inserted")

                    # <Attendance>: 1 : 2021-05-20 15:47:59 (0, 0)
                    # add_dtr = ("INSERT INTO `biometric_records` (`id`, `user_id`, `date`, `time`, `shift`, `created_at`, `updated_at`) VALUES (NULL, %s, %s, %s, %s, NULL, NULL);")
                    # dtr_data = ()
                    # input('Press ENTER to exit')

            conn.test_voice()
            # re-enable device after all commands already executed
            conn.enable_device()
        except Exception as e:
            messagebox.showerror("Error", "Process terminate : {}".format(e))
            # print("Process terminate : {}".format(e))
        finally:
            if conn:
                conn.disconnect()
                messagebox.showinfo("Exit", "Exit")


window.mainloop()
