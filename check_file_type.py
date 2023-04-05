import pandas as pd
from pathlib import Path, PureWindowsPath

# print(filepath)

pd.__version__

def validate_xl_file_type(filename)-> bool:
    """
    In the c:/xl/ folder there may be other types of data files added
    Unless these are .xls files they cannot be imported so this will check forist
    """
#    for files in filepath:
    use_file = False

    if Path(filename.lower()).suffix == ".xls":
        use_file=True
        print(f"Filename {filename} is an .xls file and will be imported: {Path(filename.lower()).suffix}")
    elif Path(filename.lower()).suffix == ".xlsx":
        use_file=False
        print(f"Filename {filename} is an .xlsx file will be not imported: {Path(filename.lower()).suffix}")
    elif Path(filename.lower()).suffix == ".csv":
        use_file=False
        print(f"Filename {filename} is an .csv file and will not be imported:: {Path(filename.lower()).suffix}")
    elif Path(filename.lower()).suffix == ".txt":
        use_file=False
        print(f"Filename {filename} is an .txt file and will not be imported:: {Path(filename.lower()).suffix}")

    return use_file
