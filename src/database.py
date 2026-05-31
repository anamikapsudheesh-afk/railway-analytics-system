import sqlite3
import pandas as pd


def create_connection(db_path):
    """
    Create SQLite database connection.
    """

    connection = sqlite3.connect(db_path)

    return connection


def load_dataframe_to_sql(df, table_name, connection):
    """
    Load dataframe into SQLite table.
    """

    df.to_sql(
        table_name,
        connection,
        if_exists="replace",
        index=False
    )

    print(f"{table_name} table loaded successfully")


def read_table(query, connection):
    """
    Read SQL query into dataframe.
    """

    return pd.read_sql(query, connection)