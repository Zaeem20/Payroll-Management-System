import re 
import tkinter as tk
from tkinter import ttk, messagebox 
from core.exporters import to_excel
from core.logic import calculateSalary
from core.utils import Manager
from core.models.employee import EmployeeDetails
from typing import Literal, List, Union

class PayrollManager(object):
    def __init__(self, root: tk.Tk):
        # Setting up Database Manager
        self.database_manager = Manager('credentials/firestore_keys.json')
        # windows config
        self.root = root
        self.root.geometry('850x720')  # W x H
        self.root.minsize(850, 720)
        self.root.maxsize(850, 720)
        self.root.call('source', 'theme/forest-dark.tcl')
        self.root.call('source', 'theme/forest-light.tcl')
        self.style = ttk.Style(root)
        self.style.theme_use('forest-light')
        self.root.title("Maharashtra College Payroll Software")
        self.root.iconphoto(True, tk.PhotoImage(file='assets/icons/icon.png'))
        self.emp_status = tk.IntVar()
        self.no_of_lectures = tk.IntVar()

        # Setting up Panes
        self.notebook = ttk.Notebook(self.root)
        self.add_tab = ttk.Frame(self.notebook)
        self.manage_tab = ttk.Frame(self.notebook)
        self.generate_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.add_tab, text="Add Employee")
        self.notebook.add(self.manage_tab, text="Manage Employees")
        self.notebook.add(self.generate_tab, text='Generate Report')
        self.notebook.pack(expand=True, fill='both')

        # Banner
        self.banner_image = tk.PhotoImage(file='assets/banner/main-banner.png')
        self.banner = tk.Label(self.add_tab, image=self.banner_image, relief=tk.RIDGE, bd=8)
        self.banner.grid(row=1, column=0, padx=(100,100), pady=20, columnspan=2)

        # Setting Up Frame 
        self.detail = ttk.LabelFrame(self.add_tab, text='EMPLOYEE DETAILS')
        self.detail.grid(row = 3, sticky='e', ipadx=30, ipady=5)

        # Spliting them in 2 sides
        self.left_side = ttk.Frame(self.detail)
        self.left_side.grid(row=0, column=0, padx=(6,1))
        self.detail.rowconfigure(0, weight=0)
        self.detail.columnconfigure(0, weight=0)

        self.right_side = ttk.Frame(self.detail)
        self.right_side.grid(row=0, column=1)
        self.detail.rowconfigure(0, weight=1)
        self.detail.columnconfigure(1, weight=1)

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
        
        ttk.Radiobutton(self.radio_frame, text='Teaching', variable=self.emp_status, value=1).pack(side='left', anchor='w', padx=(2,1))
        ttk.Radiobutton(self.radio_frame, text='Non Teaching', variable=self.emp_status, value=2).pack(side='right', anchor='w', padx=(1,2))

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

        # Seperator
        sep = ttk.Separator(self.right_side, orient='horizontal')
        sep.grid(row=3, column=0, padx=5, pady=10, sticky='ew')

        # Theme toggle button
        self.theme_mode = ttk.Checkbutton(self.right_side, text='Dark Theme', style='Switch', command=self.theme_callback)
        self.theme_mode.grid(row=4, column=0, padx=(4,4))

        # Atlast our Submit button
        self.submit_btn = ttk.Button(self.add_tab, text='Add Employee', command=self.add_employee)
        self.submit_btn.grid(row=4, column=0, pady=10, padx=(80,165), sticky='e')
        
        # Calling other functions
        self.view_employee()
        self.manage_employee()
        self.generate_report()

    def add_employee(self):
        """
        Add a new employee to the payroll system.

        Retrieves the employee details from the input fields in the GUI,
        creates an `EmployeeDetails` object with the provided information,
        and adds it to the database using the `database_manager` object.
        Displays a success or error message based on the result of the database operation.
        """

        # Retrieve employee details from GUI input fields
        name = self.name_entry.get()
        fixed = int(self.fixed_entry.get())
        it = int(self.it_entry.get())
        pf = int(self.pf_entry.get())
        other = int(self.other_tax_entry.get())
        department_type = 'teaching' if self.emp_status.get() == 1 else 'non-teaching'
        bankacc = self.employee_account.get()
        ifsc = self.ifsc_code.get()

        # Generate unique ID for the employee
        id = self.database_manager.get_next_id(department_type)

        # Create EmployeeDetails object
        details = EmployeeDetails(
            id=id,
            name=name,
            dept_type=department_type,
            salary=fixed,
            income_tax=it,
            prominent_fund=pf,
            other_tax=other,
            account_number=bankacc,
            ifsc_code=ifsc
        )

        # Add employee details to the database
        msg = self.database_manager.add(details)

        # Display success or error message
        if msg:
            messagebox.showinfo('Employee Added', msg)
        else:
            messagebox.showerror('Employee Not Added', 'It seems that an employee with the same details exists. '
                                                        'Try to remove the old entry. If the issue still persists, '
                                                        'please connect with the Development Team.')

    def view_employee(self):
        """
        Display a table of employee details in the GUI.
        """
        columns = ('ID', 'Name', 'Type', 'Salary', 'it', 'pf', 'other', 'AccountNo', "ifsc")
    
        # Create a frame to hold the employee table
        treeFrame = ttk.Frame(self.manage_tab)
        treeFrame.pack()
    
        # Create a scrollbar for the table
        scroll = ttk.Scrollbar(treeFrame)
        scroll.pack(side='right', fill='y')
    
        # Create a ttk.Treeview widget with the specified columns and height
        self.table = ttk.Treeview(treeFrame, yscrollcommand=scroll.set, show='headings', column=columns, height=10)
    
        # Configure the columns of the table with their respective widths and headings
        column_widths = [25, 125, 120, 80, 60, 60, 65, 120, 100]
        column_headings = ['ID', 'Employee Name', 'Department Type', 'Salary', 'IT', 'PF', 'Other Tax', 'Account Number', 'IFSC Code']
    
        for i, column in enumerate(columns):
            self.table.column(column, width=column_widths[i], minwidth=column_widths[i], anchor='w')
            self.table.heading(column, text=column_headings[i], anchor='w')
    
        # Configure the scrollbar to control the vertical scrolling of the table
        scroll.config(command=self.table.yview)
    
        # Retrieve employee data from the load_data function and insert it into the table
        for employee in self.database_manager.getAll('teaching'):
            self.table.insert('', tk.END, values=tuple(employee.values()))
    
        # Bind a double-click event to the table to handle selection of an employee
        self.table.bind('<Double-1>', lambda e: self._get_selection(self.table))
    
        # Pack the table
        self.table.pack()

    def manage_employee(self):
        """
        Creates a user interface for managing employee details, including adding employees to a report
        and viewing employees based on their department type. It also allows the user to input information
        about the employee's lectures if they are a teaching employee.
        """

        # Creating all frames        
        bottomFrame = ttk.Frame(self.manage_tab)  # Main Bottom Frame
        bottomright = ttk.Frame(bottomFrame)   # Child Frame (Right)
        bottomleft = ttk.Frame(bottomFrame)    # Child Frame (Left)
        self.ActionFrame = ttk.LabelFrame(bottomright, text='Make Report')  # Label Frame (bottomright)
        ActionControl = ttk.Frame(bottomright)   # Frame contains Buttons for manipulation
        self.sideFrame = ttk.LabelFrame(bottomleft, text='UG/PG lectures')  # Label Frame (bottmleft)
        side_bottom = ttk.Frame(self.sideFrame)   # Child Frame for sideFrame for lecture selection

        self.id_var = tk.IntVar(value='')
        self.name_var = tk.StringVar()
        self.dept_type = tk.StringVar()
        self.sal_var = tk.IntVar(value='')
        self.pf_var = tk.IntVar(value='')
        self.it_var = tk.IntVar(value='')
        self.oth_var = tk.IntVar(value='')
        self.acc_var = tk.IntVar(value='')
        self.ifsc_var = tk.StringVar()

        self.total_lectures = tk.IntVar(value='')

        # Action Frame Widgets
        self.emp_id = ttk.Entry(self.ActionFrame, textvariable=self.id_var)
        self.emp_id.insert(0, 'Employee ID')
        self.emp_id.bind('<FocusIn>', lambda e: self._on_entry_focus_in(self.emp_id, 'Employee ID'))
        self.emp_id.bind('<FocusOut>', lambda e: self._on_entry_focus_out(self.emp_id, 'Employee ID'))

        name = ttk.Entry(self.ActionFrame, textvariable=self.name_var)
        name.insert(0, 'Employee Name')
        name.bind('<FocusIn>', lambda e: self._on_entry_focus_in(name, 'Employee Name'))
        name.bind('<FocusOut>', lambda e: self._on_entry_focus_out(name, 'Employee Name'))

        dept = ttk.Combobox(self.ActionFrame, values=['Teaching', 'Non-Teaching'], textvariable=self.dept_type)
        dept.current(0)
        self.dept_type.trace_add("write", lambda x, y, z: self.is_teaching(self.dept_type.get(), action=True))
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
        oth.bind('<FocusOut>', lambda e: self._on_entry_focus_out(oth, "Other Tax"))

        acc = ttk.Entry(self.ActionFrame, textvariable=self.acc_var)
        acc.insert(0, 'Account Number')
        acc.bind('<FocusIn>', lambda e: self._on_entry_focus_in(acc, 'Account Number'))
        acc.bind('<FocusOut>', lambda e: self._on_entry_focus_out(acc, "Account Number"))

        ifsc = ttk.Entry(self.ActionFrame, textvariable=self.ifsc_var)
        ifsc.insert(0, 'IFSC Code')
        ifsc.bind('<FocusIn>', lambda e: self._on_entry_focus_in(oth, 'IFSC Code'))
        ifsc.bind('<FocusOut>', lambda e: self._on_entry_focus_out(oth, "IFSC Code"))


        # Action Control Widgets
        self.add_btn = ttk.Button(ActionControl, text='Add To Report', command=self.add_in_report, state=tk.DISABLED)
        view_t_btn = ttk.Button(ActionControl, text='View Teaching', command=lambda: self.show_employees(self.table, 'teaching'))
        view_nt_btn = ttk.Button(ActionControl, text='View Non-Teaching', command=lambda: self.show_employees(self.table, 'non-teaching'))
        self.update_btn = ttk.Button(ActionControl, text='Update in DB', command=self.update_to_db, state=tk.DISABLED)
        refresh_btn = ttk.Button(ActionControl, text='Refresh Tree', command=lambda : self._refresh_tree(self.table, list(self.database_manager.getAll('teaching'))))
        self.delete_btn = ttk.Button(ActionControl, text='Delete from DB', command=self.delete_from_db, state=tk.DISABLED)

        # Action Frame Entries location
        # Row: 0, column: (0,1,2)
        self.emp_id.grid(row=0, column=0, sticky='w', padx=(15, 15), pady=(15, 15)) 
        name.grid(row=0, column=1, padx=(15, 15), pady=(15, 15))
        dept.grid(row=0, column=2, padx=(15, 15), pady=(15, 15))

        # Row: 1, column: (0,1,2)
        self.salary.grid(row=1, column=0, sticky='w', padx=(15, 15), pady=(15, 15))
        income_tax.grid(row=1, column=1, padx=(15, 15), pady=(15, 15))
        pf.grid(row=1, column=2, padx=(15, 15), pady=(15, 15))

        # Row: 2, column: (0,1,2)
        oth.grid(row=2, column=0, padx=(15, 15), pady=(15, 15))
        acc.grid(row=2, column=1, padx=(15, 15), pady=(15, 15))
        ifsc.grid(row=2, column=2, padx=(15, 15), pady=(15, 15))

        # Action Control Menu
        view_nt_btn.grid(row=0, column=0, padx=(10, 10), sticky='nsew')
        self.add_btn.grid(row=0, column=1, padx=(10, 10), sticky='nsew')
        view_t_btn.grid(row=0, column=2, padx=(10, 10), sticky='nsew')
        self.update_btn.grid(row=1, column=0, padx=(10, 10), pady=(4, 4), sticky='nsew')
        refresh_btn.grid(row=1, column=1, padx=(10, 10), pady=(4, 4), sticky='nsew')
        self.delete_btn.grid(row=1, column=2, padx=(10, 10), pady=(4, 4), sticky='nsew')

        # Side Frame (Widgets)
        # combobox for selection of ug or pg
        class_ = ttk.Combobox(self.sideFrame, values=['Under Graduate', 'Post Graduate'], state='readonly')
        class_.current(0)
        class_.bind('<<ComboboxSelected>>', lambda e: self.check_class(class_))

        # widgets for selecting lectures and adding records (member of sidebottom)
        no_of_lecture = ttk.Spinbox(side_bottom, width=2, from_=0, to=30, textvariable=self.no_of_lectures)
        self.year = ttk.Combobox(side_bottom, width=4, values=['F.Y', 'S.Y', 'T.Y'], state='readonly')
        self.year.current(0)
        self.course = ttk.Combobox(side_bottom, width=8, values=['B.Sc CS', 'B.Sc IT', 'B.M.S', 'B.A.F', 'B.Com', 'B.Sc', 'B.A'], state='readonly')
        self.course.current(0)
        add_lec_record = ttk.Button(side_bottom, text='Add record', command=lambda: self.add_class_record(self.lecture_info_tree))
        line_sep = ttk.Separator(self.sideFrame, orient='horizontal')

        # Complete widgets locations of sideframe, sidebottom
        class_.grid(row=0, padx=(3, 3), pady=(2, 0), sticky='nsew') # for ug/pg
        line_sep.grid(row=1, sticky='nsew', pady=10, padx=(4, 4))   # line seperator
        no_of_lecture.grid(row=0, column=0, padx=2, columnspan=1)   # number of lectures
        self.year.grid(row=0, column=1, padx=2, columnspan=1)       # dropdown menu for selecting year
        self.course.grid(row=0, column=2, padx=2, columnspan=1)     # dropdown menu for selecting course
        add_lec_record.grid(row=1, pady=(5, 5), padx=(2, 2), columnspan=3, sticky='nsew')  # button for adding lecture in tree

        # Creating child tree for selected_lecture_info
        self.lecture_info_tree = ttk.Treeview(self.sideFrame, show='headings', columns=('year', 'course', 'nol'), height=5)
        # configuring columns
        self.lecture_info_tree.column('year', width=12, minwidth=12)
        self.lecture_info_tree.column('course', width=15, minwidth=15)
        self.lecture_info_tree.column('nol', width=25, minwidth=25, anchor='center')
        # adding heading text
        self.lecture_info_tree.heading('year', text='Year', anchor='w')
        self.lecture_info_tree.heading('course', text='Course', anchor='w')
        self.lecture_info_tree.heading('nol', text='No.of Lecture', anchor='w')
        self.lecture_info_tree.grid(row=3, sticky='nsew', padx=(3, 3))
        
        # Packing Frames in window
        side_bottom.grid(row=2, padx=(2, 2)) 
        self.sideFrame.grid(row=1, column=1, padx=(2, 4), pady=(20, 20))
        ActionControl.grid(row=2,padx=(15, 15), pady=10)
        self.ActionFrame.grid(row=1, column=0, sticky='nw')

        bottomright.grid(row=0, sticky='nw', pady=20)
        bottomleft.grid(row=0, column=1)
        bottomFrame.pack()

    def check_class(self, class_):
        """
        Update the values of the year and course dropdown menus based on the selected value of the class dropdown menu.

        Args:
            class_: A dropdown menu object representing the class selection.

        Returns:
            None
        """
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

    def add_class_record(self, tree: ttk.Treeview) -> None:
        """
        Add a new record to the Treeview widget.

        Args:
            tree (ttk.Treeview): The Treeview widget representing the table where the record will be added.

        Returns:
            None

        Summary:
        The `add_class_record` method is used to add a new record to a Treeview widget in the GUI. It checks if the record already exists and prompts the user to update it if necessary.

        Example Usage:
        ```python
        manager = PayrollManager(root)
        manager.add_class_record(tree)
        ```

        Code Analysis:
        - Get the values of the year, course, and number of lectures from the GUI.
        - Get the existing records from the Treeview widget.
        - Convert the number of lectures to an integer.
        - Check if a record with the same year and course already exists.
        - If the record exists, prompt the user to update it.
        - If the user chooses to update, find the location of the existing record and update its values.
        - If the record does not exist, insert a new row with the values into the Treeview widget.
        """
        values = (self.year.get(), self.course.get(), self.no_of_lectures.get())
        raw_row =  [(child, tree.item(child, 'values')) for child in tree.get_children()]

        # This is just for converting the number of lectures to int
        records = list(map(lambda x: [x[0], (x[1][0], x[1][1], int(x[1][2]))], raw_row))
        # checking whether record exist or not
        exists = any(x[1][:-1] == values[:-1] for x in records)

        if exists:
        
            result = messagebox.askyesno('Duplicate Found', 'it seems table already contains this record\nWould you like to update that.')
            if result:
                # if yes the where it is located
                where = list(map(lambda x: x[1][:-1] == values[:-1], records))
                entry = records[where.index(True)][0]
                tree.item(entry, values=values)
                return
            return
        tree.insert('', tk.END, values=values)


    def add_in_report(self):
        """
        Add employee details to a report table in the GUI.
        """
        # Retrieve the values of the input variables
        name = self.name_var.get()
        salary = self.sal_var.get()
        it = self.it_var.get()
        pf = self.pf_var.get()
        other = self.oth_var.get()
        deduction = int(it) + int(pf) + int(other)
        dept_type = self.dept_type.get()
        acc = self.acc_var.get()
        ifsc = self.ifsc_var.get()

        # Calculate net amount based on department type
        if self.is_teaching(dept_type, action=False):
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

        # Insert a new row into the report table with the employee details
        sr = 1
        records = self.report_table.get_children()
        if records:
            sr += len(records)
        self.report_table.insert('', tk.END, values=(sr, name, dept_type, salary, deduction, net_amount, acc, ifsc))

        # Resetting all values to default
        self.id_var.set('Employee ID')
        self.name_var.set('Employee Name')
        self.dept_type.set('Teaching')
        self.sal_var.set('Salary')
        self.it_var.set('Income Tax')
        self.pf_var.set('Prominent Fund')
        self.oth_var.set('Other Tax')
        self.acc_var.set('Account Number')
        self.ifsc_var.set('IFSC Code')
        self.add_btn.config(state=tk.DISABLED)
        self.update_btn.config(state=tk.DISABLED)
        self.delete_btn.config(state=tk.DISABLED)

        # Clear lecture info tree
        for record in self.lecture_info_tree.get_children():
            self.lecture_info_tree.delete(record)

        # Show message box indicating that the record has been added to the report
        messagebox.showinfo('Record Added', 'Record added to report\nkindly navigate to View Report')


    def export_report(self, dept_type: Literal['teaching', 'non-teaching'], date: str):
        """
        Export a report to an Excel file based on the specified department type.

        Args:
            dept_type (str): The department type. Can be either 'teaching' or 'non-teaching'.

        Returns:
            None
        """
        # Get the table widget from the GUI
        tree = self.report_table

        # Retrieve the values of each row in the table and store them in the rows list
        rows = [tree.item(row, 'values') for row in tree.get_children()]

        # Filter the rows list based on the specified dept_type
        filtered_rows = [row[1:] for row in rows if row[2].lower().replace('-', '') == dept_type]

        # Export the report to an Excel file
        filename = to_excel(filtered_rows, ('Employee Name', 'Department Type', 'Total Amount', 'Deduction', 'Net Amount', 'Account Number', 'IFSC Code'), date, dept_type)
        return filename

    def update_to_db(self):
        """
        Update the details of an employee in the database.

        Returns:
            None
        """
        id = self.id_var.get()
        name = self.name_var.get()
        dept = self.dept_type.get()
        salary = self.sal_var.get()
        it = self.it_var.get()
        pf = self.pf_var.get()
        other = self.oth_var.get()
        bankkAcc = self.acc_var.get()
        bankifsc = self.ifsc_var.get()

        new_details = EmployeeDetails(id, name, dept, salary, it, pf, other, bankkAcc, bankifsc)

        updated = self.database_manager.update(id, new_details)

        if updated:
            messagebox.showinfo('Employee Updated', 'Employee details successfully updated,\nKindly Refresh Tree.')
        else:
            messagebox.showerror('Update Failure', 'something went wrong\ncontact development team.')

    def delete_from_db(self):
        """
        Deletes an employee from the database.

        :return: None
        """
        employee_id = self.id_var.get()
        department_type = self.dept_type.get()

        removed = self.database_manager.remove(employee_id, department_type)

        if removed:
            messagebox.showinfo('Employee Deleted', 'Employee successfully removed from database\nKindly Refresh Tree.')
        else:
            messagebox.showerror('Deletion Failure', 'Something went wrong\nContact development team.')


    def show_employees(self, tree: ttk.Treeview, dept_type: Literal['teaching', 'non-teaching']):
        """
        Updates the tree widget with employee details based on their department type.

        Args:
            tree (ttk.Treeview): The tree widget where the employee details will be displayed.
            dept_type (Literal['teaching', 'non-teaching']): The department type of the employees to be displayed.

        Returns:
            None
        """
        # Clear the existing entries in the tree widget
        tree.delete(*tree.get_children())

        # Retrieve the employee details from the database for the specified dept_type
        employees = self.database_manager.getAll(dept_type)

        # Insert the employee details as rows in the tree widget
        for entry in employees:
            tree.insert('', tk.END, values=tuple(entry.values()))

    def generate_report(self):
        """
        Creates a report table in the GUI and allows the user to export the report for teaching and non-teaching employees.
        """
        # Create a frame for the report table in the GUI
        treeFrame = ttk.Frame(self.generate_tab)
        treeFrame.pack()

        # Create a scrollbar for the report table
        scroll = ttk.Scrollbar(treeFrame)
        scroll.pack(side='right', fill='y')

        # Define the columns for the report table
        columns = ['sr', 'name', 'type', 'amount', 'deduction', 'netamount', 'bankaccount', 'bankifsc']

        # Create a Treeview widget for the report table with the specified columns
        self.report_table = ttk.Treeview(treeFrame, yscrollcommand=scroll.set, show='headings', column=columns, height=10)

        # Set the column widths and headings for the report table
        column_widths = [40, 125, 120, 90, 80, 80, 120, 100]
        column_headings = ['Sr No.', 'Employee Name', 'Department Type', 'Total Amount', 'Deduction', 'Net Amount', 'Account Number', 'IFSC Code']

        for i, column in enumerate(columns):
            self.report_table.column(column, width=column_widths[i], minwidth=column_widths[i], anchor='w')
            self.report_table.heading(column, text=column_headings[i], anchor='w')

        # Configure the scrollbar to scroll the report table
        scroll.config(command=self.report_table.yview)

        # Pack the report table in the frame
        self.report_table.pack(padx=(3, 3))

        # Create a label frame for the export menu
        exportMenu = ttk.LabelFrame(self.generate_tab, text='Export Menu')

        # Create buttons for exporting the report for teaching and non-teaching employees
        date_entry = ttk.Entry(exportMenu)
        date_placeholder = "Date: DD-MM-YYYY"
        date_entry.insert(0, date_placeholder)
        date_entry.bind('<FocusIn>', lambda e: self._on_entry_focus_in(date_entry, date_placeholder))
        date_entry.bind('<FocusOut>', lambda e: self._on_entry_focus_out(date_entry, date_placeholder))
        export_teaching = ttk.Button(exportMenu, text='Export Teaching', command=lambda: validate_then_export(dept_type='teaching', placeholder=date_placeholder))
        export_nonteaching = ttk.Button(exportMenu, text='Export Non-Teaching', command=lambda: validate_then_export(dept_type='non-teaching', placeholder=date_placeholder))

        def validate_then_export(dept_type, placeholder):
            if date_entry.get() == placeholder:
                messagebox.showerror('Date Required', 'please enter date of report before exporting')
            else:
                date = date_entry.get()
                match = re.match(r'(\d{1,2}\-\d{1,2}\-\d{4})', date)
                if match:
                    filename = self.export_report(dept_type, date)
                    messagebox.showinfo('Report Generated', f"All records is succesfully exported in\nFilename: {filename}")
                else:
                    messagebox.showerror('Improper Date Format', 'please enter date in the correct format as mentioned')
    
        # Grid the buttons in the export menu
        date_entry.grid(row=0, padx=(5, 5), pady=(5, 5))
        export_teaching.grid(row=0, column=1, padx=(5, 5), pady=(5, 5))
        export_nonteaching.grid(row=0, column=2, padx=(5, 5), pady=(5, 5))

        # Pack the export menu in the GUI
        exportMenu.pack(pady=(10, 10))

    def theme_callback(self):
        """
        Callback function triggered when the user clicks on the "Dark Theme" checkbutton.
        Changes the theme of the GUI based on the state of the checkbutton.
        """
        if self.theme_mode.instate(['selected']):
            self.style.theme_use('forest-dark')
        else:
            self.style.theme_use('forest-light')

    def _refresh_tree(self, tree: ttk.Treeview, values: Union[List[tuple], List[dict]]):
        """
        Update the data displayed in a ttk.Treeview widget by deleting all existing rows and inserting new rows based on the provided values.

        Args:
            tree (ttk.Treeview): The ttk.Treeview widget to be updated.
            values (Union[List[tuple], List[dict]]): A list of tuples or dictionaries that contain the data to be displayed in the treeview.

        Returns:
            None
        """
        # Delete all existing rows in the treeview widget
        tree.delete(*tree.get_children())

        # Insert new rows based on the provided values
        for val in values:
            if isinstance(val, dict):
                tree.insert('', tk.END, values=tuple(val.values()))
            else:
                tree.insert('', tk.END, values=val)

    def _check_is_ug(self, row: tuple):
        """ Helper function to check whether class is Under Graduate or Post Graduate """
        if row[1].startswith('M'):
            return False
        return True

    def _on_entry_focus_in(self, widget, placeholder_text):
        """
        Handles the focus in event of an entry widget.

        Args:
            widget (tk.Entry): The entry widget that triggered the focus event.
            placeholder_text (str): The placeholder text that is displayed in the entry widget.

        Returns:
            None
        """
        if widget.get() == placeholder_text:
            widget.delete(0, tk.END)
            
    def _on_entry_focus_out(self, widget: ttk.Widget.bbox, placeholder_text):
        """
        Handles the focus out event of an entry widget.

        Args:
            widget (ttk.Widget.bbox): The entry widget that triggered the focus event.
            placeholder_text (str): The placeholder text that is displayed in the entry widget.

        Returns:
            None
        """
        if not widget.get():
            widget.insert(0, placeholder_text)
    
    def _get_selection(self, tree: ttk.Treeview):
        row_id = tree.selection()[0]
        row_values = self.table.item(row_id, 'values')
        id, name, type, sal, pf, it, oth, acc, ifsc = row_values
        self.id_var.set(id)
        self.emp_id.config(state=tk.DISABLED)
        self.name_var.set(name)
        self.dept_type.set(type)
        self.sal_var.set(sal)
        self.pf_var.set(pf)
        self.it_var.set(it)
        self.oth_var.set(oth)
        self.acc_var.set(acc)
        self.ifsc_var.set(ifsc)
        self.add_btn.config(state=tk.NORMAL)
        self.update_btn.config(state=tk.NORMAL)
        self.delete_btn.config(state=tk.NORMAL)

if __name__ == '__main__':
    root = tk.Tk()
    app = PayrollManager(root)
    root.mainloop()