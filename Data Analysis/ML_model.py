import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report

df = pd.read_csv('ML_data.csv')

# Encode 'HomeTeam' and 'AwayTeam'
le_home = LabelEncoder()
le_away = LabelEncoder()
df['HomeTeam_encoded'] = le_home.fit_transform(df['HomeTeam'])
df['AwayTeam_encoded'] = le_away.fit_transform(df['AwayTeam'])

le_season = LabelEncoder()
df['season_encoded'] = le_season.fit_transform(df['season'])

# Prepare features and target variable
features = ['season_encoded', 'HomeTeam_encoded', 'AwayTeam_encoded', 'HomeTeamStrength', 'AwayTeamStrength', 
            'avgHG', 'avgAG', 'avgHHG', 'avgHAG', 'avgHST', 'avgAST','FTR']
df_ML = df[features]

#Split the data into training and testing sets
X= df_ML.drop('FTR', axis=1)
y = df_ML['FTR']

# Convert the target to numerical classes (0, 1, 2)
y = y.map({'H': 0, 'D': 1, 'A': 2})

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.35, random_state=71)

model = LogisticRegression(penalty='l2', multi_class='multinomial', solver='lbfgs', C=0.2, max_iter=400, class_weight='balanced', random_state=71)

# Train the model
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Print the classification report
print(classification_report(y_test, y_pred))

# Making Predictions with new inputs
# Function to dynamically retrieve stats based on season and teams
def get_team_stats(df, season, home_team, away_team):
    # Filter for home team stats in the specified season
    home_team_stats = df[
        (df['season'] == season) & 
        (df['HomeTeam'] == home_team)
    ].iloc[0]  # Assuming one row per team per season

    # Filter for away team stats in the specified season
    away_team_stats = df[
        (df['season'] == season) & 
        (df['AwayTeam'] == away_team)
    ].iloc[0]  # Assuming one row per team per season

# Return a dictionary of the extracted stats
    return {
        'HomeTeamStrength': home_team_stats['HomeTeamStrength'],
        'AwayTeamStrength': away_team_stats['AwayTeamStrength'],
        'avgHG': home_team_stats['avgHG'],
        'avgAG': away_team_stats['avgAG'],
        'avgHHG': home_team_stats['avgHHG'],
        'avgHAG': away_team_stats['avgHAG'],
        'avgHST': home_team_stats['avgHST'],
        'avgAST': away_team_stats['avgAST'],
    }

# Example input parameters
input_season = 'S2024/2025'
input_home_team = 'Cercle Brugge'
input_away_team = 'Genk'

# Dynamically retrieve stats for both teams
team_stats = get_team_stats(df, input_season, input_home_team, input_away_team)

# Encode the input values
input_season_encoded = le_season.transform([input_season])[0]
input_home_team_encoded = le_home.transform([input_home_team])[0]
input_away_team_encoded = le_away.transform([input_away_team])[0]

# Create the new input DataFrame for your model
new_input = pd.DataFrame({
    'season_encoded': [input_season_encoded],
    'HomeTeam_encoded': [input_home_team_encoded],
    'AwayTeam_encoded': [input_away_team_encoded],
    'HomeTeamStrength': [team_stats['HomeTeamStrength']],
    'AwayTeamStrength': [team_stats['AwayTeamStrength']],
    'avgHG': [team_stats['avgHG']],
    'avgAG': [team_stats['avgAG']],
    'avgHHG': [team_stats['avgHHG']],
    'avgHAG': [team_stats['avgHAG']],
    'avgHST': [team_stats['avgHST']],
    'avgAST': [team_stats['avgAST']],
    # remove odds and redcard to improve higher accuracy
})
print(new_input)

# Use the new input for prediction
prediction = model.predict(new_input)
predicted_result = {0: 'Home Win', 1: 'Draw', 2: 'Away Win'}[prediction[0]]
print(f"Predicted match outcome: {predicted_result}")   

