import streamlit as st
import pandas as pd
import base64
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder

# Cache the dataset loading
@st.cache_data
def load_data():
    df = pd.read_csv('./Streamlit/ML_data.csv')  
    # Ensure 'Date' is in string format and 'Time' is in string format before concatenation
    df['Date'] = df['Date'].astype(str)
    df['Time'] = df['Time'].astype(str)
    
    # Combine 'Date' and 'Time' columns into a single 'DateTime' column for proper sorting
    df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])  
    return df

# Load dataset
df = load_data()

# Load upcoming matches from a new CSV file (from the image) for the 2024-2025 season
upcoming_matches_df = pd.DataFrame({
    'Date': ['20/09/2024', '21/09/2024', '21/09/2024', '21/09/2024', '22/09/2024', '22/09/2024', '22/09/2024', '22/09/2024'],
    'HomeTeam': ['Standard', 'Beerschot VA', 'Westerlo', 'Anderlecht', 'Club Brugge', 'Mechelen', 'Genk', 'Oud-Heverlee Leuven'],
    'AwayTeam': ['St. Gilloise', 'St Truiden', 'Antwerp', 'Charleroi', 'Gent', 'Cercle Brugge', 'Dender', 'Kortrijk']
})

# Encode 'HomeTeam', 'AwayTeam', and 'season'
le_home = LabelEncoder()
le_away = LabelEncoder()
le_season = LabelEncoder()

df['HomeTeam_encoded'] = le_home.fit_transform(df['HomeTeam'])
df['AwayTeam_encoded'] = le_away.fit_transform(df['AwayTeam'])
df['season_encoded'] = le_season.fit_transform(df['season'])

# Prepare features and target variable for model
features = ['season_encoded', 'HomeTeam_encoded', 'AwayTeam_encoded', 'HomeTeamStrength', 'AwayTeamStrength',
            'avgHG', 'avgAG', 'avgHHG', 'avgHAG', 'avgHST', 'avgAST']
X = df[features]
y = df['FTR'].map({'H': 0, 'D': 1, 'A': 2})

# Train logistic regression model
model = LogisticRegression(max_iter=1000)
model.fit(X, y)

# Function to predict outcome for upcoming matches in the 2024-2025 season
def predict_outcome_2024(home_team, away_team):
    home_team_encoded = le_home.transform([home_team])[0]
    away_team_encoded = le_away.transform([away_team])[0]
    
    # Use a default season (2024-2025) for the prediction
    season_encoded = le_season.transform(['S2024/2025'])[0]
    
    team_data = df.loc[df['HomeTeam'] == home_team].iloc[0]
    
    # Create a DataFrame with the same feature names as the original training data
    match_features = pd.DataFrame([[season_encoded, home_team_encoded, away_team_encoded,
                                    team_data['HomeTeamStrength'], team_data['AwayTeamStrength'],
                                    team_data['avgHG'], team_data['avgAG'], team_data['avgHHG'], 
                                    team_data['avgHAG'], team_data['avgHST'], team_data['avgAST']]],
                                  columns=features)
    
    # Make predictions
    prediction = model.predict(match_features)
    result_map = {0: 'Home Win', 1: 'Draw', 2: 'Away Win'}
    
    return result_map[prediction[0]]

# Function to calculate team stats for a season
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
    stats_df.index += 1  # Set the index starting from 1 instead of 0

    return stats_df

# Function to get last 5 match stats
def get_team_last_5_matches_avg_stats(df, team):
    team_matches = df[(df['HomeTeam'] == team) | (df['AwayTeam'] == team)].sort_values(by='DateTime', ascending=False).head(5)

    avg_stats = {
        'Stat': ['Average Home Shots', 'Average Away Shots', 'Average Home Shots on Target', 
                 'Average Away Shots on Target', 'Average Home Corners', 'Average Away Corners', 
                 'Average Home Fouls', 'Average Away Fouls', 'Average Home Yellow Cards', 
                 'Average Away Yellow Cards', 'Average Home Red Cards', 'Average Away Red Cards', 
                 'Average Full Time Home Goals (FTHG)', 'Average Full Time Away Goals (FTAG)', 
                 'Accuracy (Home Shots on Target / Home Shots)'],
        'Value': [
            f"{round(team_matches['HS'].mean(), 2):.2f}",
            f"{round(team_matches['AS'].mean(), 2):.2f}",
            f"{round(team_matches['HST'].mean(), 2):.2f}",
            f"{round(team_matches['AST'].mean(), 2):.2f}",
            f"{round(team_matches['HC'].mean(), 2):.2f}",
            f"{round(team_matches['AC'].mean(), 2):.2f}",
            f"{round(team_matches['HF'].mean(), 2):.2f}",
            f"{round(team_matches['AF'].mean(), 2):.2f}",
            f"{round(team_matches['HY'].mean(), 2):.2f}",
            f"{round(team_matches['AY'].mean(), 2):.2f}",
            f"{round(team_matches['HR'].mean(), 2):.2f}",
            f"{round(team_matches['AR'].mean(), 2):.2f}",
            f"{round(team_matches['FTHG'].mean(), 2):.2f}",
            f"{round(team_matches['FTAG'].mean(), 2):.2f}",
            f"{round(team_matches['HST'].sum() / team_matches['HS'].sum() if team_matches['HS'].sum() > 0 else 0, 2):.2f}"
        ]
    }

    return pd.DataFrame(avg_stats)

# Function to style the DataFrame
def style_dataframe(df):
    return df.style.set_properties(**{
        'color': 'white',
        'font-weight': 'bold',
        'background-color': 'rgba(0, 0, 0, 0.8)',  
        'text-align': 'center',
        'border': '2px solid #ffffff',
        'padding': '12px',
        'font-size': '18px'
    })

# Inject CSS for background image
def set_background(jpg_file):
    bin_str = get_base64_of_bin_file(jpg_file)
    page_bg_img = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{bin_str}");
        background-size: cover;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Convert image to base64 to use in CSS
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Set the background image using the correct path
set_background('./Streamlit/jupprolg.jpg')

# Streamlit app layout
st.title("Jupiler Pro-League App")

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a section", ["Upcoming Matches & Predictions", "Compare Team Stats", "Team Rankings"])

# Section 1: Upcoming Matches and Predictions for the 2024-2025 season
if page == "Upcoming Matches & Predictions":
    st.header("Upcoming Matches and Predictions (S2024/2025)")

    predictions = []
    for _, match in upcoming_matches_df.iterrows():
        result = predict_outcome_2024(match["HomeTeam"], match["AwayTeam"])
        predictions.append({
            "Date": match["Date"],
            "Home Team": match["HomeTeam"], 
            "Away Team": match["AwayTeam"], 
            "Prediction": result
        })

    predicted_matches = pd.DataFrame(predictions)
    st.table(predicted_matches)

# Section 2: Compare Team Stats over Last 5 Matches
elif page == "Compare Team Stats":
    st.header("Compare Team Stats (Last 5 Matches)")

    teams = pd.concat([df['HomeTeam'], df['AwayTeam']]).unique()
    team1 = st.selectbox("Select Team 1", teams)
    team2 = st.selectbox("Select Team 2", teams)

    if team1 and team2:
        # Get the average stats for the two teams
        team1_stats_df = get_team_last_5_matches_avg_stats(df, team1)
        team2_stats_df = get_team_last_5_matches_avg_stats(df, team2)

        # Create two columns for side-by-side comparison
        col1, col2 = st.columns(2)

        # Display the stats for Team 1
        with col1:
            st.subheader(f"{team1} Stats")
            st.dataframe(style_dataframe(team1_stats_df.set_index('Stat')))

        # Display the stats for Team 2
        with col2:
            st.subheader(f"{team2} Stats")
            st.dataframe(style_dataframe(team2_stats_df.set_index('Stat')))

# Section 3: Team Rankings for a Selected Season
elif page == "Team Rankings":
    st.header("Team Rankings")

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
