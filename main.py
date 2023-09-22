import tkinter as tk
from tkinter import ttk, messagebox
from calendar import monthrange
from core.utils import load_data
import numpy as np 
from core.exporters import to_excel
from core.logic import calculateSalary
from typing import Literal
# from PIL import ImageTk


class PayrollManager(object):
    def __init__(self, root: tk.Tk):
        self.root = root
        # windows config
        self.root.geometry('860x720')  # W x H
        self.root.maxsize(860, 720)
        self.root.minsize(860, 720)
        self.root.call('source', 'theme/forest-dark.tcl')
        self.root.call('source', 'theme/forest-light.tcl')
        self.style = ttk.Style(root)
        self.style.theme_use('forest-light')
        self.root.title("Maharashtra College Payroll Software")
        self.root.iconphoto(True, tk.PhotoImage(file='assets/icons/icon.png'))
        self.emp_status = tk.IntVar()
        self.no_of_lectures = tk.IntVar()
        self.notebook = ttk.Notebook(self.root)

        self.add_tab = ttk.Frame(self.notebook)
        self.view_tab = ttk.Frame(self.notebook)
        self.view_report = ttk.Frame(self.notebook)

        self.notebook.add(self.add_tab, text="Add Employee")
        self.notebook.add(self.view_tab, text="View Employees")
        self.notebook.add(self.view_report, text='View Report')
        self.notebook.pack(expand=True, fill='both')
        # Banner
        self.banner_image = tk.PhotoImage(file='assets/banner/main-banner.png')
        self.banner = tk.Label(self.add_tab, image=self.banner_image, relief=tk.RIDGE, bd=8)
        self.banner.grid(row=1, column=0, padx=(100,100), pady=20, columnspan=2)
        # self.banner.pack()

        self.detail = ttk.LabelFrame(self.add_tab, text='EMPLOYEE DETAILS')
        self.detail.grid(row = 3, sticky='e', ipadx=30, ipady=5)

        self.left_side = ttk.Frame(self.detail)
        self.left_side.grid(row=0, column=0, padx=(6,1))
        
        self.detail.rowconfigure(0, weight=0)
        self.detail.columnconfigure(0, weight=0)

        self.right_side = ttk.Frame(self.detail)
        self.right_side.grid(row=0, column=1)

        self.detail.rowconfigure(0, weight=1)
        self.detail.columnconfigure(1, weight=1)

        # self.detail.columnconfigure(1,weight=1)
        # Enteries

        # Details Section

        # Employee name  (label & entry)
        self.name_entry = ttk.Entry(self.left_side)
        self.name_entry.insert(0, 'Name')
        self.name_entry.bind('<FocusIn>', lambda x: self._on_entry_focus_in(self.name_entry, 'Name'))
        self.name_entry.bind('<FocusOut>', lambda x: self._on_entry_focus_out(self.name_entry, 'Name'))
        self.name_entry.grid(row=0, column=0, pady=(2,3))

        # Fixed Pay (label & entry)
        self.fixed_entry = ttk.Entry(self.left_side)
        self.fixed_entry.insert(0, 'Fixed Pay')
        self.fixed_entry.bind('<FocusIn>', lambda x: self._on_entry_focus_in(self.fixed_entry, 'Fixed Pay'))
        self.fixed_entry.bind('<FocusOut>', lambda x: self._on_entry_focus_out(self.fixed_entry, 'Fixed Pay'))
        self.fixed_entry.grid(row=1, column=0, pady=(2,3))

        # Deduction (label & entry)
        self.it_entry = ttk.Entry(self.left_side)
        self.it_entry.insert(0, 'Income Tax')
        self.it_entry.bind('<FocusIn>', lambda x: self._on_entry_focus_in(self.it_entry, 'Income Tax'))
        self.it_entry.bind('<FocusOut>', lambda x: self._on_entry_focus_out(self.it_entry, 'Income Tax'))
        self.it_entry.grid(row=2, pady=(2,3))

        
        self.pf_entry = ttk.Entry(self.left_side)
        self.pf_entry.insert(0, 'Prominent Fund')
        self.pf_entry.bind('<FocusIn>', lambda x: self._on_entry_focus_in(self.pf_entry, 'Prominent Fund'))
        self.pf_entry.bind('<FocusOut>', lambda x: self._on_entry_focus_out(self.pf_entry, 'Prominent Fund'))
        self.pf_entry.grid(row=3, pady=(2,3))

        self.other_tax_entry=ttk.Entry(self.left_side)
        self.other_tax_entry.insert(0,'Other taxes')
        self.other_tax_entry.bind('<FocusIn>', lambda x: self._on_entry_focus_in(self.other_tax_entry, 'Other taxes'))
        self.other_tax_entry.bind('<FocusOut>', lambda x: self._on_entry_focus_out(self.other_tax_entry, 'Other taxes'))
        self.other_tax_entry.grid(row=4, pady=(2,3))

        # Employee type
        self.radio_frame = ttk.LabelFrame(self.right_side, text='Employee Type')
        self.radio_frame.grid(row=0, column=0, sticky='nsew', padx=5)
        
        ttk.Radiobutton(self.radio_frame, text='Teaching', variable=self.emp_status, value=1, command=self.__pack_teaching).pack(side='left', anchor='w', padx=(2,1))
        ttk.Radiobutton(self.radio_frame, text='Non Teaching', variable=self.emp_status, value=2, command=self.__unpack_teaching).pack(side='right', anchor='w', padx=(1,2))

        self.employee_account = ttk.Entry(self.right_side, width=28)
        self.employee_account.insert(0, 'Account Number')
        self.employee_account.bind('<FocusIn>', lambda e: self._on_entry_focus_in(self.employee_account, 'Account Number'))
        self.employee_account.bind('<FocusOut>', lambda e: self._on_entry_focus_out(self.employee_account, 'Account Number'))
        self.employee_account.grid(row=1, column=0, pady=(5,3), padx=4)

        self.ifsc_code = ttk.Entry(self.right_side, width=20)
        self.ifsc_code.insert(0, 'Bank\'s IFSC Code')
        self.ifsc_code.bind('<FocusIn>', lambda x: self._on_entry_focus_in(self.ifsc_code, 'Bank\'s IFSC Code'))
        self.ifsc_code.bind('<FocusOut>', lambda x: self._on_entry_focus_out(self.ifsc_code, 'Bank\'s IFSC Code'))
        self.ifsc_code.grid(row=2, column=0, pady=(5,3), padx=4, sticky="nsew")

        # Enteries
        
        sep = ttk.Separator(self.right_side, orient='horizontal')
        sep.grid(row=3, column=0, padx=5, pady=10, sticky='ew')

        self.theme_mode = ttk.Checkbutton(self.right_side, text='Dark Theme', style='Switch', command=self.theme_callback)
        self.theme_mode.grid(row=4, column=0, padx=(4,4))

        # self.options_frame = tk.LabelFrame(self.right_side, padx=5, text='Lectures in')

        # self.ug_checkbox = tk.Checkbutton(self.options_frame, text='UG', variable=self.ug, command=self.__ug_input)
        # self.pg_checkbox = tk.Checkbutton(self.options_frame, text='PG', variable=self.pg, command=self.__pg_input)

        # self.ug_label = tk.Label(self.options_frame, text='No. of UG lectures')
        # self.ug_entry = tk.Spinbox(self.options_frame, from_=1, to=30, width=3)
        # self.pg_label = tk.Label(self.options_frame, text='No. of PG lectures')
        # self.pg_entry = tk.Entry(self.options_frame, textvariable=self.pg_lectures_n, width=3)

        self.submit_btn = ttk.Button(self.add_tab, text='Add Employee', command=self.add_employee)
        self.submit_btn.grid(row=4, column=0, pady=10, padx=(80,165), sticky='e')
        self.view_employee()
        self.manage_employee()
        self.generate_report()

    def add_employee(self):
        name = self.wd.get()
        fixed_pay = self.fixed_pay.get()
        deduction = self.deduction.get()
        dept = (1 if self.teaching.get() else 0)
        print(name, fixed_pay, deduction, dept)

    def view_employee(self):
        columns = ('ID', 'Name', 'Type', 'Salary', 'pf', 'it', 'other', 'AccountNo', "ifsc")
        treeFrame = ttk.Frame(self.view_tab)
        treeFrame.pack()
        scroll = ttk.Scrollbar(treeFrame)
        scroll.pack(side='right', fill='y')
        self.table = ttk.Treeview(treeFrame, yscrollcommand=scroll.set, show='headings', column=columns, height=10)

        # table.column("#0", width=0, stretch=tk.NO)  # Hide the first column
        self.table.column('ID', width=25, minwidth=25, anchor='w')
        self.table.column("Name", width=125, minwidth=125, anchor='w')
        self.table.column("Type", width=120, minwidth=120, anchor='w')
        self.table.column("Salary", width=80, minwidth=80, anchor='w')
        self.table.column("AccountNo", width=120, minwidth=120, anchor='w')
        self.table.column('pf', width=60, minwidth=60, anchor='w')
        self.table.column('it', width=60, minwidth=60, anchor='w')
        self.table.column('other', width=65, minwidth=65, anchor='w')
        self.table.column('ifsc', width=100, minwidth=100, anchor='w')

        self.table.heading('ID', text='ID', anchor='w')
        self.table.heading('Name', text='Employee Name', anchor='w')
        self.table.heading('Type', text='Department Type', anchor='w')
        self.table.heading('Salary', text='Salary', anchor='w')
        self.table.heading('pf',text='PF', anchor='w')
        self.table.heading('it', text='IT', anchor='w')
        self.table.heading('other', text='Other Tax', anchor='w')
        self.table.heading('AccountNo', text='Account Number', anchor='w')
        self.table.heading('ifsc', text='IFSC Code', anchor='w')

        scroll.config(command=self.table.yview)
        
        for x in load_data('both'):
            self.table.insert('', tk.END, values=tuple(x))
        self.table.bind('<Double-1>', lambda e: self._get_selection(self.table))

        self.table.pack()

        

    def manage_employee(self):
        bottomFrame = ttk.Frame(self.view_tab)
        bottomright = ttk.Frame(bottomFrame)
        bottomleft = ttk.Frame(bottomFrame)
        self.ActionFrame = ttk.LabelFrame(bottomright, text='Make Report')
        self.sideFrame = ttk.LabelFrame(bottomleft, text='UG/PG lectures')
        ActionControl = ttk.Frame(bottomright)
        # bottomright.grid(row=0)
        bottomright.grid(row=0, sticky='nw', pady=20)
        bottomleft.grid(row=0, column=1)
        
        self.id_var = tk.StringVar()
        self.name_var = tk.StringVar()
        self.dept_type = tk.StringVar()
        self.sal_var = tk.IntVar(value='')
        self.pf_var = tk.IntVar(value='')
        self.it_var = tk.IntVar(value='')
        self.oth_var = tk.IntVar(value='')
        self.acc_var = tk.IntVar(value='')
        self.ifsc_var = tk.StringVar()

        self.total_lectures = tk.IntVar(value='')

        emp_id = ttk.Entry(self.ActionFrame, textvariable=self.id_var)
        emp_id.insert(0, 'Employee ID')
        emp_id.bind('<FocusIn>', lambda e: self._on_entry_focus_in(emp_id, 'Employee ID'))
        emp_id.bind('<FocusOut>', lambda e: self._on_entry_focus_out(emp_id, 'Employee ID'))

        name = ttk.Entry(self.ActionFrame, textvariable=self.name_var)
        name.insert(0, 'Employee Name')
        name.bind('<FocusIn>', lambda e: self._on_entry_focus_in(name, 'Employee Name'))
        name.bind('<FocusOut>', lambda e: self._on_entry_focus_out(name, 'Employee Name'))

        dept = ttk.Combobox(self.ActionFrame, values=['Teaching', 'Non-Teaching'], textvariable=self.dept_type)
        dept.current(0)
        self.dept_type.trace_add("write", lambda x,y,z: self.is_teaching(self.dept_type.get(), action=True))
        self.salary = ttk.Entry(self.ActionFrame, textvariable=self.sal_var)
        self.salary.insert(0, 'Salary')
        self.salary.bind('<FocusIn>', lambda e: self._on_entry_focus_in(self.salary, 'Salary'))
        self.salary.bind('<FocusOut>', lambda e: self._on_entry_focus_out(self.salary, 'Salary'))

        income_tax = ttk.Entry(self.ActionFrame, textvariable=self.it_var)
        income_tax.insert(0, 'Income Tax')
        income_tax.bind('<FocusIn>', lambda e: self._on_entry_focus_in(income_tax, 'Income Tax'))
        income_tax.bind('<FocusOut>', lambda e: self._on_entry_focus_out(income_tax, 'Income Tax'))

        pf = ttk.Entry(self.ActionFrame, textvariable=self.pf_var)
        pf.insert(0, 'Prominent Fund')
        pf.bind('<FocusIn>', lambda e: self._on_entry_focus_in(pf, 'Prominent Fund'))
        pf.bind('<FocusOut>', lambda e: self._on_entry_focus_out(pf, 'Prominent Fund'))

        oth = ttk.Entry(self.ActionFrame, textvariable=self.oth_var)
        oth.insert(0, 'Other Tax')
        oth.bind('<FocusIn>', lambda e: self._on_entry_focus_in(oth, 'Other Tax'))
        oth.bind('<FocusOut>', lambda e: self._on_entry_focus_out(oth,"Other Tax"))

        acc = ttk.Entry(self.ActionFrame, textvariable=self.acc_var)
        acc.insert(0, 'Account Number')
        acc.bind('<FocusIn>', lambda e: self._on_entry_focus_in(acc, 'Account Number'))
        acc.bind('<FocusOut>', lambda e: self._on_entry_focus_out(acc,"Account Number"))

        ifsc = ttk.Entry(self.ActionFrame, textvariable=self.ifsc_var)
        ifsc.insert(0, 'IFSC Code')
        ifsc.bind('<FocusIn>', lambda e: self._on_entry_focus_in(oth, 'IFSC Code'))
        ifsc.bind('<FocusOut>', lambda e: self._on_entry_focus_out(oth,"IFSC Code"))

        add_btn = ttk.Button(ActionControl, text='Add To Report', command=self.add_in_report)
        view_t_btn = ttk.Button(ActionControl, text='View Teaching', command=lambda _: self.view_teaching(self.table))
        view_nt_btn = ttk.Button(ActionControl, text='View Non-Teaching', command=lambda _: self.view_non_teching(self.table))


        emp_id.grid(row=0, column=0, sticky='w', padx=(15,15), pady=(15,15))
        name.grid(row=0, column=1, padx=(15,15), pady=(15,15))
        dept.grid(row=0, column=2, padx=(15,15), pady=(15,15))

        self.salary.grid(row=1, column=0, sticky='w', padx=(15,15), pady=(15,15))
        income_tax.grid(row=1, column=1, padx=(15,15), pady=(15,15))
        pf.grid(row=1, column=2, padx=(15,15), pady=(15,15))
        
        oth.grid(row=2, column=0, padx=(15,15), pady=(15,15))
        acc.grid(row=2, column=1, padx=(15,15), pady=(15,15))
        ifsc.grid(row=2, column=2, padx=(15,15), pady=(15,15))
        
    # Action Control Menu
        view_nt_btn.grid(row=0, column=0, padx=(10,10))
        add_btn.grid(row=0, column=1, padx=(10,10))
        view_t_btn.grid(row=0, column=2, padx=(10,10))

    # Side Frame
        class_ = ttk.Combobox(self.sideFrame, values=['Under Graduate', 'Post Graduate'], state='readonly')
        class_.current(0)
        class_.bind('<<ComboboxSelected>>', lambda e: self.check_class(class_))

        side_bottom = ttk.Frame(self.sideFrame)
        side_bottom.grid(row=2)

        no_of_lecture = ttk.Spinbox(side_bottom, width=2, from_=0, to=30, textvariable=self.no_of_lectures)
        self.year = ttk.Combobox(side_bottom, width=4, values=['F.Y', 'S.Y', 'T.Y'], state='readonly')
        self.year.current(0)
        self.course = ttk.Combobox(side_bottom, width=8, values=['B.Sc CS', 'B.Sc IT', 'B.M.S', 'B.A.F', 'B.Com', 'B.Sc', 'B.A'], state='readonly')
        self.course.current(0)
        add_lec_record = ttk.Button(side_bottom, text='Add record', command=lambda : self.add_class_record(self.lecture_info_tree))
    
        #         ...       
        class_.grid(row=0, padx=(3,3), pady=(2,0), sticky='nsew' )
        line_sep = ttk.Separator(self.sideFrame, orient='horizontal')
        line_sep.grid(row=1, sticky='nsew', pady=10, padx=(4,4))

        no_of_lecture.grid(row=0, column=0, padx=2)
        self.year.grid(row=0, column=1, padx=2)
        self.course.grid(row=0, column=2, padx=2)
        add_lec_record.grid(row=1, pady=(5,5), padx=(2,2), columnspan=3,sticky='nsew')

        self.lecture_info_tree = ttk.Treeview(self.sideFrame, show='headings', columns=('year', 'course', 'nol'), height=5)
        
        self.lecture_info_tree.column('year', width=12, minwidth=12)
        self.lecture_info_tree.column('course', width=15, minwidth=15)
        self.lecture_info_tree.column('nol', width=25, minwidth=25, anchor='center')

        self.lecture_info_tree.heading('year', text='Year', anchor='w')
        self.lecture_info_tree.heading('course', text='Course', anchor='w')
        self.lecture_info_tree.heading('nol', text='No.of Lecture', anchor='w')

        self.lecture_info_tree.grid(row=3, sticky='nsew', padx=(3,3))
        self.ActionFrame.grid(row=1, column=0, sticky='nw')
        ActionControl.grid(padx=(15,15),pady=10)
        self.sideFrame.grid(row=1, column=1, padx=(8,8), pady=(20,20))

        bottomFrame.pack()

    def check_class(self, class_):
        value = class_.get().lower().replace(' ', '')

        if value == 'postgraduate':
            self.year.config(values=['I', 'II'])
            self.year.current(0)
            self.course.config(values=['M.Sc IT', 'M.Com', 'M.A', 'M.Sc'])
            self.course.current(0)
        else:
            self.year.config(values=['F.Y', 'S.Y', 'T.Y'])
            self.year.current(0)
            self.course.config(values=['B.Sc CS', 'B.Sc IT', 'B.M.S', 'B.A.F', 'B.Com', 'B.Sc', 'B.A'])
            self.course.current(0)


    def is_teaching(self, dept: str, action: bool = True) -> bool:
        """
        Determines if the department type is "teaching" or not.

        Args:
            dept (str): The department type to check.
            action (bool, optional): Whether to perform the action or not. Defaults to True.

        Returns:
            bool: True if the department type is "teaching", False otherwise.
        """
        if dept.lower() != 'teaching':
            if action:
                self.sideFrame.grid_forget()
            return False
        else:
            if action:
                self.sideFrame.grid(row=1, column=1, padx=(8,8), pady=(20,20))
            return True

    def add_class_record(self, tree: ttk.Treeview):
        values = (self.year.get(), self.course.get(), self.no_of_lectures.get())
        records = list(map(lambda x: [x[0], (x[1][0], x[1][1], int(x[1][2]))], [(child, tree.item(child, 'values')) for child in tree.get_children()]))
        exists, where = any(x[1][:-1] == values[:-1] for x in records), list(map(lambda x: x[1][:-1] == values[:-1], records))

        if exists:
            result = messagebox.askyesno('Duplicate Found', 'it seems table already contains this record\nWould you like to update that.')
            if result:
                entry = records[where.index(True)][0]
                tree.item(entry, values=values)
                return
            return
        tree.insert('', tk.END, values=values)


    def add_in_report(self):
        name = self.name_var.get()
        salary = self.sal_var.get()
        it, pf, other = self.it_var.get(), self.pf_var.get(), self.oth_var.get()
        deduction = it+pf+other
        type = self.dept_type.get()
        if self.is_teaching(type, action=False):
            total_ug_lectures = 0
            total_pg_lectures = 0
            for i in self.lecture_info_tree.get_children():
                row = self.lecture_info_tree.item(i, 'values')
                if self._check_is_ug(row):
                    total_ug_lectures += int(row[-1])
                else:
                    total_pg_lectures += int(row[-1])
            net_amount = calculateSalary(salary, deduction, total_ug_lectures, total_pg_lectures)
        else:
            net_amount = calculateSalary(salary, deduction, is_teaching=False)
        acc = self.acc_var.get()
        ifsc = self.ifsc_var.get()

        sr = 1
        records = self.report_table.get_children()
        if not records:
            self.report_table.insert('', tk.END, values=(sr, name, type, salary, deduction, net_amount, acc, ifsc))
        else:
            sr += len(records)
            self.report_table.insert('', tk.END, values=(sr, name, type, salary, deduction, net_amount, acc, ifsc))


        self.id_var.set('Employee ID')
        self.name_var.set('Employee Name')
        self.dept_type.set('Teaching')
        self.sal_var.set('Salary')
        self.it_var.set('Income Tax')
        self.pf_var.set('Prominent Fund')
        self.oth_var.set('Other Tax')
        self.acc_var.set('Account Number')
        self.ifsc_var.set('IFSC Code')

        self.no_of_lectures.set(0)
        for record in self.lecture_info_tree.get_children():
            self.lecture_info_tree.delete(record)

        return messagebox.showinfo('Record Added', 'Record added to report\nkindly navigate to View Report')


    def export_report(self, dept_type: Literal['teaching', 'nonteaching']):
        tree = self.report_table
        rows = [tree.item(row, 'values') for row in tree.get_children()]
        print(rows)
        type_filter = filter(lambda x: x[2].lower().replace('-', '') == dept_type, rows)

        updated_rows = [row[1:] for row in type_filter]
        print(updated_rows)

        to_excel(updated_rows, ('Employee Name', 'Department Type', 'Total Amount', 'Deduction', 'Net Amount', 'Account Number', 'IFSC Code'))



    def _check_is_ug(self, row: tuple):
        if row[1].startswith('M'):
            return False
        return True

    def view_teaching(self, tree: ttk.Treeview):
        for record in tree.get_children():
            tree.delete(record)

        for entires in load_data('teaching'):
            tree.insert('', tk.END, values=tuple(entires))

    def view_non_teching(self, tree: ttk.Treeview):
        for record in tree.get_children():
            tree.delete(record)

        for entires in load_data('nonteaching'):
            tree.insert('', tk.END, values=tuple(entires))

    def generate_report(self):
        treeFrame = ttk.Frame(self.view_report)
        treeFrame.pack()
        scroll = ttk.Scrollbar(treeFrame)
        scroll.pack(side='right', fill='y')
        columns = ['sr', 'name', 'type', 'amount', 'deduction', 'netamount', 'bankaccount', 'bankifsc']
        self.report_table = ttk.Treeview(treeFrame, yscrollcommand=scroll.set, show='headings', column=columns, height=10)

        # table.column("#0", width=0, stretch=tk.NO)  # Hide the first column
        self.report_table.column('sr', width=40, minwidth=40, anchor='w')
        self.report_table.column("name", width=125, minwidth=125, anchor='w')
        self.report_table.column("type", width=120, minwidth=120, anchor='w')
        self.report_table.column("amount", width=90, minwidth=90, anchor='w')
        self.report_table.column('deduction', width=80, minwidth=80, anchor='w')
        self.report_table.column("netamount", width=80, minwidth=80, anchor='w')
        self.report_table.column("bankaccount", width=120, minwidth=120, anchor='w')
        self.report_table.column('bankifsc', width=100, minwidth=100, anchor='w')

        self.report_table.heading('sr', text='Sr No.', anchor='w')
        self.report_table.heading('name', text='Employee Name', anchor='w')
        self.report_table.heading('type', text='Department Type', anchor='w')
        self.report_table.heading('amount', text='Total Amount', anchor='w')
        self.report_table.heading('deduction', text='Deduction', anchor='w')
        self.report_table.heading('netamount', text='Net Amount', anchor='w')
        self.report_table.heading('bankaccount', text='Account Number', anchor='w')
        self.report_table.heading('bankifsc', text='IFSC Code', anchor='w')

        scroll.config(command=self.report_table.yview)
        self.report_table.pack(padx=(3,3))

        exportMenu = ttk.LabelFrame(self.view_report, text='Export Menu')
        
        export_teaching = ttk.Button(exportMenu, text='Export Teaching', command=lambda : self.export_report(dept_type='teaching'))
        export_nonteaching = ttk.Button(exportMenu, text='Export Non-Teaching', command=lambda : self.export_report(dept_type='nonteaching'))
        export_teaching.grid(row=0, padx=(5,5), pady=(5,5))
        export_nonteaching.grid(row=0, column=1, padx=(5,5), pady=(5,5))
        
        exportMenu.pack(pady=(10,10))


    def theme_callback(self):
        if self.theme_mode.instate(['selected']):
            self.style.theme_use('forest-dark')
        else:
            self.style.theme_use('forest-light')

    def _on_entry_focus_in(self, widget, placeholder_text):
        if widget.get() == placeholder_text:
            widget.delete(0, tk.END)
            # if self.style.get_
            # widget.config(foreground="black")
            
    def _on_entry_focus_out(self, widget, placeholder_text):
        if not widget.get():
            widget.insert(0, placeholder_text)
            # widget.config(foreground="black") 
    
    def _get_selection(self, tree: ttk.Treeview):
        row_id = tree.selection()[0]
        row_values = self.table.item(row_id, 'values')
        id, name, type, sal, pf, it, oth, acc, ifsc = row_values
        self.id_var.set(id)
        self.name_var.set(name)
        self.dept_type.set(type)
        self.sal_var.set(sal)
        self.salary.config(state=tk.DISABLED)
        self.pf_var.set(pf)
        self.it_var.set(it)
        self.oth_var.set(oth)
        self.acc_var.set(acc)
        self.ifsc_var.set(ifsc)

    def __pack_teaching(self):
        # self.mode.grid(row=6)
        self.options_frame.grid(row=3, column=1)
        self.ug_checkbox.grid(row=0, sticky='w')
        self.pg_checkbox.grid(row=0, column=1, sticky='e')

    def __unpack_teaching(self):
        # self.mode.grid_forget()
        self.options_frame.grid_forget()


if __name__ == '__main__':
    root = tk.Tk()
    app = PayrollManager(root)
    root.mainloop()
    