import pandas as pd
from typing import List, Literal
from datetime import datetime
from tkinter.filedialog import asksaveasfilename

def to_excel(data: List[tuple], columns, date=None, collection: Literal['teaching', 'non-teaching']='teaching'):
    try:
        if date is None:
            date = datetime.now(datetime.now().strftime("%d-%m-%y"))
        else:
            date = datetime(*list(map(int, date.split('-')))[::-1]).strftime("%d-%m-%y")
        df = pd.DataFrame(data, columns=columns)
        df.index = df.index + 1
        df.index.name = 'sr no.'
        filetypes = [('Excel Files', '*.xlsx'), ('All Files', "*")]
        initial_filename = f'Payroll-report-{collection}-[{date}].xlsx'    
        file_path = asksaveasfilename(defaultextension='.xlsx', initialfile=initial_filename, filetypes=filetypes)

        if file_path:
            df.to_excel(file_path)
            return True, file_path
    
    except Exception as e:
        return False, e

