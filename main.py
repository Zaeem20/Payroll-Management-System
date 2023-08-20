import calendar
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from PIL import Image, ImageTk
# from PIL import ImageTk

class PayrollManager(object):
    def __init__(self, root: tk.Tk):
        self.root = root
        # windows config
        self.root.geometry('710x640')  # W x H
        self.root.maxsize(710, 640)
        self.root.minsize(710, 640)
        self.root.title("Maharashtra College Payroll Software")
        self.root.iconphoto(True, tk.PhotoImage(file='assets/icons/icon.png'))
        self.non_teaching = tk.IntVar()
        self.fixed_pay = tk.IntVar()
        self.teaching = tk.IntVar()
        self.deduction = tk.IntVar()
        self.emp_status = tk.IntVar()
        self.wd = tk.IntVar()
        self.ug_lectures_n = tk.IntVar()
        self.pg_lectures_n = tk.IntVar()
        self.ug = tk.BooleanVar()
        self.pg = tk.BooleanVar()
        self.visiting_pay = tk.IntVar()
        self.emp_name = tk.StringVar()

        # Banner
        self.banner_image = tk.PhotoImage(file='assets/banner/main-banner.png')
        self.banner = tk.Label(root, image=self.banner_image, relief=tk.RIDGE, bd=8)
        self.banner.grid(row=0, column=0, padx=30, pady=20, columnspan=2)

        # Enteries
        self.radio_frame = tk.Frame(root, padx=30)
        self.radio_frame.grid(row=1, sticky='e')
        
        tk.Radiobutton(self.radio_frame, text='Teaching', variable=self.emp_status, value=1, command=self.__pack_teaching).pack(side='left', padx=20)
        tk.Radiobutton(self.radio_frame, text='Non Teaching', variable=self.emp_status, value=2, command=self.__unpack_teaching).pack(side='right', padx=15)

        # Details Section
        details = tk.Frame(root, padx=5, pady=10, relief=tk.RIDGE, bd=4)
        details.grid(row = 3, sticky='e', padx=30, pady=5)

        # Employee name  (label & entry)
        self.name_label = tk.Label(details, text="Employee name: ", font=('Helvetica', 10))
        self.name_label.grid(row=1, column=0)
        self.name_entry = tk.Entry(details, textvariable=self.emp_name)
        self.name_entry.grid(row=1, column=1)

        # Fixed Pay (label & entry)
        self.fixedpay_label = tk.Label(details, text='Fixed Pay: ', font=('Helvetica', 10))
        self.fixedpay_label.grid(row=2, column=0)
        self.fixed_entry = tk.Entry(details, textvariable=self.fixed_pay)
        self.fixed_entry.grid(row=2, column=1)

        # Deduction (label & entry)
        self.ded_l = tk.Label(details, text='Deduction: ', font=('Helvetica', 10))
        self.ded_l.grid(row=3)
        self.ded_e = tk.Entry(details, textvariable=self.deduction)
        self.ded_e.grid(row=3, column=1)

        # Enteries
        # self.visiting_label = tk.Label(details, text="Visiting Pay (/lec):",font=('Helvetica', 10))
        # self.visiting_entry = tk.Entry(details, textvariable=self.visiting_pay)
        
        self.mode = tk.Label(details, text='Lectures in:', font=('Helvetica', 10))
        self.options_frame = tk.Frame(details, padx=10)

        self.ug_checkbox = tk.Checkbutton(self.options_frame, text='UG', variable=self.ug, command=self.__ug_input)
        self.pg_checkbox = tk.Checkbutton(self.options_frame, text='PG', variable=self.pg, command=self.__pg_input)


        self.ug_label = tk.Label(self.options_frame, text='No. of UG lectures')
        self.ug_entry = tk.Entry(self.options_frame, textvariable=self.ug_lectures_n, width=3)
        self.pg_label = tk.Label(self.options_frame, text='No. of PG lectures')
        self.pg_entry = tk.Entry(self.options_frame, textvariable=self.pg_lectures_n, width=3)


        # Working Days
        self.no_of_days = tk.Label(details, text='Working Days:', font=('Helvetica', 10))
        self.no_of_days.grid(row=4)
        self.days_entry = tk.Entry(details, textvariable=self.wd)
        self.days_entry.grid(row=4, column=1)

        self.submit_btn = tk.Button(root, text='submit', padx=7, bd=3, command=self.submit_response)
        self.submit_btn.grid(row=4, column=0, pady=10, padx=120, sticky='e')


    def submit_response(self):
        self.days_entry.get()

    def __ug_input(self):
        if self.ug.get():
            self.ug_label.grid(row=1)
            self.ug_entry.grid(row=1, column=1)
        else:
            self.ug_label.grid_forget()
            self.ug_entry.grid_forget()
    
    def __pg_input(self):
        if self.pg.get():
            self.pg_label.grid(row=2)
            self.pg_entry.grid(row=2, column=1)
        else:
            self.pg_label.grid_forget()
            self.pg_entry.grid_forget()

    def __pack_teaching(self):
        self.mode.grid(row=6)
        self.options_frame.grid(row=6, column=1)
        self.ug_checkbox.grid(row=0, sticky='w')
        self.pg_checkbox.grid(row=0, column=1, sticky='e')

    def __unpack_teaching(self):
        self.mode.grid_forget()
        self.options_frame.grid_forget()


if __name__ == '__main__':
    root = tk.Tk()
    app = PayrollManager(root)
    root.mainloop()