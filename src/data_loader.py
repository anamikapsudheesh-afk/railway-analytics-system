import pandas as pd


def load_dataset(file_path):
    """
    Load railway dataset from CSV file.

    Parameters:
        file_path (str): Path to CSV file

    Returns:
        pandas.DataFrame
    """

    df = pd.read_csv(file_path)

    return df