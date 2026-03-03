import pandas as pd

def load_data():
    df1 = pd.read_csv("data/PL-season-2324.csv")
    df2 = pd.read_csv("data/PL-season-2425.csv")

    df1["Season"] = "2023-24"
    df2["Season"] = "2024-25"
    df = pd.concat([df1, df2], ignore_index=True)
  
    team_summary = (
        df.groupby(["Season", "Team"], as_index=False)
        .agg({
            "Points": "sum",
            "GoalsFor": "sum",
            "GoalsAgainst": "sum",
            "GD": "sum"
        })
    )

    metrics = ["GoalsFor", "Shots", "ShotsOnTarget", "Corners"]
    for m in metrics:
        df[f"{m}_roll"] = df.groupby("Team")[m].transform(lambda x: x.rolling(5, min_periods=1).mean())

    melted = df.melt(
        id_vars=["Team", "Season", "Matchweek"],
        value_vars=[f"{m}_roll" for m in metrics],
        var_name="metric",
        value_name="value"
    )

    return df, team_summary, melted
