import pandas as pd


def convert_time_columns(df):
    """
    Convert arrival and departure columns to datetime.
    """

    df["Arrival_time"] = pd.to_datetime(
        df["Arrival_time"],
        format="%H:%M:%S",
        errors="coerce"
    )

    df["Departure_Time"] = pd.to_datetime(
        df["Departure_Time"],
        format="%H:%M:%S",
        errors="coerce"
    )

    return df


def calculate_halt_time(df):
    """
    Calculate halt time in minutes.
    """

    df["Halt_Time_Minutes"] = (
        df["Departure_Time"] - df["Arrival_time"]
    ).dt.total_seconds() / 60

    df["Halt_Time_Minutes"] = (
        df["Halt_Time_Minutes"]
        .fillna(0)
    )

    return df


def create_journey_summary(df):
    """
    Create train-level journey analytics.
    """

    sorted_df = df.sort_values(
        by=["Train_No", "Distance"]
    )

    journey_summary = (
        sorted_df.groupby("Train_No")
        .agg(
            Start_Time=("Arrival_time", "first"),
            End_Time=("Departure_Time", "last"),
            Total_Distance=("Distance", "max")
        )
        .reset_index()
    )

    journey_summary["Journey_Duration_Hours"] = (
        (
            journey_summary["End_Time"]
            - journey_summary["Start_Time"]
        ).dt.total_seconds()
    ) / 3600

    journey_summary[
        "Journey_Duration_Hours"
    ] = journey_summary[
        "Journey_Duration_Hours"
    ].apply(
        lambda x: x + 24 if x < 0 else x
    )

    return journey_summary


def classify_route(distance):
    """
    Categorize train routes by distance.
    """

    if distance < 300:
        return "Short"

    elif distance <= 800:
        return "Medium"

    else:
        return "Long"


def add_route_category(journey_summary):
    """
    Add route category column.
    """

    journey_summary["Route_Category"] = (
        journey_summary["Total_Distance"]
        .apply(classify_route)
    )

    return journey_summary