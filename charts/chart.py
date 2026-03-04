import altair as alt

alt.data_transformers.disable_max_rows()

def chart_q1(team_summary):
    team_select = alt.selection_point(fields=["Team"], empty="none")
    season_select = alt.selection_point(
        fields=["Season"],
        bind=alt.binding_select(options=["2023-24", "2024-25"])
    )

    chart = (
        alt.Chart(team_summary)
        .mark_point(size=140)
        .encode(
            x=alt.X("Points:Q", title="Total Points"),
            y=alt.Y("Team:N", sort="-x"),
            color=alt.Color("Team:N"),
            shape=alt.Shape(
                "Season:N",
                scale=alt.Scale(
                    domain=["2023-24", "2024-25"],
                    range=["circle", "triangle-up"]
                )
            ),
            tooltip=["Team", "Season", "Points", "GD"],
            opacity=alt.condition(season_select, alt.value(1), alt.value(0.2))
        )
        .add_params(team_select, season_select)
        .properties(
            title="Q1: Team Performance Across Seasons"
        )
    )
    return chart

def chart_q2_single_season(melted, season):
    season_df = melted[melted["Season"] == season]

    metric_options = sorted(season_df["metric"].unique())
    metric_select = alt.selection_point(
        fields=["metric"],
        bind=alt.binding_select(options=metric_options),
        value=metric_options[0]
    )

    hover_team = alt.selection_point(fields=["Team"], on="mouseover", empty="none")

    chart = (
        alt.Chart(season_df)
        .mark_line()
        .encode(
            x="Matchweek:Q",
            y=alt.Y("value:Q", title="Rolling Average"),
            color="Team:N",
            opacity=alt.condition(hover_team, alt.value(1), alt.value(0.15)),
            strokeWidth=alt.condition(hover_team, alt.value(3), alt.value(1)),
            tooltip=["Team", "Season", "Matchweek", "value"]
        )
        .transform_filter(metric_select)
        .add_params(metric_select, hover_team)
        .properties(title=f"Q2: Attacking Performance — {season}")
    )

    return chart
    
def chart_q4_scatter(df):
    brush_extremes = alt.selection_interval()

    chart = (
        alt.Chart(df)
        .mark_circle(size=80)
        .encode(
            x=alt.X("FTHG:Q", title="Home Goals"),
            y=alt.Y("FTAG:Q", title="Away Goals"),
            color=alt.condition(brush_extremes, alt.value("red"), alt.value("steelblue")),
            tooltip=["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR"]
        )
        .add_params(brush_extremes)
        .properties(title="Q4: Extreme Match Outcomes")
    )
    return chart

def chart_q4_table(df):
    brush_extremes = alt.selection_interval()

    table = (
        alt.Chart(df)
        .transform_filter(brush_extremes)
        .transform_calculate(
            MatchLabel='datum.HomeTeam + " " + datum.FTHG + "–" + datum.FTAG + " " + datum.AwayTeam'
        )
        .transform_window(row_number="row_number()")
        .transform_filter("datum.row_number <= 15")
        .mark_text(align="left")
        .encode(
            y=alt.Y("row_number:O", axis=None),
            text="MatchLabel:N"
        )
        .properties(title="Selected Matches (Top 15)")
    )
    return table
