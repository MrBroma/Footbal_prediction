import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime

# Load data from the dataset.csv file
def load_data():
    df = pd.read_csv('dataset.csv')
    df['Time'] = pd.to_datetime(df['Time'])  
    return df

# Filter data based on the selected season's date range
def filter_season_data(df, season_dates):
    start_date, end_date = season_dates
    mask = (df['Time'] >= start_date) & (df['Time'] <= end_date)
    return df[mask]

# Function to calculate team points and ranking
def calculate_team_points(df):
    team_points = {}

    for _, row in df.iterrows():
        home_team = row['HomeTeam']
        away_team = row['AwayTeam']
        result = row['FTR']

        if result == 'H':  # Home Win
            team_points[home_team] = team_points.get(home_team, 0) + 3
        elif result == 'A':  # Away Win
            team_points[away_team] = team_points.get(away_team, 0) + 3
        elif result == 'D':  # Draw
            team_points[home_team] = team_points.get(home_team, 0) + 1
            team_points[away_team] = team_points.get(away_team, 0) + 1

    # Convert to DataFrame and sort by points
    points_df = pd.DataFrame(team_points.items(), columns=['Team', 'Points'])
    points_df = points_df.sort_values(by='Points', ascending=False).reset_index(drop=True)
    return points_df

# Function to plot win statistics as a pie chart
def plot_win_statistics(df):
    home_wins = df['FTR'].value_counts().get('H', 0)
    away_wins = df['FTR'].value_counts().get('A', 0)
    draws = df['FTR'].value_counts().get('D', 0)

    labels = ['Home Wins', 'Away Wins', 'Drawn']
    sizes = [home_wins, away_wins, draws]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig)

# Function to plot win statistics as a bar chart
def plot_win_bar_chart(df):
    home_wins = df['FTR'].value_counts().get('H', 0)
    away_wins = df['FTR'].value_counts().get('A', 0)
    draws = df['FTR'].value_counts().get('D', 0)

    data = {
        'Category': ['Home Wins', 'Away Wins', 'Drawn'],
        'Count': [home_wins, away_wins, draws]
    }

    bar_df = pd.DataFrame(data)
    fig = px.bar(bar_df, x='Category', y='Count', title='Win Statistics')
    st.plotly_chart(fig)

# Dictionary to store season date ranges
seasons = {
    '2024/2025': ('2024-07-20', '2025-06-15'),
    '2023/2024': ('2023-07-20', '2024-06-15'),
    '2022/2023': ('2022-07-20', '2023-06-15'),
    '2021/2022': ('2021-07-20', '2022-06-15'),
    '2020/2021': ('2020-07-20', '2021-06-15'),
    '2019/2020': ('2019-07-20', '2020-06-15'),
}

# Streamlit app layout
st.title("Football League Rankings & Statistics")

# Create a select box to choose the season
selected_season = st.selectbox("Choose a Season", list(seasons.keys()))
season_dates = seasons[selected_season]

# Load the full dataset
df = load_data()

# Filter data based on the selected season
season_df = filter_season_data(df, season_dates)

# Display the team rankings
st.write(f"Team Rankings for Season {selected_season}")
points_df = calculate_team_points(season_df)
st.dataframe(points_df)

# Show win statistics
st.write(f"Win Statistics for Season {selected_season}")
plot_type = st.selectbox("Choose Chart Type", ["Pie Chart", "Bar Chart"])

if plot_type == "Pie Chart":
    plot_win_statistics(season_df)
else:
    plot_win_bar_chart(season_df)






