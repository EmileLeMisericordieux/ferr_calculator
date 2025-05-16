import pandas as pd


class FerrCalculator():
    def __init__(
        self,
        start_value: float = 200_000,
        start_age: int = 71,
        end_age: int = 90,
        interest_rate: float = 6.00,
        start_paying_on_year: int = 2,
        paying_type: str = "Minimum",
        fix_value: float = 0,
        inflation_rate: float = 1.5
    ):
        self.start_value = start_value
        self.start_age = start_age
        self.end_age = end_age
        self.interest_rate = interest_rate
        self.start_paying_on_year = start_paying_on_year
        self.paying_type = paying_type
        self.fix_value = fix_value
        self.inflation_rate = inflation_rate

        self.min_withdrawal = pd.DataFrame({
            'age': [
                50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64,
                65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75,
                76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86,
                87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97,
                98, 99, 100
            ],
            'min_withdraw': [
                2.50, 2.56, 2.63, 2.70, 2.78,
                2.86, 2.94, 3.03, 3.13, 3.23, 3.33, 3.45,
                3.57, 3.70, 3.85, 4.00, 4.17, 4.35, 4.55,
                4.76, 5.00, 5.28, 5.40, 5.53, 5.67, 5.82,
                5.98, 6.17, 6.36, 6.58, 6.82, 7.08, 7.38,
                7.71, 8.08, 8.51, 8.99, 9.55, 10.21, 10.99,
                11.92, 13.06, 14.49, 16.34, 18.79, 20.00,
                20.00, 20.00, 20.00, 20.00, 20.00
            ]
        })

    def calculate_payments_and_value(self, df):
        year_payment = []
        end_year_value = []
        time_counter = 0
        no_more_money_flag = False
        ferr_value = self.start_value
        for w in df['min_withdraw']:
            if self.start_paying_on_year == 1:

                payment = max(
                    (ferr_value * (w/100)),
                    self.fix_value + (self.fix_value * ((1 + self.inflation_rate/100)**time_counter - 1))
                )

                if (ferr_value - payment) < 0:
                    payment = ferr_value
                    no_more_money_flag = True

                else:
                    ferr_value = ferr_value - payment

                if no_more_money_flag:
                    ferr_value = 0

                year_payment.append(round(payment))

            else:
                year_payment.append(0)
                self.start_paying_on_year = self.start_paying_on_year - 1

            ferr_value = ferr_value * (1 + (self.interest_rate/100))
            end_year_value.append(round(ferr_value))
            time_counter += 1

        df['year_payment'] = year_payment
        df['end_year_value'] = end_year_value

        return df
    
    def reformat_df(self, df):
        df.rename(columns={
            'age': 'Age',
            'min_withdraw': 'Pourcentage de Retrait',
            'year_payment': 'Versement Annuel',
            'end_year_value': "Valeur à la fin de l'année",
            'start_year_value': "Valeur au début de l'année",
        }, inplace=True)

        df = df[[
            'Age',
            "Valeur au début de l'année",
            'Versement Annuel',
            'Pourcentage de Retrait',
            "Valeur à la fin de l'année"
        ]]

        return df

    def calculate(self):
        self.yrs = pd.DataFrame({'age': [y for y in range(self.start_age, self.end_age+1)]})
        df = self.yrs.merge(self.min_withdrawal, on="age", how='left')
        df = self.calculate_payments_and_value(df)
        df["start_year_value"] = [self.start_value] + df["end_year_value"].iloc[:-1].tolist()
        df = df[df['start_year_value'] != 0]

        if self.paying_type != "Minimum":
            df['min_withdraw'] =  (df["year_payment"] / df['start_year_value'])

        else:
            df['min_withdraw'] = df['min_withdraw'] / 100
        df = self.reformat_df(df)
        return df

class NoMinimumCalculator(FerrCalculator):
    def __init__(
        self,
        start_value = 200000,
        start_age = 71,
        end_age = 90,
        interest_rate = 6,
        start_paying_on_year = 2,
        paying_type = "Fixe",
        fix_value = 0,
        inflation_rate = 1.5
    ):
        super().__init__(
            start_value,
            start_age,
            end_age,
            interest_rate,
            start_paying_on_year,
            paying_type,
            fix_value,
            inflation_rate
        )

        self.min_withdrawal = pd.DataFrame({
            'age': [i for i in range(0, 101)],
            'min_withdraw': [0 for i in range(0, 101)]
        })


def add_thousand_separator_with_dollar(df, column):
    """
    Format a numeric column with a space as thousands separator and a $ sign at the end.

    Args:
        df (pd.DataFrame): The DataFrame.
        column (str): The name of the column to format.

    Returns:
        pd.DataFrame: DataFrame with the formatted column (as strings).
    """
    df = df.copy()
    df[column] = df[column].apply(
        lambda x: f"{x:,.0f}".replace(",", " ") + "$" if pd.notnull(x) else ""
    )
    return df

def format_percent_column(df, column, decimals=0):
    """
    Format a numeric column as a percentage with space as thousands separator and % at the end.

    Args:
        df (pd.DataFrame): The DataFrame.
        column (str): The name of the column to format.
        decimals (int): Number of decimal places to keep (default is 0).

    Returns:
        pd.DataFrame: DataFrame with the formatted column (as strings).
    """
    df = df.copy()
    format_str = f"{{:,.{decimals}f}}"
    df[column] = df[column].apply(
        lambda x: format_str.format(x * 100).replace(",", " ") + "%" if pd.notnull(x) else ""
    )
    return df
