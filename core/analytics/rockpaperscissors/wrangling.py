from dataclasses import dataclass
import pandas as pd
from pandas import DataFrame


@dataclass
class Dataset:
    customers = "https://raw.githubusercontent.com/dicodingacademy/dicoding_dataset/main/DicodingCollection/customers.csv"
    orders = "https://raw.githubusercontent.com/dicodingacademy/dicoding_dataset/main/DicodingCollection/orders.csv"
    products = "https://raw.githubusercontent.com/dicodingacademy/dicoding_dataset/main/DicodingCollection/products.csv"
    sales = "https://raw.githubusercontent.com/dicodingacademy/dicoding_dataset/main/DicodingCollection/sales.csv"


class AssessingData():
    def __init__(self, dataset: Dataset):
        self.load_data_csv = pd.read_csv(dataset)

    # TODO: Returning base information of the data
    def __repr__(self) -> str:

        base_info = f"Data Informations: \n{self.load_data_csv.info()}\n\n"
        missing_value_total = f"Missing Value\n{self.load_data_csv.isna().sum()}\n\n"
        duplicate_data_total = f"Total Duplicate Data: {self.load_data_csv.duplicated().sum()}\n\n"
        descriptions = f"Desriptions: {self.load_data_csv.describe()}\n\n"

        data_info = base_info + missing_value_total + duplicate_data_total + descriptions
        return data_info

    # TODO: return first 5 data
    def first_five_data(self) -> DataFrame:
        return self.load_data_csv.head()

    # * Can apply to all data
    def base_remove_duplicate(self):
        return self.load_data_csv.drop_duplicates(inplace=True)

    # * Can apply to all data, based on considerations
    def missing_value_repair(self, value):
        return self.load_data_csv.fillna(value=value, inplace=True)

    # ! ONLY FOR CUSTOMER DATA
    # TODO: replace inapropriate data based on max data on age feature
    def customer_inaccurate_value(self, value):
        return self.load_data_csv.age.replace(self.load_data_csv.age.max(), value, inplace=True)

    # ! ONLY FOR ORDER DATA
    # TODO: Fixing date data types
    def order_date_type_fix(self):
        datetime_columns = ["order_date", "delivery_date"]
        for column in datetime_columns:
            self.load_data_csv[column] = pd.to_datetime(
                self.load_data_csv[column])

    # ! ONLY FOR SALES DATA
    # TODO: Fill the missing with total price
    def sales_total_fill(self):
        self.load_data_csv["total_price"] = self.load_data_csv["price_per_unit"] * \
            self.load_data_csv["quantity"]
        return self.load_data_csv.isna().sum()


def main() -> None:

    # * You can apply to all data on Dataset
    customer_data = AssessingData(Dataset.customers)

    print(customer_data)
    print(customer_data.first_five_data())

    # TODO: YOU CAN APPLY THE FUNCTION BASED ON YOUR DATA CONDITIONS
    # ....
    # ....
    # ....


if __name__ == "__main__":
    main()
