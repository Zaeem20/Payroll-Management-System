import pandas as pd
from typing import List, Literal
from datetime import datetime

def to_excel(data: List[tuple], columns, date=None, collection: Literal['teaching', 'non-teaching']='teaching'):
    if date is None:
        date = datetime.now(datetime.now().strftime("%d-%m-%y"))
    else:
        date = datetime(*list(map(int, date.split('-')))[::-1]).strftime("%d-%m-%y")
    df = pd.DataFrame(data, columns=columns)
    df.index = df.index + 1
    df.index.name = 'sr no.'
    filename = f'Payroll-report-{collection}-[{date}].xlsx'
    df.to_excel(filename)
    return filename
