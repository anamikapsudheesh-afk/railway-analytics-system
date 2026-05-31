from flask import Flask, render_template, request, redirect, session
import sqlite3
import pandas as pd
import plotly.express as px

app = Flask(__name__)
app.secret_key = "railconnect_secret_key"

DATA_PATH = "data/raw/railway_dataset.csv"
USER_DB = "database/users.db"


def init_user_db():
    conn = sqlite3.connect(USER_DB)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def load_data():
    df = pd.read_csv(DATA_PATH)
    df.columns = df.columns.str.strip()
    return df


def build_train_summary():
    df = load_data()

    train_summary = (
        df.sort_values(["Train_No", "SN"])
        .groupby("Train_No")
        .agg(
            Source=("Station_Name", "first"),
            Destination=("Station_Name", "last"),
            Total_Stops=("Station_Name", "count"),
            Total_Distance=("Distance", "max")
        )
        .reset_index()
    )

    train_summary["Route_Category"] = pd.cut(
        train_summary["Total_Distance"],
        bins=[0, 500, 1500, float("inf")],
        labels=["Short Route", "Medium Route", "Long Route"]
    )

    return train_summary


@app.route("/")
def index():
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect(USER_DB)
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                (name, email, password)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return redirect("/login")

        conn.close()
        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect(USER_DB)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        )

        user = cursor.fetchone()
        conn.close()

        if user:
            session["user_id"] = user[0]
            session["user_name"] = user[1]
            return redirect("/home")

        return redirect("/login")

    return render_template("login.html")


@app.route("/home")
def home():
    if "user_name" not in session:
        return redirect("/login")

    return render_template("home.html", name=session["user_name"])


@app.route("/dashboard")
def dashboard():
    if "user_name" not in session:
        return redirect("/login")

    df = load_data()
    train_summary = build_train_summary()

    total_trains = train_summary["Train_No"].nunique()
    total_stations = df["Station_Name"].nunique()
    longest_route = int(train_summary["Total_Distance"].max())
    avg_stops = round(train_summary["Total_Stops"].mean(), 2)

    station_frequency = (
        df["Station_Name"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    station_frequency.columns = ["Station_Name", "Train_Count"]

    fig1 = px.bar(
        station_frequency,
        x="Station_Name",
        y="Train_Count",
        title="Top 10 High-Traffic Stations"
    )

    fig1.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    chart1 = fig1.to_html(full_html=False)

    route_counts = (
        train_summary["Route_Category"]
        .value_counts()
        .reset_index()
    )

    route_counts.columns = ["Route_Category", "Count"]

    fig2 = px.pie(
        route_counts,
        names="Route_Category",
        values="Count",
        title="Route Category Distribution"
    )

    fig2.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    chart2 = fig2.to_html(full_html=False)

    # LEVEL 5 — Advanced Analysis Chart
    level5_data = (
        train_summary
        .groupby("Route_Category")
        .agg(
            Average_Distance=("Total_Distance", "mean"),
            Train_Count=("Train_No", "count")
        )
        .reset_index()
    )

    fig3 = px.bar(
        level5_data,
        x="Route_Category",
        y="Average_Distance",
        color="Route_Category",
        title="Level 5: Average Route Distance by Route Category",
        text="Train_Count"
    )

    fig3.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    chart3 = fig3.to_html(full_html=False)

    insights = [
        f"The dataset contains {total_trains} unique trains.",
        f"{total_stations} unique stations are present in the schedule data.",
        f"The longest recorded route distance is {longest_route} km.",
        f"The average number of stops per train is {avg_stops}."
    ]

    return render_template(
        "dashboard.html",
        total_trains=total_trains,
        top_stations=total_stations,
        longest_route=longest_route,
        avg_duration=avg_stops,
        chart1=chart1,
        chart2=chart2,
        chart3=chart3,
        insights=insights
    )


@app.route("/smart-search", methods=["GET", "POST"])
def smart_search():
    if "user_name" not in session:
        return redirect("/login")

    df = load_data()
    df = df.sort_values(["Train_No", "SN"])

    stations = sorted(df["Station_Name"].dropna().unique())

    results = []

    if request.method == "POST":
        source = request.form["source"]
        destination = request.form["destination"]
        results = sorted(results, key=lambda x: (x["stops"], x["distance"]))

        print("Source:", source)
        print("Destination:", destination)
        print("Results Found:", len(results))

        for train_no, train_data in df.groupby("Train_No"):

            train_data = train_data.sort_values("SN").reset_index(drop=True)
            station_list = train_data["Station_Name"].tolist()

            if source in station_list and destination in station_list:

                source_index = station_list.index(source)
                destination_index = station_list.index(destination)

                if source_index < destination_index:

                    source_distance = train_data.loc[source_index, "Distance"]
                    destination_distance = train_data.loc[destination_index, "Distance"]

                    estimated_distance = destination_distance - source_distance
                    stops = destination_index - source_index

                    results.append({
                        "train_no": train_no,
                        "source": source,
                        "destination": destination,
                        "stops": stops,
                        "distance": round(estimated_distance, 2)
                    })

    return render_template(
        "smart_search.html",
        stations=stations,
        results=results
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


if __name__ == "__main__":
    init_user_db()
    app.run(debug=True)