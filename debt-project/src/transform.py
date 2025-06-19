import pandas as pd

def transform_debt_data(raw_data):
    rel_data = []
    for item in raw_data[1]:
        if item['value'] is not None:
            rel_data.append({
                'country_code': item['country']['id'],
                'debt_value': item['value'],
                'year': int(item['date']),
                'debt_desc': item['indicator']['value']
            })

    df = pd.DataFrame(rel_data)
    return df
