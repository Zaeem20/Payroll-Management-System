def calculateSalary(salary: int, deduction: int, no_of_ug_lectures: int = 0, no_of_pg_lectures: int = 0, is_teaching: bool = True) -> int:
    """
    Calculates the total salary after deducting a specified amount.

    Args:
        salary (int): The base salary of the person.
        deduction (int): The amount to be deducted from the salary.
        no_of_ug_lectures (int, optional): The number of undergraduate lectures taught by the person. Defaults to 0.
        no_of_pg_lectures (int, optional): The number of postgraduate lectures taught by the person. Defaults to 0.
        is_teaching (bool, optional): A boolean flag indicating whether the person is teaching or not. Defaults to True.

    Returns:
        int: The total salary after deducting the specified amount.
    """
    if is_teaching:
        ug_rate = no_of_ug_lectures * 550
        pg_rate = no_of_pg_lectures * 750
        total = salary + ug_rate + pg_rate - deduction
    else:
        total = salary - deduction
    return total