import pandas as pd

def load_data():
    df1 = pd.read_csv("data/PL-season-2324.csv")
    df2 = pd.read_csv("data/PL-season-2425.csv")

    df1["Season"] = "2023-24"
    df2["Season"] = "2024-25"

    df = pd.concat([df1, df2], ignore_index=True)

    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    df["GD"] = df["FTHG"] - df["FTAG"]

    def points(row):
        if row["FTR"] == "H":
            return 3
        elif row["FTR"] == "A":
            return 0
        else:
            return 1

    df["HomePoints"] = df.apply(lambda r: points(r), axis=1)
    df["AwayPoints"] = df.apply(
        lambda r: 3 - points(r) if r["FTR"] != "D" else 1, axis=1
    )

    home = df[
        [
            "Season", "Date", "HomeTeam", "FTHG", "FTAG", "GD",
            "HomePoints", "HS", "HST", "HC"
        ]
    ].rename(
        columns={
            "HomeTeam": "Team",
            "FTHG": "GoalsFor",
            "FTAG": "GoalsAgainst",
            "HomePoints": "Points",
            "HS": "Shots",
            "HST": "ShotsOnTarget",
            "HC": "Corners",
        }
    )

    away = df[
        [
            "Season", "Date", "AwayTeam", "FTAG", "FTHG", "GD",
            "AwayPoints", "AS", "AST", "AC"
        ]
    ].rename(
        columns={
            "AwayTeam": "Team",
            "FTAG": "GoalsFor",
            "FTHG": "GoalsAgainst",
            "AwayPoints": "Points",
            "AS": "Shots",
            "AST": "ShotsOnTarget",
            "AC": "Corners",
        }
    )

    team_df = pd.concat([home, away], ignore_index=True)

    team_df = team_df.sort_values(["Season", "Team", "Date"])
    team_df["Matchweek"] = (
        team_df.groupby(["Season", "Team"]).cumcount() + 1
    )

    team_df["GoalsFor_roll"] = (
        team_df.groupby(["Season", "Team"])["GoalsFor"]
        .transform(lambda s: s.rolling(3, min_periods=1).mean())
    )
    team_df["Shots_roll"] = (
        team_df.groupby(["Season", "Team"])["Shots"]
        .transform(lambda s: s.rolling(3, min_periods=1).mean())
    )
    team_df["ShotsOnTarget_roll"] = (
        team_df.groupby(["Season", "Team"])["ShotsOnTarget"]
        .transform(lambda s: s.rolling(3, min_periods=1).mean())
    )
    team_df["Corners_roll"] = (
        team_df.groupby(["Season", "Team"])["Corners"]
        .transform(lambda s: s.rolling(3, min_periods=1).mean())
    )

    # -----------------------------
    # Q1 team_summary (HW3 In[6])
    # -----------------------------
    team_summary = (
        team_df.groupby(["Season", "Team"], as_index=False)
        .agg({
            "Points": "sum",
            "GoalsFor": "sum",
            "GoalsAgainst": "sum",
            "GD": "sum",
        })
    )

    melted = team_df.melt(
        id_vars=["Season", "Team", "Matchweek"],
        value_vars=[
            "GoalsFor_roll",
            "Shots_roll",
            "ShotsOnTarget_roll",
            "Corners_roll",
        ],
        var_name="metric",
        value_name="value",
    )

    return df, team_summary, melted
