import pandas as pd
from typing import List
from datetime import datetime

def to_excel(data: List[tuple], columns):
    df = pd.DataFrame(data, columns=columns)
    df.index = df.index + 1
    df.index.name = 'sr no.'
    
    df.to_excel(f'payroll-report_{datetime.now().strftime("%d-%m-%y")}.xlsx')
    
