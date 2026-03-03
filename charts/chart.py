import altair as alt

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
        .properties(title="Q1: Team Performance Across Seasons")
    )
    return chart
