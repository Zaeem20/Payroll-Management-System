from typing import Literal, Optional

class EmployeeDetails(object):
    def __init__(self, id: Optional[int], name: str, dept_type: Literal['teaching', 'non-teaching'], salary: int
                ,income_tax: int, prominent_fund, other_tax,account_number: int, ifsc_code: str):
        self.id = id 
        self.empName = name
        self.deptType = dept_type.lower()
        self.salary = salary
        self.income_tax = income_tax
        self.prominent_fund = prominent_fund
        self.other_tax = other_tax
        self.bankAccount = account_number
        self.ifsc_code = ifsc_code

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, data: dict):
        return cls(*data.values())

# obj = EmployeeDetails('zaeem', 10000, 'teaching', 881035282846, False)
# print(obj.to_dict())