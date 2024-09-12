import streamlit as st
import pandas as pd

# Load the dataset from 'dataset.csv'
@st.cache_data
def load_data():
    df = pd.read_csv('ML_data.csv')
    df['Time'] = pd.to_datetime(df['Time'])  # Ensure Time column is in datetime format
    return df

# Calculate the team points based on match results for the selected season
def calculate_team_points(df):
    team_points = {}

    # Loop through each match to calculate points
    for _, row in df.iterrows():
        home_team = row['HomeTeam']
        away_team = row['AwayTeam']
        result = row['FTR']  # Full Time Result

        # Initialize teams in the dictionary if not already present
        if home_team not in team_points:
            team_points[home_team] = 0
        if away_team not in team_points:
            team_points[away_team] = 0

        # Award points based on match result
        if result == 'H':  # Home team wins
            team_points[home_team] += 3
        elif result == 'A':  # Away team wins
            team_points[away_team] += 3
        elif result == 'D':  # Draw
            team_points[home_team] += 1
            team_points[away_team] += 1

    # Convert team points into a DataFrame and rank by points
    points_df = pd.DataFrame(team_points.items(), columns=['Team', 'Points'])
    points_df = points_df.sort_values(by='Points', ascending=False).reset_index(drop=True)
    # Set the index starting from 1 instead of 0
    points_df.index += 1

    return points_df

# Streamlit app layout
st.title("Football League Seasonal Leaderboard")

# Load the full dataset
df = load_data()

# Get unique seasons from the dataset
seasons = df['season'].unique()

# Create a select box to choose the season
selected_season = st.selectbox("Choose a Season", seasons)

# Filter data for the selected season
season_df = df[df['season'] == selected_season]

# Display the team rankings for the selected season
st.write(f"Team Rankings for Season {selected_season}")
points_df = calculate_team_points(season_df)
st.dataframe(points_df)








