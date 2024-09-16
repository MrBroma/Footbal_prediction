import streamlit as st
import pandas as pd
import base64

# Load the dataset
df = pd.read_csv('./Streamlit/ML_data.csv')

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

# Combine 'Date' and 'Time' columns into a single 'DateTime' column for proper sorting
df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])

# Function to get the 5 most recent match stats for each team and calculate averages
def get_team_last_5_matches_avg_stats(df, team):
    # Filter matches where the team played either as home or away
    team_matches = df[(df['HomeTeam'] == team) | (df['AwayTeam'] == team)]

    # Sort matches by DateTime to get the most recent ones
    team_matches = team_matches.sort_values(by='DateTime', ascending=False).head(5)

    # Calculate the averages for the last 5 matches and format to 2 decimal places
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
        'background-color': 'rgba(0, 0, 0, 0.8)',  # Dark background with slight transparency
        'text-align': 'center',   # Center align the text
        'border': '2px solid #ffffff',   # Add a solid white border around each cell
        'padding': '12px',  # Increase padding for more spacing within cells
        'font-size': '18px'  # Set larger font size for better readability
    })

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a section", ["Upcoming Matches & Odds", "Compare Team Stats (Last 5 Matches)"])

# First section: Upcoming matches with predictions and odds
if page == "Upcoming Matches & Odds":
    st.title("Upcoming Matches and Predictions")

    # Sample data for predicted outcomes (you could replace this with a model's predictions)
    upcoming_matches = pd.DataFrame({
        'Home Team': ['Club Brugge', 'Anderlecht', 'Standard Liège'],
        'Away Team': ['Genk', 'Gent', 'Oostende'],
        'Prediction': ['Home Win', 'Draw', 'Away Win']
    })

    # Display predicted outcomes
    st.subheader("Predicted Outcomes for Upcoming Matches")
    st.table(upcoming_matches)

# Second section: Compare team stats over the last 5 matches
elif page == "Compare Team Stats (Last 5 Matches)":
    st.title("Compare Team Stats for the Last 5 Matches")

    # Get a list of all teams
    teams = pd.concat([df['HomeTeam'], df['AwayTeam']]).unique()

    # Select two teams to compare
    team1 = st.selectbox("Select Team 1", teams)
    team2 = st.selectbox("Select Team 2", teams)

    if team1 and team2:
        # Get the average stats for the two teams
        team1_stats_df = get_team_last_5_matches_avg_stats(df, team1)
        team2_stats_df = get_team_last_5_matches_avg_stats(df, team2)

        # Create two columns for side-by-side comparison
        col1, col2 = st.columns(2)

        # Display the stats for Team 1 with the opaque background for readability
        with col1:
            st.markdown('<div class="stats-container">', unsafe_allow_html=True)
            st.subheader(f"{team1} Stats")
            st.dataframe(style_dataframe(team1_stats_df.set_index('Stat')))  # Using st.dataframe() to allow scrolling
            st.markdown('</div>', unsafe_allow_html=True)

        # Display the stats for Team 2 with the opaque background for readability
        with col2:
            st.markdown('<div class="stats-container">', unsafe_allow_html=True)
            st.subheader(f"{team2} Stats")
            st.dataframe(style_dataframe(team2_stats_df.set_index('Stat')))  # Using st.dataframe() to allow scrolling
            st.markdown('</div>', unsafe_allow_html=True)
