import streamlit as st
import pandas as pd

# Load the dataset from 'dataset.csv'
@st.cache_data
def load_data():
    df = pd.read_csv('ML_data.csv')  
    df['Time'] = pd.to_datetime(df['Time'])  # Ensure Time column is in datetime format
    return df

# Calculate the team points based on match results for the selected season
def calculate_team_stats(df):
    team_stats = {}

    # Loop through each match to calculate points
    for _, row in df.iterrows():
        home_team = row['HomeTeam']
        away_team = row['AwayTeam']
        result = row['FTR']
        home_goals = row['FTHG']
        away_goals = row['FTAG']  

        # Initialize teams in the dictionary if not already present
        if home_team not in team_stats:
            team_stats[home_team] = {'W': 0, 'D': 0, 'L': 0, 'G': 0, 'GC': 0, 'Points': 0}
        if away_team not in team_stats:
            team_stats[away_team] = {'W': 0, 'D': 0, 'L': 0, 'G': 0, 'GC': 0, 'Points': 0}

        # Update goals scored and goals conceded
        team_stats[home_team]['G'] += home_goals
        team_stats[home_team]['GC'] += away_goals
        team_stats[away_team]['G'] += away_goals
        team_stats[away_team]['GC'] += home_goals

        # Award points based on match result
        if result == 'H':  
            team_stats[home_team]['Points'] += 3
            team_stats[home_team]['W'] += 1
            team_stats[away_team]['L'] += 1
        elif result == 'A':  
            team_stats[away_team]['Points'] += 3
            team_stats[away_team]['W'] += 1
            team_stats[home_team]['L'] += 1
        elif result == 'D':  
            team_stats[home_team]['Points'] += 1
            team_stats[away_team]['Points'] += 1
            team_stats[home_team]['D'] += 1
            team_stats[away_team]['D'] += 1

    # Convert team points into a DataFrame and rank by points
    stats_df = pd.DataFrame(
        [(team, stats['W'], stats['D'], stats['L'], stats['G'], stats['GC'], stats['Points']) for team, stats in team_stats.items()],
        columns=['Team', 'Wins', 'Draws', 'Losses', 'Goals Scored', 'Goals Conceded', 'Points']
    )
    stats_df = stats_df.sort_values(by='Points', ascending=False).reset_index(drop=True)
    # Set the index starting from 1 instead of 0
    stats_df.index += 1

    return stats_df

# Streamlit app layout
st.title("Jupiler Pro-League Predictions")

# Load the full dataset
df = load_data()

# Get unique seasons from the dataset
seasons = df['season'].unique()

# Create a select box to choose the season
selected_season = st.selectbox("Choose a Season", seasons)

# Filter data for the selected season
season_df = df[df['season'] == selected_season]

# Display the team rankings for the selected season
st.write(f"Team Rankings for {selected_season}")
stats_df = calculate_team_stats(season_df)
st.dataframe(stats_df)








