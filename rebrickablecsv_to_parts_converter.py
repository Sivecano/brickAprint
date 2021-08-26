import pandas

def convert(rebrickable_csv_path: str):
    csv_data = pandas.read_csv(rebrickable_csv_path)
    return csv_data[['Quantity', 'Part', 'Color']]