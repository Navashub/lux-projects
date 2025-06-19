from extract_debt_data import fetch_debt_data
from transform import transform_debt_data
from load_data import load_data_to_postgres

def main():
    raw_data = fetch_debt_data()
    df = transform_debt_data(raw_data)
    load_data_to_postgres(df)

if __name__ == "__main__":
    main()
