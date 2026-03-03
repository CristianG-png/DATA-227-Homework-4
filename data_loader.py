# data_loader.py
import pandas as pd

def load_data():
    # Load CSVs
    df1 = pd.read_csv("data/PL-season-2324.csv")
    df2 = pd.read_csv("data/PL-season-2425.csv")

    # Add season labels
    df1["Season"] = "2023-24"
    df2["Season"] = "2024-25"

    # Combine raw match data
    df = pd.concat([df1, df2], ignore_index=True)

    # -----------------------------
    # Create team-level long table
    # -----------------------------
    home = df.rename(columns={
        "HomeTeam": "Team",
        "FTHG": "GoalsFor",
        "FTAG": "GoalsAgainst"
    })

    away = df.rename(columns={
        "AwayTeam": "Team",
        "FTAG": "GoalsFor",
        "FTHG": "GoalsAgainst"
    })

    team_df = pd.concat([home, away], ignore_index=True)

    # Ensure Date is datetime
    team_df["Date"] = pd.to_datetime(team_df["Date"])

    # -----------------------------
    # Compute Matchweek
    # -----------------------------
    team_df = team_df.sort_values(["Team", "Season", "Date"])
    team_df["Matchweek"] = team_df.groupby(["Team", "Season"]).cumcount() + 1

    # -----------------------------
    # Q1: Team Summary
    # -----------------------------
    team_summary = (
        team_df.groupby(["Season", "Team"], as_index=False)
        .agg({
            "GoalsFor": "sum",
            "GoalsAgainst": "sum"
        })
    )
    team_summary["GD"] = team_summary["GoalsFor"] - team_summary["GoalsAgainst"]
    team_summary["Points"] = 0  # optional unless you computed points in HW3

    # -----------------------------
    # Q2: Rolling averages
    # -----------------------------
    metrics = ["GoalsFor", "Shots", "ShotsOnTarget", "Corners"]
    for m in metrics:
        team_df[f"{m}_roll"] = (
            team_df.groupby(["Team", "Season"])[m]
            .transform(lambda x: x.rolling(5, min_periods=1).mean())
        )

    melted = team_df.melt(
        id_vars=["Team", "Season", "Matchweek"],
        value_vars=[f"{m}_roll" for m in metrics],
        var_name="metric",
        value_name="value"
    )

    return df, team_summary, melted
