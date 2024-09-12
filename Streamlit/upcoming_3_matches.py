import streamlit as st
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder

# Load dataset
df = pd.read_csv('./Streamlit/ML_data.csv')

# Encode 'HomeTeam' and 'AwayTeam'
le_home = LabelEncoder()
le_away = LabelEncoder()
df['HomeTeam_encoded'] = le_home.fit_transform(df['HomeTeam'])
df['AwayTeam_encoded'] = le_away.fit_transform(df['AwayTeam'])

# Prepare features and target variable
features = ['HomeTeam_encoded', 'AwayTeam_encoded', 'HomeTeamStrength', 'AwayTeamStrength',
            'avgHG', 'avgAG', 'avgHHG', 'avgHAG', 'avgHST', 'avgAST', 'avgHR', 'avgAR']
X = df[features]
y = df['FTR'].map({'H': 0, 'D': 1, 'A': 2})

# Train logistic regression model
model = LogisticRegression(max_iter=1000)
model.fit(X, y)

# Function to predict outcome for upcoming matches
def predict_outcome(home_team, away_team):
    home_team_encoded = le_home.transform([home_team])[0]
    away_team_encoded = le_away.transform([away_team])[0]
    
    # Use a default team data for the example
    team_data = df.loc[df['HomeTeam'] == home_team].iloc[0]
    
    match_features = [[home_team_encoded, away_team_encoded,
                      team_data['HomeTeamStrength'], team_data['AwayTeamStrength'],
                      team_data['avgHG'], team_data['avgAG'], team_data['avgHHG'], team_data['avgHAG'],
                      team_data['avgHST'], team_data['avgAST'], team_data['avgHR'], team_data['avgAR']]]
    
    prediction = model.predict(match_features)
    result_map = {0: 'Home Win', 1: 'Draw', 2: 'Away Win'}
    
    return result_map[prediction[0]]

# Streamlit app layout
st.title("Jupiler Pro League Predictions")
st.header("Upcoming Matches and Predictions")

upcoming_matches = [
    {"HomeTeam": "Club Brugge", "AwayTeam": "Genk"},
    {"HomeTeam": "Anderlecht", "AwayTeam": "Gent"},
    {"HomeTeam": "Standard", "AwayTeam": "Oostende"}
]

predictions = []
for match in upcoming_matches:
    result = predict_outcome(match["HomeTeam"], match["AwayTeam"])
    predictions.append({"Home Team": match["HomeTeam"], "Away Team": match["AwayTeam"], "Prediction": result})

predicted_matches_df = pd.DataFrame(predictions)

st.table(predicted_matches_df)
