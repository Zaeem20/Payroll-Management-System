def calculateSalary(salary, deduction, no_of_ug_lectures=0, no_of_pg_lectures = 0, is_teaching: bool = True):
    if is_teaching:
        ug_rate = no_of_ug_lectures * 550
        pg_rate = no_of_pg_lectures * 750    
    
        total = (salary + ug_rate + pg_rate) - deduction 
    else:
        total = salary - deduction
    return total